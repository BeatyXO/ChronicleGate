# ChronicleGate

**Consensus-based semantic event ordering for GenLayer.**

ChronicleGate is a standalone, reusable Intelligent Contract primitive. It answers a narrow but difficult question for downstream contracts:

> **Given two precisely defined real-world events and public evidence for each, which event occurred first?**

There is **no frontend** in this repository. ChronicleGate is intended to be imported by other contracts and protocols through a small read interface.

## Why this primitive exists

## Verification status

This checkout has no canonical Studionet deployment yet. The verified local gates are Direct Mode 17/17, preflight PASS, and `genvm-linter 0.10.0` lint + validation PASS. Live address, transaction, finality, and runtime claims are intentionally omitted until a deployment is actually performed.

Traditional smart contracts can compare two timestamps only after somebody has already decided what those timestamps mean.

Real evidence is messier:

- a release can be announced before it is actually downloadable,
- a governance proposal can be posted before its required notice becomes effective,
- a shipment can be scanned before custody is actually transferred,
- an incident can be detected before it is publicly acknowledged,
- a document can be uploaded before it is formally published.

ChronicleGate lets each event define **what counts as occurrence**, then asks GenLayer validators to independently inspect public evidence and determine the semantic ordering.

## Verdicts

A relation resolves to one of:

| Verdict | Meaning |
| --- | --- |
| `A_BEFORE_B` | Event A is supported as occurring before event B. |
| `B_BEFORE_A` | Event B is supported as occurring before event A. |
| `SAME_EVENT_WINDOW` | The best supported occurrence windows overlap, so neither strict order is truthful. |
| `ORDER_NOT_PROVABLE` | Evidence is insufficient, ambiguous, conflicting, or too coarse to establish the order. |
| `EXTERNAL_FAILURE` | One or more evidence sources could not be read. |

Only the first three are terminal importable outcomes. `ORDER_NOT_PROVABLE` and `EXTERNAL_FAILURE` remain retryable.

## What makes it GenLayer-native

ChronicleGate uses GenLayer for the part deterministic code cannot safely do: interpreting whether public evidence satisfies a natural-language occurrence definition.

`resolve_relation` performs a real consensus flow:

1. The leader independently renders the registered evidence URLs for event A and event B.
2. The leader's LLM derives a bounded structured result.
3. Each validator independently re-fetches the same evidence and independently derives its own result.
4. The validator compares the stable **relation enum** with the leader's relation.
5. State is updated only from the consensus-accepted result.

The explanation and timestamp precision are deliberately excluded from equality because independent validators can phrase the same conclusion differently. The on-chain consequence depends on the stable semantic relationship.

This is not a format-only validator and not a thin LLM wrapper: validators reproduce the evidence-reading and classification work themselves.

## State design

### Event

An event is immutable after registration.

```text
Event
├── id
├── title
├── subject
├── occurrence_definition
├── evidence_uris[]
├── creator
├── status
└── created_at
```

The `occurrence_definition` is the key semantic boundary. It defines what the contract means by "this event happened."

### Relation

```text
Relation
├── id
├── event_a
├── event_b
├── comparison_context
├── callback
├── status
├── relation
├── a_occurrence
├── b_occurrence
├── reason
├── opened_by
├── created_at
├── resolved_at
└── callback_sent
```

Events remain immutable so a resolved ordering cannot silently change because a claimant later edits the definition or source list.

## Contract API

### `register_event`

```python
register_event(
    title: str,
    subject: str,
    occurrence_definition: str,
    evidence_uris_json: str,
) -> u256
```

`evidence_uris_json` must be a JSON array containing 1-4 HTTP(S) URLs.

Example:

```json
[
  "https://example.org/release-notes",
  "https://example.org/downloads"
]
```

### `open_relation`

```python
open_relation(
    event_a: u256,
    event_b: u256,
    comparison_context: str,
    callback: Address,
) -> u256
```

Use the zero address if no callback is needed.

### `resolve_relation`

```python
resolve_relation(relation_id: u256) -> None
```

Runs the nondeterministic evidence + LLM flow and GenLayer consensus.

### `retry_unresolved`

```python
retry_unresolved(relation_id: u256) -> None
```

Reopens only `INCONCLUSIVE` or `EXTERNAL_FAILURE` relations.

### `can_import`

```python
can_import(relation_id: u256, expected_relation: str) -> bool
```

This is the main consumer surface. It returns `True` only when the relation is terminally `RESOLVED` and exactly matches the expected importable verdict.

### Read methods

```python
event_of(event_id: u256) -> str
relation_of(relation_id: u256) -> str
stats() -> str
```

Records are returned as JSON strings.

## Example use case

Suppose a release policy says:

> A production build must be publicly downloadable before the official launch announcement.

Register:

**Event A**

```text
definition = "The event occurs when a production build is publicly downloadable."
```

**Event B**

```text
definition = "The event occurs when the official public announcement is published."
```

After resolution, a consumer contract can require:

```python
gate.can_import(relation_id, "A_BEFORE_B")
```

See [`examples/release_sequence_guard.py`](examples/release_sequence_guard.py).

## Fail-closed behavior

ChronicleGate deliberately avoids manufacturing certainty.

- Invalid model enums normalize to `ORDER_NOT_PROVABLE`.
- Unreadable evidence becomes `EXTERNAL_FAILURE`.
- Conflicting or semantically insufficient evidence should become `ORDER_NOT_PROVABLE`.
- `ORDER_NOT_PROVABLE` cannot be imported as a successful order.
- `EXTERNAL_FAILURE` cannot be imported as a successful order.
- Resolved relations cannot be replayed or retried.
- Evidence content is explicitly treated as untrusted data to reduce prompt-injection risk.

## Repository structure

```text
ChronicleGate/
├── contracts/
│   └── chronicle_gate.py
├── examples/
│   └── release_sequence_guard.py
├── tests/
│   ├── direct/
│   │   ├── conftest.py
│   │   └── test_chronicle_gate.py
│   └── integration/
│       └── test_studionet_smoke.py
├── docs/
│   ├── ARCHITECTURE.md
│   ├── CONSENSUS.md
│   ├── INTEGRATION.md
│   ├── DEPLOYMENT.md
│   └── SECURITY.md
├── scripts/
│   └── preflight.py
├── gltest.config.yaml
├── requirements.txt
└── LICENSE
```

## Testing

Requires Python 3.12+.

```bash
python -m pip install -r requirements.txt
pytest tests/direct -v
```

The Direct Mode suite covers registration, input bounds, relation lifecycle, all terminal verdicts, retry paths, replay protection, fail-closed model handling, import behavior, and counters.

Run the local preflight:

```bash
python scripts/preflight.py
```

For hosted/full-network validation, deploy the contract first and set:

```bash
CHRONICLE_GATE_ADDRESS=0x...
```

Then:

```bash
gltest tests/integration -v --network studionet
```

The integration smoke test is intentionally opt-in and does not fabricate a deployment address.

## Design boundaries

ChronicleGate does **not**:

- decide whether an event is morally good or bad,
- assign reputation,
- settle escrow,
- decide whether a generic claim is true,
- act as a general-purpose oracle,
- accept a timestamp simply because a source contains one.

Its sole primitive is:

> **semantic temporal ordering under explicit event definitions and independently inspected public evidence.**

That narrow boundary is what makes it reusable.

## License

MIT.
