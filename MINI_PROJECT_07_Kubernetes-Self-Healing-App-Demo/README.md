# Kubernetes Self-Healing Application Demo

This project deploys an interactive Flask calculator web application on a local Kubernetes cluster (Minikube) with a Deployment of `3` replicas, a internal `ClusterIP` Service, and an external `NodePort` Service. It includes an automated PowerShell script to demonstrate Kubernetes' native self-healing (auto-recovery) capability by deleting random pods and showing instant replacement.

## Project Structure
```text
MINI_PROJECT_07_Kubernetes-Self-Healing-App-Demo/
├── app/
│   ├── app.py           # Flask web calculator source code
│   ├── requirements.txt # Python package dependencies
│   └── Dockerfile       # Container definition
├── k8s/
│   ├── deployment.yaml  # Deployment config (3 replicas)
│   └── service.yaml     # ClusterIP and NodePort Service definitions
├── chaos-monkey.ps1     # PowerShell script simulating pod failures
└── README.md            # This file
```

---

## Prerequisites
- **Minikube** installed and running (`minikube status`)
- **kubectl** installed and configured (`kubectl get nodes`)
- **PowerShell** (for running the auto-healing chaos test script)

---

## Deployment Steps

### 1. Build the Docker Image
Build the container image directly inside the Minikube registry:
```powershell
minikube image build -t calculator-app:latest ./app
```

### 2. Apply Manifests
Apply the Deployment and Service configurations to the cluster:
```powershell
kubectl apply -f k8s/
```

### 3. Verify Active Replicas
Confirm that all `3` replicas are successfully running:
```powershell
kubectl get pods -l app=calculator-app
```

---

## Demonstrating Kubernetes Auto-Healing

### Step 1: Watch the pods live (Recommended)
Open a separate terminal window and start a watch stream to observe pods shifting statuses in real-time:
```powershell
kubectl get pods -l app=calculator-app -w
```

### Step 2: Run the Chaos Script
In your main terminal window, run the chaos monkey script to randomly delete a pod:
```powershell
powershell -ExecutionPolicy Bypass -File .\chaos-monkey.ps1
```

### What happens under the hood:
1. The script fetches all active pod names running the calculator app.
2. It picks one pod at random and deletes it (`kubectl delete pod`).
3. Kubernetes immediately detects that the actual state (2 pods) does not match the desired state configured in our deployment (3 pods).
4. Within **2 seconds**, Kubernetes schedules and launches a brand new replacement pod, returning the deployment to a healthy `Running` state with 3 pods.
5. The script loops infinitely every 15 seconds to allow you to capture a clean video or GIF of this recovery cycle. Use `Ctrl+C` to terminate the script loop.

---

## Cleanup
To remove all deployed Kubernetes resources:
```powershell
kubectl delete -f k8s/
```
