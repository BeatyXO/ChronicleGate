# Integration Guide

ChronicleGate is designed to be consumed by other Intelligent Contracts.

## Polling integration

The smallest interface is:

```python
@gl.contract_interface
class IChronicleGate:
    class View:
        def can_import(self, relation_id: u256, expected_relation: str) -> bool:
            pass

    class Write:
        pass
```

Consumer:

```python
gate = gl.get_contract_at(chronicle_gate_address, IChronicleGate)

if not gate.can_import(relation_id, "A_BEFORE_B"):
    raise gl.vm.UserError("required sequence not established")
```

See `examples/release_sequence_guard.py`.

## Callback integration

`open_relation` also accepts a callback address.

When a relation reaches `RESOLVED`, ChronicleGate attempts:

```python
on_chronicle_relation(
    relation_id,
    event_a,
    event_b,
    relation,
)
```

The callback is best-effort. Callback failure does not invalidate the already-resolved ChronicleGate state. Consumers that require guaranteed observation should poll `can_import`.

## Recommended consumer pattern

1. Register immutable events.
2. Open a directed relation `(A, B)`.
3. Resolve it.
4. Check that status is `RESOLVED`.
5. Import exactly one expected relation using `can_import`.
6. Treat `INCONCLUSIVE` and `EXTERNAL_FAILURE` as non-authorizing states.

## Direction matters

`A_BEFORE_B` refers to the event IDs stored in the relation record.

Opening `(B, A)` is a distinct directed question.

## Zero callback

Use:

```text
0x0000000000000000000000000000000000000000
```

when no callback is required.
