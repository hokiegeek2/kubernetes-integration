import json, yaml
from enum import Enum
from typing import Dict, List
from kubernetes.client import Configuration
from kubernetes.client.rest import ApiException
from org.hokiegeek2.integration.core import IntegrationError
from org.hokiegeek2.integration.kubernetes.client import KubernetesClient

'''
The ScrapTargetAction enum encapsulates the currently-supported actions
'''
class ScrapeTargetAction(Enum):
    ADD =  'ADD'
    REMOVE = 'REMOVE'
    RETRIEVE = 'RETRIEVE'

    def __str__(self) -> str:
        '''
        Overridden method returns value
        '''
        return self.value
    
    def __repr__(self) -> str: 
        '''
        Overridden method returns value
        '''
        return self.value

class PrometheusKubernetesClient(KubernetesClient):

    def __init__(self, config : Configuration) -> None:
        KubernetesClient.__init__(self, config)

    def getPrometheusConfig(self, name: str, namespace) -> Dict:
        # Retrieve Prometheus ConfigMap
        try:
            cm = self.coreClient.read_namespaced_config_map(name, namespace)
        except ApiException as e:
            raise IntegrationError(e)

        if not cm:
            raise ValueError(f'ConfigMap {name} is not in namespace {namespace}')

        # Retrieve prometheus.yml string and convert to yaml dict
        try: 
            return yaml.safe_load(cm.data['prometheus.yml'])
        except Exception as e:
            raise ValueError(f'in retrieving prometheus.yml {e}')

    def getPrometheusScrapeTargets(self, name : str, namespace : str) -> List[Dict]:
        # Retrieve prometheus.yml dict
        promConfig = self.getPrometheusConfig(name=name, namespace=namespace)

        # Retrieve and return scrape_configs list
        try:
            return promConfig['scrape_configs']
        except KeyError as ke:
            raise ValueError(f'{name} does not contain scrape_configs;')

    def getPrometheusScrapeTarget(self, name : str, namespace : str, 
                                                 targetName : str) -> List[Dict]:
        # Retrieve prometheus.yml dict
        promConfig = self.getPrometheusConfig(name=name, namespace=namespace)

        # Retrieve and return scrape_configs list
        try:
            for config in promConfig['scrape_configs']:
                if targetName == config['job_name']:
                    return config
            return None
        except KeyError as ke:
            raise ValueError(f'{name} does not contain scrape_configs;')

    def removePrometheusScrapeTarget(self, name : str, namespace : str, 
                                                  targetName : str) -> None:

        # Retrieve scrape_targets and remove scrape config dict
        scrape_configs = self.getPrometheusScrapeTargets(name=name,
                                                         namespace=namespace)
        for config in scrape_configs:
            # If the config has static_configs element, proceed
            if config.get('static_configs'):
                # Remove config from scrape_configs list
                if targetName == config['job_name']:
                    scrape_configs.remove(config)

        # Update scrape_configs in prometheus.yml and generate yaml str
        promConfig = self.getPrometheusConfig(name=name, namespace=namespace)
        promConfig['scrape_configs'] = scrape_configs

        # Retrieve ConfigMapl, set prometheus.yml to updated promConfig str
        try:
            cm = self.coreClient.read_namespaced_config_map(name, namespace)
        except ApiException as ae:
            raise IntegrationError(f'Kubernetes API error {ae}')
        try:
            cm.data['prometheus.yml'] = yaml.safe_dump(promConfig)
        except yaml.YAMLEror as ye:
            raise IntegrationError(f'YAML dump error: {ye}')

        # Patch ConfigMap with new prometheus.yml yaml string
        try:
            self.coreClient.patch_namespaced_config_map(name=name,
                                                    namespace=namespace,
                                                    body=cm)
        except ApiException as e:
            raise IntegrationError(e)

    def addPrometheusScrapeTarget(self, name : str, namespace, 
                                                scrapeTarget : Dict) -> None:
        # Retrieve scrape_targets and append scrape target
        scrape_configs = self.getPrometheusScrapeTargets(name=name,
                                                          namespace=namespace)
        scrape_configs.append(scrapeTarget)

        # Update scrape_configs in prometheus.yml
        promConfig = self.getPrometheusConfig(name=name, namespace=namespace)
        promConfig['scrape_configs'] = scrape_configs

        # Retrieve ConfigMap, set prometheus.yml element to updated promConfig str
        try:
            cm = self.coreClient.read_namespaced_config_map(name, namespace)
        except ApiException as ae:
            raise IntegrationError(f'Kubernetes API error {ae}')
        try:
            cm.data['prometheus.yml'] = yaml.safe_dump(promConfig)
        except yaml.YAMLEror as ye:
            raise IntegrationError(f'YAML dump error: {ye}')

        # Patch ConfigMap with new prometheus.yml yaml string
        try:
            self.coreClient.patch_namespaced_config_map(name=name,
                                                    namespace=namespace,
                                                    body=cm)
        except ApiException as e:
            raise IntegrationError(e)
