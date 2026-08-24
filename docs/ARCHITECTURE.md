# Architecture

## Objective

ChronicleGate turns unstructured public evidence into a reusable temporal relation while keeping deterministic state transitions separate from nondeterministic interpretation.

## Components

### Immutable event registry

Each event stores:

- a human-readable title,
- a subject,
- a natural-language occurrence definition,
- one to four public HTTP(S) evidence URIs,
- creator metadata.

The definition and evidence list are immutable. A consumer that imports a relation therefore knows exactly which semantic boundary and which source set were adjudicated.

### Relation lifecycle

A relation has four lifecycle states:

```text
OPEN
├── RESOLVED
├── INCONCLUSIVE
└── EXTERNAL_FAILURE
```

`INCONCLUSIVE` and `EXTERNAL_FAILURE` may be reopened with `retry_unresolved`.

`RESOLVED` is terminal.

### Consumer boundary

Consumers should depend on:

```python
can_import(relation_id, expected_relation)
```

instead of parsing the stored reasoning.

Only `A_BEFORE_B`, `B_BEFORE_A`, and `SAME_EVENT_WINDOW` can be imported.

## Why TreeMap + JSON records

The contract uses a single `TreeMap[str, str]` and JSON-encoded records because:

1. event and relation schemas contain multiple fields,
2. record keys remain deterministic and easy to inspect,
3. downstream views can return a stable JSON representation,
4. the layout avoids proliferating parallel maps that can drift out of sync.

Counters are stored separately for inexpensive aggregate inspection.

## Temporal semantics

ChronicleGate distinguishes a source timestamp from an event occurrence.

A timestamp is evidence only if the source content establishes the event according to its registered definition.

Example:

```text
Source: "Launch announced at 10:00."
Definition: "Launch occurs when the production artifact becomes publicly downloadable."
```

That 10:00 announcement timestamp does not, by itself, establish the defined launch occurrence.

## Bounded evidence

Each event accepts at most four sources and each rendered source is truncated before being supplied to the model.

This bounds consensus cost and discourages "dump the whole internet into a prompt" designs.
