# Kubernetes Ingress Demo

This repository contains a minimal three-tier application intended for demonstrating Kubernetes Ingress routing and path-based routing.

- Frontend: React single-page app served on port 3000 (served as static files in the container).
- Backend: Node + Express API on port 4000 exposing `/api/message`.
- Redis: in-cluster Redis used by the backend to increment a visit counter.

Prerequisites

- Docker (or a container runtime compatible with your cluster)
- kubectl
- A Kubernetes cluster (minikube, kind, microk8s, or remote cluster)
- An Ingress controller (e.g. ingress-nginx)

Overview

- The frontend is configured to call `/api/message`. The Ingress routes `/` to the `frontend` service and `/api` to the `backend` service, demonstrating path-based routing and different backends under one host.

Build container images (options)

Option A — standard Docker (local):

```bash
docker build -t ingress-demo-frontend:latest ./frontend
docker build -t ingress-demo-backend:latest ./backend
```

Option B — minikube (use minikube's Docker daemon):

```bash
# Linux/macOS
eval "$(minikube -p minikube docker-env)"
# Windows PowerShell (run as Admin)
minikube -p minikube docker-env --shell powershell | Invoke-Expression
docker build -t ingress-demo-frontend:latest ./frontend
docker build -t ingress-demo-backend:latest ./backend
```

Option C — kind: build images locally and load into kind cluster:

```bash
docker build -t ingress-demo-frontend:latest ./frontend
docker build -t ingress-demo-backend:latest ./backend
kind load docker-image ingress-demo-frontend:latest
kind load docker-image ingress-demo-backend:latest
```

Push to registry (remote cluster)

If your cluster cannot access local images, tag and push the images to a registry and update the image names in the `k8s` manifests.

Deploy to Kubernetes

1. Ensure an Ingress controller is installed and running. Examples:

minikube:

```bash
minikube addons enable ingress
```

kind:

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/kind/deploy.yaml
```

2. Apply manifests (order is not strict):

```bash
kubectl apply -f k8s/redis-deployment.yaml
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/ingress.yaml
```

Expose host and access

1. Find the Ingress IP or use minikube IP:

```bash
kubectl get ingress
# or for minikube:
minikube ip
```

2. Add an OS host entry mapping `example.local` to the ingress IP. On Windows edit `C:\Windows\System32\drivers\etc\hosts` as Administrator and add:

```
<INGRESS_IP> example.local
```

3. Open `http://example.local` in your browser.

Alternative: if your cluster does not surface a cluster IP for ingress, port-forward the frontend service for a quick check:

```bash
kubectl port-forward svc/frontend 8080:80
# then open http://localhost:8080
```

Local development without Kubernetes

Backend

```bash
cd backend
npm install
npm start
# listens on :4000
```

Frontend

```bash
cd frontend
npm install
npm run build
npx serve -s build -l 3000
# open http://localhost:3000
```

Files in this repo

- `k8s/redis-deployment.yaml` — Redis Deployment + Service
- `k8s/backend-deployment.yaml` — Backend Deployment + ClusterIP Service
- `k8s/frontend-deployment.yaml` — Frontend Deployment + ClusterIP Service
- `k8s/ingress.yaml` — Ingress rules mapping `/` to frontend and `/api` to backend
- `frontend/` — React app and `Dockerfile`
- `backend/` — Node API and `Dockerfile`

Troubleshooting

- Check the ingress controller logs if no rules are applied: `kubectl -n ingress-nginx logs deploy/ingress-nginx-controller` (namespace may vary).
- If services return 404 from the ingress, ensure the `host` in `k8s/ingress.yaml` matches the host you use in the browser.
- If images are not found by the cluster, use `kind load docker-image` or push to a registry.

Cleanup

```bash
kubectl delete -f k8s/ingress.yaml
kubectl delete -f k8s/frontend-deployment.yaml
kubectl delete -f k8s/backend-deployment.yaml
kubectl delete -f k8s/redis-deployment.yaml
```




