# Security Notes

## Trust model

ChronicleGate does not trust:

- the relation opener,
- the leader validator,
- model prose,
- fetched page instructions,
- an isolated timestamp without semantic support.

Its security goal is narrower: multiple validators should independently converge on the same bounded temporal relation from the registered evidence and occurrence definitions.

## Threats and mitigations

### Prompt injection in evidence

**Threat:** a fetched page contains instructions intended for the model.

**Mitigation:** the prompt explicitly declares evidence as untrusted data and tells the model to ignore embedded instructions.

### Leader fabrication

**Threat:** the leader invents a relation.

**Mitigation:** validators independently fetch and classify the evidence. Consensus compares their independently produced relation enum with the leader's.

### False precision

**Threat:** an LLM invents an exact time from coarse evidence.

**Mitigation:** the prompt requires the most precise supported time/window and directs the model to use `ORDER_NOT_PROVABLE` when ordering requires unsupported precision. Timestamp strings are informational; only the relation enum authorizes consumers.

### External source outage

**Threat:** evidence becomes temporarily unreadable.

**Mitigation:** the state becomes `EXTERNAL_FAILURE`, which cannot be imported and can be retried.

### Ambiguous evidence

**Threat:** sources disagree or do not establish an event definition.

**Mitigation:** `ORDER_NOT_PROVABLE` is fail-closed and retryable.

### Replay

**Threat:** a terminal relation is resolved again.

**Mitigation:** `resolve_relation` accepts only `OPEN`.

### Oversized evidence

**Threat:** excessive source sets inflate consensus work.

**Mitigation:** 1-4 HTTP(S) URLs per event and per-source content truncation.

## Known limitations

- Public web evidence can change after a relation resolves. ChronicleGate stores the registered URIs and accepted result, not a cryptographic snapshot of every fetched byte.
- Semantic adjudication can remain inconclusive when evidence is weak.
- Callback delivery is best-effort.
- The contract does not authenticate the publisher behind a URL; consumers should choose evidence sources appropriate to their risk model.
## Callback finality and diagnostics

Callbacks use finalized delivery semantics. Only the consensus-bound `relation` is authoritative; `leader_a_occurrence`, `leader_b_occurrence`, and `leader_reason` are bounded informational diagnostics and must not be used as certified timestamps or settlement inputs.

## Limitations

Mutable web sources can change after resolution; validators may fail to converge; weak or conflicting evidence becomes inconclusive; publisher identity is not authenticated by ChronicleGate; consumers must choose appropriate sources; StudioNet behavior is not production-network assurance; and semantic judgments depend on validator/model quality.
