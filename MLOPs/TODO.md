## Directory: MLOps_Production
## Topics that must be covered
- Version Control: Git (branching, merging, commits, PRs), DVC (Data Version Control for large datasets)
- Experiment Tracking: MLflow (Tracking metrics/params, Projects, Model Registry), Weights & Biases (wandb - sweeps, reports)
- Model Serialization: Saving models in ONNX (cross-platform), TorchScript (PyTorch JIT), TensorRT (NVIDIA optimization), OpenVINO (Intel optimization)
- API Development: Building REST APIs with FastAPI (async support) and Flask, GraphQL for complex queries
- Containerization: Writing Dockerfiles for reproducible training environments, Docker Compose for multi-service setups
- Orchestration: Kubernetes (Pods, Services, Ingress, Horizontal Pod Autoscaling) for scaling inference
- CI/CD for ML: GitHub Actions or GitLab CI for running tests, linting, and automated deployment to staging/production
- Feature Store: Feast, Tecton - for real-time feature computation and serving (online/offline stores)
- Model Monitoring: Detecting Data Drift (distribution changes) and Concept Drift (target changes), Performance alerts (accuracy drops), Logging with Prometheus/Grafana