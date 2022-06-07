# Overview

The kubernetes-integration project is a high-level API for creating, updating, and deleting Kubernetes artifacts such as services, endpoints, and config maps. 

# Kubernetes Integration Modules

## Client

The [client](src/org/hokiegeek2/integration/kubernetes/client.py) module contains the KubernetesClient class that serves as the base class for all kubernetes-integration classes. Accordingly, the KubernetesClient class encapsulates logic and state required to (1) connect to the Kubernetes API, and (2) execute create, read, update, and delete requests against the k8s API.

## ConfigMap

The [config_map](src/org/hokiegeek2/integration/kubernetes/config_map.py) module contains the ConfigMapClient that encapsulates logic to retrieve and update ConfigMaps.

## Prometheus

The [prometheus](src/org/hokiegeek2/integration/kubernetes/prometheus.py) module contains the PrometheusKubernetesClient that encapsulates logic to add and remove scrape configs within a Prometheus server ConfigMap.

# Installation

Navigate to the [src](src/) directory and execute the following command:

```
pip install -e .
```

# Deployment

## Docker

Navigate to the project home directory and execute the following command:

```
docker build -f Dockerfile -t hokiegeek2/kubernetes-integration:0.0.1 .
```
