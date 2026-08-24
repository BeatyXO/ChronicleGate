# Deployment evidence

## Current status

No canonical Studionet deployment is recorded for this checkout. `CHRONICLE_GATE_ADDRESS` is not committed and the integration test is opt-in, so this repository does not claim a live address, transaction hash, finality, or runtime smoke-test result.

The earlier deployment is historical because the contract source subsequently changed to accept CLI-native URI arrays. A fresh deployment is required before current-source runtime evidence can be claimed.

## Reproducible deployment checklist

Deploy the exact `contracts/chronicle_gate.py` from the commit being submitted with the official GenLayer Studio/CLI tooling. Record the public contract address, deployment transaction, receipt lifecycle, consensus result, and the source commit here. Do not commit credentials.

After deployment, run the integration suite with:

```text
CHRONICLE_GATE_ADDRESS=0x... gltest tests/integration -v --network studionet
```

The canonical deployment must be kept separate from disposable integration deployments. If the contract source changes after deployment, the old deployment is historical evidence and must not be described as current-source proof.

## Local evidence

- Preflight: PASS (required files, AST, consensus primitives, and fail-closed states).
- Direct Mode: 28 passed (28 collected).
- GenVM linter: `genvm-linter 0.11.0`; lint passed. The full `check` command was attempted; SDK validation did not complete in this environment and is not claimed as passed.
- Studionet: not run; no address was configured.
