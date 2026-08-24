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

print("ChronicleGate preflight: PASS")
print(f"- required files: {len(required_files)}/{len(required_files)}")
print("- contract AST: valid")
print("- consensus primitives: present")
print("- fail-closed states: present")
