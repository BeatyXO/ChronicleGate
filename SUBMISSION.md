# Submission Notes

## Category

Standalone GenLayer Intelligent Contract / reusable contract primitive.

## One-line description

ChronicleGate is a reusable semantic event-ordering primitive that lets GenLayer validators independently inspect public evidence and establish whether event A occurred before event B under explicit natural-language occurrence definitions.

## Why it is not a thin LLM wrapper

- Registered event definitions and sources become durable contract state.
- Validators independently rerun the evidence-reading and semantic-classification work.
- Consensus compares the state-changing relation enum.
- Inconclusive and external-failure states are explicit and non-authorizing.
- Downstream contracts import the result through `can_import`.
- A callback interface demonstrates contract-to-contract composition.
- Input bounds, replay protection, retry semantics, and source-failure handling are part of the state machine.

## Reviewer walkthrough

1. Read `contracts/chronicle_gate.py`.
2. Read `docs/CONSENSUS.md`.
3. Run `python scripts/preflight.py`.
4. Run `pytest tests/direct -v`.
5. Review `examples/release_sequence_guard.py`.
6. Deploy to StudioNet for a live two-event ordering test and record the explorer address here before final submission.

## Live deployment

Not recorded in this repository until a real deployment has been performed and verified. Do not replace this section with a fabricated address.
## Submission status

- Category: standalone Intelligent Contract
- Primitive: ChronicleGate — consensus-based semantic event ordering
- Repository: https://github.com/BeatyXO/ChronicleGate
- Canonical Studionet address: not yet deployed in this checkout
- Deployment transaction/source parity/live runtime proof: not claimed
- Local evidence: preflight PASS; Direct Mode 17/17; `genvm-linter 0.10.0` lint and validation PASS

ChronicleGate uses GenLayer consensus because validators must independently inspect public evidence and apply natural-language occurrence definitions. The leader proposes a bounded relation enum and each validator independently re-fetches and classifies the evidence; disagreement prevents a trusted terminal ordering. Deterministic code owns bounds, parsing, state transitions, retry/replay protection, import gating, and persistence.

The primitive is reusable through `register_event`, `open_relation`, `resolve_relation`, `retry_unresolved`, and the stable `can_import` view. It fails closed to retryable `ORDER_NOT_PROVABLE` or `EXTERNAL_FAILURE` when ordering cannot safely be established. Limitations include dependence on public source availability, model interpretation, and the usual malicious-validator-majority assumption.

See `docs/CONSENSUS.md`, `docs/SECURITY.md`, `docs/INTEGRATION.md`, and `docs/DEPLOYMENT.md` for the reviewer fast path.
