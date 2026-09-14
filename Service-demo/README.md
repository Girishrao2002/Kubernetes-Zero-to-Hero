# Kubernetes Service Types Demo

This project demonstrates the three common Kubernetes Service types using a simple Python web app running inside Minikube:

1. ClusterIP
2. NodePort
3. LoadBalancer

The app is intentionally tiny and prints the active service type along with the pod name and namespace so you can visually confirm routing behavior.

## Application behavior

Each pod serves a simple HTML page on port 8000 and exposes a health endpoint at `/healthz`.

The page shows:

- the current Service type
- the pod hostname
- the namespace

## Project structure

- `app.py` — Python app that runs the demo website
- `Dockerfile` — container image definition
- `k8s/` — Kubernetes manifests for the service examples

## Prerequisites for Ubuntu

Install Docker, Minikube, and kubectl:

```bash
sudo apt update
sudo apt install -y curl ca-certificates conntrack docker.io

curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
chmod +x minikube-linux-amd64
sudo mv minikube-linux-amd64 /usr/local/bin/minikube
```

Start Minikube:

```bash
minikube start --driver=docker
kubectl get nodes
```

## Build and push the app image

This version is set up to deploy directly from a registry, so you do not need `minikube image load`.

Replace `yourdockerhubusername` with your actual Docker Hub username and run:

```bash
cd /path/to/Service-demo
docker build -t yourdockerhubusername/service-demo:latest .
docker push yourdockerhubusername/service-demo:latest
```

If you prefer a private registry or a local registry, use that image name instead of Docker Hub.

The Deployment files use `imagePullPolicy: Always` and reference:

```yaml
image: yourdockerhubusername/service-demo:latest
```

## Deploy all services

```bash
kubectl apply -f k8s/
kubectl get deployments,pods,svc
```

## Run locally on your machine

```bash
cd /path/to/Service-demo
python3 app.py
```

Then open:

```text
http://localhost:8000
```

Health check:

```text
http://localhost:8000/healthz
```

## Test each service type

### 1) ClusterIP

This service is reachable only from inside the cluster. Create a temporary pod and curl the service name:

```bash
kubectl run curl --rm -it --restart=Never --image=curlimages/curl -- sh
```

Inside the pod:

```bash
curl http://demo-clusterip.default.svc.cluster.local
```

### 2) NodePort

This service exposes the app on a node port for external access:

```bash
minikube service demo-nodeport --url
```

Open the URL printed by Minikube in the browser.

### 3) LoadBalancer

This service is exposed via a load balancer-like endpoint in Minikube:

```bash
minikube service demo-loadbalancer --url
```

Open the URL printed by Minikube in the browser.

## Troubleshooting

If you see `ImagePullBackOff`, it usually means the image name in the Deployment does not match the registry image you pushed.

Check the YAML image value and make sure it matches exactly:

```yaml
image: yourdockerhubusername/service-demo:latest
```

Then push the image again and re-apply the manifests:

```bash
docker build -t yourdockerhubusername/service-demo:latest .
docker push yourdockerhubusername/service-demo:latest
kubectl delete -f k8s/
kubectl apply -f k8s/
```

## Cleanup

```bash
kubectl delete -f k8s/
minikube stop
```
