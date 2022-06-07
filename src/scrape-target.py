#!/usr/bin/env python

import os, json
from org.hokiegeek2.integration.kubernetes.client \
     import getConfig
from org.hokiegeek2.integration.kubernetes.prometheus \
     import PrometheusKubernetesClient, ScrapeTargetAction

try:
    server = os.environ['PROMETHEUS_SERVER']
    namespace = os.environ['PROMETHEUS_NAMESPACE']
    targetName = os.environ['PROMETHEUS_SCRAPE_TARGET_NAME']
    targetAction = os.environ['PROMETHEUS_SCRAPE_TARGET_ACTION']
except KeyError as ke:
    raise EnvironmentError(f'Prometheus env variable {ke} is missing')

try:
    host = os.environ['KUBERNETES_HOST']
    certPath = os.environ['CERT_PATH']
    keyPath = os.environ['KEY_PATH']
except KeyError as ke:
    raise EnvironmentError(f'Kubernetes env variable {ke} is missing')

try: 
    action = ScrapeTargetAction(targetAction)
except ValueError:
    raise EnvironmentError((f'{action} is not a valid ScrapeTarget, check ' +
          'the PROMETHEUS_SCRAPE_TARGET_ACTION env variable'))

config = getConfig(host=host,certPath=certPath,keyPath=keyPath)

pc = PrometheusKubernetesClient(config)

if action == ScrapeTargetAction.ADD:
    try:
        addPayload = json.loads(os.environ['PROMETHEUS_SCRAPE_TARGET'])
    except KeyError:
        raise EnvironmentError(('PROMETHEUS_SCRAPE_TARGET must not None for ' +
                               'scrape target adds'))
    except json.JSONDecodeError as je:
        raise ValueError(je)
    pc.addPrometheusScrapeTarget(server, namespace, addPayload)
elif action == ScrapeTargetAction.RETRIEVE:
    target = pc.getPrometheusScrapeTarget(server, namespace, targetName)
    print(f'Scrape Target {target} for target name {targetName}')
else:
    pc.removePrometheusScrapeTarget(server, namespace, targetName)

