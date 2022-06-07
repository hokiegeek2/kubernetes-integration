from kubernetes.client import Configuration
from kubernetes.client.rest import ApiException
from org.hokiegeek2.integration.core import IntegrationError
from org.hokiegeek2.integration.kubernetes.client import KubernetesClient

class ConfigMapClient(KubernetesClient):

    def __init__(self, config : Configuration) -> None:
        KubernetesClient.__init__(self,config)

    def getConfigMap(self, name : str, namespace):
        try:
            cm = self.coreClient.read_namespaced_config_map(name, namespace)
        except ApiException as e:
            raise IntegrationError(e)
        if not cm:
            raise ValueError(f'cm named {name} in namespace {namespace} does not exist')
        return cm

    def updateConfigMap(self, name : str, namespace, cmName : str, cmValue : str) -> None:
        try:
            cm = self.coreClient.read_namespaced_config_map(name, namespace)
        except ApiException as e:
            raise IntegrationError(e)
        if not cm:
            raise ValueError(f'cm named {name} in namespace {namespace} does not exist')

        # update ConfigMap value
        cm.data[cmName]=cmValue

        # patch ConfigMap
        try:
            self.coreClient.patch_namespaced_config_map(name=name, 
                                               namespace=namespace,
                                              body=cm)
        except ApiException as e:
            raise IntegrationError(e)

