# ⚛️ Quantum-Lab-Project: Scalable Quantum Simulations on Kubernetes

This project demonstrates a containerized Quantum Simulation environment deployed on a self-healing **Kubernetes (kind)** cluster. It handles the complexities of local image orchestration and load-balanced service exposure.

## 🏗️ Architecture Overview
The application consists of a Python-based Quantum Lab (Streamlit) containerized via Docker and managed by a Kubernetes Deployment.

* **Replicas:** 3 Pods (ensuring high availability).
* **Self-Healing:** Integrated Liveness Probes to restart stalled simulations.
* **Orchestration:** Managed via `kind` (Kubernetes in Docker).
* **Load Balancing:** Service-level traffic distribution across worker nodes.



---

## 🚀 Getting Started

### 1. Prerequisites
* Docker Desktop
* `kubectl`
* `kind` (Kubernetes in Docker)

### 2. Build the Image
Build the image specifically for the local cluster environment:
```bash
docker build -t quantum-lab:v1 .
