# Local-first implementation plan

1. Inventory Mint HP k3s, Jenkins, Docker, storage, and resource limits.
2. Add a minimal Node.js health endpoint and tests.
3. Build and run the image with Docker Compose.
4. Package and deploy the app with Helm to a dedicated namespace.
5. Add Jenkins build/test/image/publish/deploy stages using a local registry.
6. Add Terraform and Ansible only where ownership is clear.
7. Add Prometheus metrics and a Python health/recovery utility.
8. Re-run validation and document rollback.
