import os
import kubernetes
import yaml
import sys

# Root directory of the project.
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
CURR_DIR = os.path.abspath(os.path.dirname(__file__))


def create_ingress_yaml(module_name):
    """
    Uses a template yaml file in the same directory to construct a python yaml
    object. Replaces the ingress.global-static-ip-name annotation with the
    correct module name (depending on which cluster this script is ran in).

    :param module_name: The name of the environment we're in (ie. staging, dev
    :return: python object containing yaml.
    """
    path = os.path.join(CURR_DIR, 'ingress.yaml')
    print("printing current directory: ", path)

    with open(path) as yaml_file:
        content = yaml.safe_load(yaml_file.read())
        content['metadata']['annotations']['kubernetes.io/ingress.global-static-ip-name'] = module_name + '-aimmo-ingress'

    return content


def create_creator_yaml():
    path = os.path.join(CURR_DIR, 'rc_aimmo_game_creator.yaml')
    with open(path) as yaml_file:
        content = yaml.safe_load(yaml_file.read())
    return content


def restart_pods(game_creator, ingress_yaml):
    for rc in api_instance.list_namespaced_replication_controller('default').items:
        api_instance.delete_namespaced_replication_controller(
            body=kubernetes.client.V1DeleteOptions(),
            name=rc.metadata.name,
            namespace='default')
    for pod in api_instance.list_namespaced_pod('default').items:
        api_instance.delete_namespaced_pod(
            body=kubernetes.client.V1DeleteOptions(),
            name=pod.metadata.name,
            namespace='default')
    for service in api_instance.list_namespaced_service('default').items:
        api_instance.delete_namespaced_service(
            name=service.metadata.name,
            namespace='default')
    for ingress in extensions_api_instance.list_namespaced_ingress('default').items:
        extensions_api_instance.delete_namespaced_ingress(
            name=ingress.metadata.name,
            namespace='default',
            body=kubernetes.client.V1DeleteOptions())

    extensions_api_instance.create_namespaced_ingress("default", ingress_yaml)

    api_instance.create_namespaced_replication_controller(
        body=game_creator,
        namespace='default',
    )


def main(module_name):
    """
    :param module_name: The environment (ie. staging, etc).
    """
    kubernetes.config.load_kube_config("/home/runner/.kube/config")

    global api_instance
    global extensions_api_instance
    api_instance = kubernetes.client.CoreV1Api()
    extensions_api_instance = kubernetes.client.ExtensionsV1beta1Api()

    ingress = create_ingress_yaml(module_name=module_name)
    game_creator_rc = create_creator_yaml()

    restart_pods(game_creator_rc, ingress)


if __name__ == '__main__':
    main(module_name=sys.argv[1])
