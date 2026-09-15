# Contributing

Use Python 3.12 from `mise.toml`. Run the bootstrap tests before submitting changes:

```bash
python3 -m unittest discover -s scripts -p 'test_*.py' -v
```

Keep secrets, kubeconfigs, private host data, and generated state out of the repository. Record verified operational actions in `docs/runbook/events.jsonl` through `scripts/runbook.py`.
