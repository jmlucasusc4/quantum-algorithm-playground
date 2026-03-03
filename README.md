# ⚛️ Quantum-Lab-K8s: Scalable Quantum Simulation Environment

A containerized Quantum Computing Lab built with Python (Streamlit/Qiskit) and orchestrated via a self-healing Kubernetes cluster. This project demonstrates advanced local DevOps workflows, specifically handling image injection and networking in a `kind` (Kubernetes-in-Docker) environment on Apple Silicon.

## 🏗️ Architecture Summary
The deployment consists of three identical "worker" pods that simulate quantum circuits. Kubernetes ensures high availability by monitoring pod health and managing traffic via a LoadBalancer-style Service.

- **Orchestration:** Kubernetes (`kind`)
- **Replica Count:** 3 (Load-balanced)
- **Networking:** NodePort Service with local Port-Forwarding
- **Self-Healing:** Liveness probes ensure the Streamlit server is responsive.



---

## 🚀 Deployment Guide

### 1. Build the Image
To ensure compatibility with the `kind` cluster runtime, build the image locally:
```bash
docker build -t quantum-lab:v1 .
