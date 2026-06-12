# Kubernetes Horizontal Pod Autoscaler (HPA) - Interactive Calculator

This project deploys a CPU-intensive Flask calculator web application on a local Kubernetes cluster (Minikube) and configures a Horizontal Pod Autoscaler (HPA) to scale the application dynamically from 2 to 8 replicas based on CPU utilization.

## Project Structure
```text
MINI_PROJECT_08_Kubernetes-Horizontal-Pod-Autoscaler/
├── app/
│   ├── app.py           # Interactive web calculator & CPU-intensive endpoint
│   ├── requirements.txt # Python package dependencies
│   └── Dockerfile       # Container definition
├── k8s/
│   └── deployment.yaml  # Combined Kubernetes Deployment, Service, and HPA manifests
└── README.md            # This file
```

---

## Prerequisites
- **Minikube** installed and running (`minikube status`)
- **kubectl** installed and configured (`kubectl get nodes`)
- **hey** load-testing tool installed (executable located at `C:\Users\STA-MADH-51\go\bin\hey.exe`)

---

## Getting Started

### 1. Enable Metrics Server
Enable the `metrics-server` addon in Minikube (required for HPA to monitor CPU usage):
```powershell
minikube addons enable metrics-server
```

### 2. Build the Docker Image
Build the container image directly inside the Minikube registry:
```powershell
minikube image build -t cpu-intensive-app:latest ./app
```

### 3. Deploy to Kubernetes
Apply the combined Deployment, Service, and HPA configurations:
```powershell
kubectl apply -f k8s/
```

---

## Load Testing & Monitoring Scaling

### Step 1: Open the Service Tunnel
Run the following command in a new terminal window to expose the service NodePort and print the application's local URL (e.g. `http://127.0.0.1:57001`):
```powershell
minikube service cpu-intensive-service
```

### Step 2: Watch HPA Scaling Status
In a second terminal window, watch the HPA status and pod count scale in real-time:
```powershell
kubectl get hpa cpu-intensive-hpa -w
```

### Step 3: Run the Load Test
In a third terminal, run the load-testing tool `hey` to stress the backend calculation endpoint. Replace `<PORT>` with the port number shown in Step 1 (e.g. `57001`):
```powershell
C:\Users\STA-MADH-51\go\bin\hey.exe -z 2m -c 50 "http://127.0.0.1:<PORT>/calculate?op=multiply&a=999&b=999"
```

As traffic loads the backend, you will observe the HPA CPU utilization rise and scale the replica count up to **8 pods**. Once the test ends, HPA will cool down and automatically scale the replica count back to **2 pods**.

---

## Cleanup
To remove all deployed Kubernetes resources:
```powershell
kubectl delete -f k8s/
```
