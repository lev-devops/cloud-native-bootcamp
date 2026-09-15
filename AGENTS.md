# Project Instructions

## Boundaries

- Default target is local k3s on Mint HP.
- Do not run terraform apply, helm upgrade/install, kubectl delete, AWS commands, or production actions without explicit approval.
- Use terraform fmt/validate/plan, ansible-playbook --check, helm lint/template, and Jenkins dry-run or isolated jobs before mutation.
- Never commit kubeconfigs, cloud credentials, tokens, Terraform state, or generated secrets.

## Ownership

- Terraform owns declared infrastructure resources and namespaces.
- Ansible owns host packages and service configuration only.
- Helm owns application releases inside Kubernetes.
- Jenkins orchestrates checks and deployment but does not hide infrastructure ownership.

## Validation

- Validate locally before any remote or cloud work.
- Record assumptions, versions, resource limits, rollback, and observed results in docs/.

## Relevant skills

- terraform-iac
- kubernetes-sre
- cicd-engineer
- cloud-devops
- configure-codex-mise
- capsule-extractor (analysis-only when selecting change boundaries)
