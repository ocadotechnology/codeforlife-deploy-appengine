from django_site.wsgi import application

from google.auth import compute_engine
from google.cloud.container_v1 import ClusterManagerClient
from kubernetes import client


try:
    import googleclouddebugger

    googleclouddebugger.enable()
except ImportError:
    pass


def setup_gke():
    project_id = "decent-digit-629"
    zone = "europe-west1-b"
    cluster_id = "agones-terraform-dev"

    credentials = compute_engine.Credentials()

    cluster_manager_client = ClusterManagerClient(credentials=credentials)
    cluster = cluster_manager_client.get_cluster(project_id, zone, cluster_id)

    configuration = client.Configuration()
    configuration.host = f"https://{cluster.endpoint}:443"
    configuration.verify_ssl = False
    configuration.api_key = {"authorization": "Bearer " + credentials.token}
    client.Configuration.set_default(configuration)


setup_gke()

v1 = client.CoreV1Api()
print("Listing pods with their IPs:")
pods = v1.list_pod_for_all_namespaces(watch=False)
for i in pods.items:
    print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))


app = application
