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
