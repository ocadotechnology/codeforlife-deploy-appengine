import os
import sys

import kubernetes
import yaml

# Root directory of the project.
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
CURR_DIR = os.path.abspath(os.path.dirname(__file__))
LIB_DIR = os.path.join(BASE_DIR, "lib")


def get_aimmo_version():
    sys.path.append(LIB_DIR)
    from aimmo import __version__

    return __version__


def create_ingress_yaml(module_name):
    """
    Uses a template ingress yaml file in the same directory to construct a python yaml
    object. Replaces the ingress.global-static-ip-name annotation with the
    correct module name (depending on which cluster this script is ran in). Similarly for
    cors-allow-origin, it replaces it with the correct url for selected module.

    Also replaces the TLS certificate host name and the host for the ingress paths.

    :param module_name: The name of the environment we're in (ie. staging, dev
    :return: python object containing yaml with modified values.
    """
    path = os.path.join(CURR_DIR, "ingress.yaml")

    host_name = f"{module_name}-aimmo.codeforlife.education"

    with open(path) as yaml_file:
        content = yaml.safe_load(yaml_file.read())
        content["metadata"]["annotations"][
            "kubernetes.io/ingress.global-static-ip-name"
        ] = f"{module_name}-aimmo-ingress"
        content["metadata"]["annotations"][
            "nginx.ingress.kubernetes.io/cors-allow-origin"
        ] = f"https://{module_name}-dot-decent-digit-629.appspot.com"
        content["spec"]["tls"][0]["hosts"][0] = host_name
        content["spec"]["rules"][0]["host"] = host_name

    return content


def create_fleet_yaml(module_name, aimmo_version):
    """
    Uses a template fleet yaml file in the same directory to construct a python yaml
    object. Replaces image version with the one received as a parameter. Also replaces
    the GAME_API_URL environment variable with the correct url for the deployment
    environment we are in.

    :param module_name: The name of the environment we're in (ie. staging, dev).
    :param aimmo_version: The game version we want to deploy.
    :return: python object containing yaml with modified values.
    """
    path = os.path.join(CURR_DIR, "fleet.yaml")

    game_api_url = (
        f"https://{module_name}-dot-decent-digit-629.appspot.com/kurono/api/games/"
    )
    container_image = f"ocadotechnology/aimmo-game:{aimmo_version}"

    with open(path) as yaml_file:
        content = yaml.safe_load(yaml_file.read())

        env_variables = content["spec"]["template"]["spec"]["template"]["spec"][
            "containers"
        ][0]["env"]
        game_api_url_index = env_variables.index(
            {"name": "GAME_API_URL", "value": "REPLACE_ME"}
        )
        env_variables[game_api_url_index]["value"] = game_api_url
        content["spec"]["template"]["spec"]["template"]["spec"]["containers"][0][
            "image"
        ] = container_image

    return content


def create_creator_yaml(module_name, aimmo_version):
    """
    Loads an aimmo-game-creator yaml into a dictionary.

    Replaces the GAME_API_URL environment variable with the correct url for the
    deployment environment we are in

    :param module_name: The name of the environment we're in (ie. staging, dev).
    :param aimmo_version: The game version we want to deploy.
    :return: python object containing yaml with modified values.
    """

    def _replace_game_api_url(content):
        game_api_url = (
            "https://"
            + module_name
            + "-dot-decent-digit-629.appspot.com/kurono/api/games/"
        )
        env_variables = content["spec"]["template"]["spec"]["containers"][0]["env"]
        game_api_url_index = env_variables.index(
            {"name": "GAME_API_URL", "value": "REPLACE_ME"}
        )
        env_variables[game_api_url_index]["value"] = game_api_url

    def _replace_image_version(content):
        env_variables = content["spec"]["template"]["spec"]["containers"][0]["env"]
        image_suffix_index = env_variables.index(
            {"name": "IMAGE_SUFFIX", "value": "latest"}
        )
        env_variables[image_suffix_index]["value"] = aimmo_version

    def _replace_image_tag(content):
        content["spec"]["template"]["spec"]["containers"][0][
            "image"
        ] = "ocadotechnology/aimmo-game-creator:{}".format(aimmo_version)

    path = os.path.join(CURR_DIR, "rs_aimmo_game_creator.yaml")
    with open(path) as yaml_file:
        content = yaml.safe_load(yaml_file.read())
        _replace_game_api_url(content)
        _replace_image_version(content)
        _replace_image_tag(content)
    return content


def restart_pods(game_creator_yaml, ingress_yaml, fleet_yaml):
    """
    Restarts the kubernetes replication controllers, pods, services and ingresses
    in the 'default' namespace

    :param game_creator_yaml: The dict to create the aimmo game creator rc
    :param ingress_yaml: The dict to create the ingress
    :param fleet_yaml: The dict to create the fleet
    """
    for rs in apps_api_instance.list_namespaced_replica_set("default").items:
        if rs.metadata.name == game_creator_yaml["metadata"]["name"]:
            apps_api_instance.delete_namespaced_replica_set(
                body=kubernetes.client.V1DeleteOptions(),
                name=rs.metadata.name,
                namespace="default",
            )
    # for rc in api_instance.list_namespaced_replication_controller("default").items:
    #     api_instance.delete_namespaced_replication_controller(
    #         body=kubernetes.client.V1DeleteOptions(),
    #         name=rc.metadata.name,
    #         namespace="default",
    #     )
    # for pod in api_instance.list_namespaced_pod("default").items:
    #     api_instance.delete_namespaced_pod(
    #         body=kubernetes.client.V1DeleteOptions(),
    #         name=pod.metadata.name,
    #         namespace="default",
    #     )
    # for service in api_instance.list_namespaced_service("default").items:
    #     api_instance.delete_namespaced_service(
    #         name=service.metadata.name, namespace="default"
    #     )
    for ingress in networking_api_instance.list_namespaced_ingress("default").items:
        networking_api_instance.delete_namespaced_ingress(
            name=ingress.metadata.name,
            namespace="default",
            body=kubernetes.client.V1DeleteOptions(),
        )
    try:
        custom_objects_api_instance.delete_namespaced_custom_object(
            "agones.dev", "v1", "default", "fleets", fleet_yaml["metadata"]["name"]
        )
    except kubernetes.client.exceptions.ApiException as e:
        # This can fail when the fleet doesn't exist (before it's first created)
        print(
            f"Exception when calling CustomObjectsApi->delete_namespaced_custom_object: {e}\n"
        )

    networking_api_instance.create_namespaced_ingress("default", ingress_yaml)

    apps_api_instance.create_namespaced_replica_set(
        body=game_creator_yaml, namespace="default"
    )

    custom_objects_api_instance.create_namespaced_custom_object(
        "agones.dev", "v1", "default", "fleets", fleet_yaml
    )


def main(module_name):
    """
    :param module_name: The environment (ie. staging, etc).
    :param aimmo_version: The tagged version of AI:MMO. We will use this to
                          build the correct docker images.
    """
    kubernetes.config.load_kube_config("/home/runner/.kube/config")

    global api_instance
    global apps_api_instance
    global networking_api_instance
    global custom_objects_api_instance
    api_instance = kubernetes.client.CoreV1Api()
    apps_api_instance = kubernetes.client.AppsV1Api()
    networking_api_instance = kubernetes.client.NetworkingV1beta1Api()
    custom_objects_api_instance = kubernetes.client.CustomObjectsApi()
    aimmo_version = get_aimmo_version()

    ingress = create_ingress_yaml(module_name=module_name)
    game_creator_rs = create_creator_yaml(
        module_name=module_name, aimmo_version=aimmo_version
    )
    fleet = create_fleet_yaml(module_name=module_name, aimmo_version=aimmo_version)

    restart_pods(game_creator_rs, ingress, fleet)


if __name__ == "__main__":
    main(module_name=sys.argv[1])
