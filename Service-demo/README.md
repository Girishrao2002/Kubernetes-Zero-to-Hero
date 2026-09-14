# Kubernetes Service Types Demo

This project provides a tiny web application that shows how Kubernetes Service types behave in a Minikube cluster.

It includes three examples:

1. ClusterIP
2. NodePort
3. LoadBalancer

## Application behavior

Every pod serves a simple HTML page that displays:

- the current Service type
- the pod hostname
- the namespace

The app also exposes a health endpoint at `/healthz`.

## File structure

- `app.py` — small Python HTTP app
- `Dockerfile` — container image for the demo app
- `k8s/` — Kubernetes manifests

## Build the image

From this directory:

```bash
docker build -t service-demo:latest .
minikube image load service-demo:latest
```

## Run locally

```bash
python app.py
```

Then open:

```text
http://localhost:8000
```

## Deploy all services

```bash
kubectl apply -f k8s/
```

## Verify the resources

```bash
kubectl get deployments,pods,svc
```

## Test each service type

### 1) ClusterIP

This type is only reachable inside the cluster:

```bash
kubectl get svc | grep clusterip
kubectl run curl --rm -it --restart=Never --image=curlimages/curl -- sh
# inside the pod
curl http://demo-clusterip.default.svc.cluster.local
```

### 2) NodePort

```bash
minikube service demo-nodeport --url
```

Then open the URL printed by Minikube in a browser.

### 3) LoadBalancer

```bash
minikube service demo-loadbalancer --url
```

Then open the URL printed by Minikube in a browser.

## Cleanup

```bash
kubectl delete -f k8s/
```
