# Consensus Design

## Stable decision field

The state-changing field is:

```text
relation
```

Allowed values:

```text
A_BEFORE_B
B_BEFORE_A
SAME_EVENT_WINDOW
ORDER_NOT_PROVABLE
EXTERNAL_FAILURE
```

## Leader work

The leader:

1. renders every registered evidence source for event A,
2. renders every registered evidence source for event B,
3. supplies the immutable definitions plus source content to the LLM,
4. returns a structured relation, supported occurrence strings, and a short reason.

## Validator work

Validators do not validate only shape or enum membership.

Each validator independently executes the same evidence-reading and semantic-classification function, producing its own candidate relation.

The custom validator then requires:

```python
leader_relation == validator_relation
```

This is deliberate field-level equivalence.

### Why not compare full JSON?

Reason text is subjective. Even the best supported occurrence representation can vary harmlessly:

```text
2026-08-20
2026-08-20T00:00:00Z
2026-08-20 (day precision)
```

Requiring byte equality would turn harmless representational differences into consensus failures.

### Why relation equality is sufficient

The relation enum is the only field that changes downstream authorization through `can_import`.

The validator independently recomputes that field from source evidence, so the leader cannot set it unilaterally.

## Fail-closed cases

### Evidence unavailable

The nondeterministic function returns:

Only `relation` is consensus-bound and authoritative. Stored `leader_a_occurrence`, `leader_b_occurrence`, and `leader_reason` are bounded informational leader output and must not be used as certified facts. Caller-controlled titles, subjects, definitions, comparison context, and source content are JSON data values, never instructions.

```text
EXTERNAL_FAILURE
```

If validators can fetch successfully while the leader cannot, their independently computed relations differ and the leader result is rejected.

### Evidence ambiguous

The model is instructed to return:

```text
ORDER_NOT_PROVABLE
```

when:

- one event is not established,
- timestamps are too coarse,
- evidence conflicts materially,
- ordering requires speculation.

### Invalid model output

Unknown relation enums deterministically normalize to `ORDER_NOT_PROVABLE`.

## Prompt-injection boundary

Evidence is explicitly marked as untrusted data. The adjudication prompt tells the model to ignore instructions embedded in source content.

This cannot make arbitrary web content perfectly safe, but it narrows the model's role and prevents fetched pages from becoming authoritative instruction sources by design.
