from kubernetes.client import ApiClient, Configuration, CoreV1Api, AppsV1Api
from dataclasses import dataclass
import urllib3

urllib3.disable_warnings()

def getConfig(host : str, certPath: str, keyPath: str) -> Configuration:
    config = Configuration()

    config.host = host
    config.cert_file = certPath
    config.key_file = keyPath
    config.verify_ssl = False

    return config

@dataclass
class KubernetesClient():

    __slots__ = ('coreClient', 'appsClient')

    coreClient: CoreV1Api
    appsClient: AppsV1Api

    def __init__(self, config : Configuration) -> None:
        apiClient = ApiClient(configuration=config)
        self.coreClient = CoreV1Api(api_client=apiClient)
        self.appsClient = AppsV1Api(api_client=apiClient)
