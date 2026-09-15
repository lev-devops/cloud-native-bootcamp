# Security

Do not commit credentials, private keys, kubeconfigs, tokens, `.env` files, Terraform state, or private network details. The bootstrap wizard uses existing SSH configuration and never accepts passwords or key contents. Review the printed plan before using `--apply`.
