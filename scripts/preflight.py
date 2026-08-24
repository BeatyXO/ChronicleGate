from pathlib import Path
import ast
import sys

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contracts" / "chronicle_gate.py"

required_files = [
    ROOT / "README.md",
    CONTRACT,
    ROOT / "docs" / "ARCHITECTURE.md",
    ROOT / "docs" / "CONSENSUS.md",
    ROOT / "docs" / "INTEGRATION.md",
    ROOT / "docs" / "SECURITY.md",
    ROOT / "docs" / "DEPLOYMENT.md",
    ROOT / "examples" / "release_sequence_guard.py",
    ROOT / "tests" / "direct" / "test_chronicle_gate.py",
    ROOT / "gltest.config.yaml",
]

errors = []

for path in required_files:
    if not path.exists():
        errors.append(f"missing: {path.relative_to(ROOT)}")

if CONTRACT.exists():
    source = CONTRACT.read_text(encoding="utf-8")
    try:
        ast.parse(source)
    except SyntaxError as exc:
        errors.append(f"contract syntax: {exc}")

    required_tokens = [
        "gl.vm.run_nondet_unsafe",
        "gl.nondet.web.render",
        "gl.nondet.exec_prompt",
        "def validator_fn",
        "def can_import",
        "ORDER_NOT_PROVABLE",
        "EXTERNAL_FAILURE",
    ]
    for token in required_tokens:
        if token not in source:
            errors.append(f"contract missing token: {token}")

    source_checks = [
        ("finalized callbacks", 'on="finalized"' in source),
        ("HTTPS URL admission", 'value.startswith("https://")' in source),
        ("diagnostic-only leader fields", 'leader_a_occurrence' in source and 'leader_reason' in source),
        ("bounded evidence sources", "MAX_EVIDENCE_URIS" in source),
        ("retry lifecycle", "retry_unresolved" in source),
        ("hostile-input prompt framing", "untrusted data values" in source),
    ]
    for label, passed in source_checks:
        if not passed:
            errors.append(f"source invariant missing: {label}")

    forbidden_tokens = [
        "strict_eq(leader_fn",
        "return True  # validator",
    ]
    for token in forbidden_tokens:
        if token in source:
            errors.append(f"suspicious validator pattern: {token}")

if errors:
    print("ChronicleGate preflight: FAIL")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

checks = [
    ("required files", f"{len(required_files)}/{len(required_files)}"),
    ("contract AST", "valid"),
    ("consensus primitives", "present"),
    ("source invariants", f"{len(source_checks)}/{len(source_checks)}"),
    ("fail-closed states", "present"),
]
print("ChronicleGate preflight: PASS")
for index, (label, result) in enumerate(checks, 1):
    print(f"{index}. PASS - {label}: {result}")
