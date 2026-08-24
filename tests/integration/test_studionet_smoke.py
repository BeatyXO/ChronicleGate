"""
Optional hosted-Studio smoke test.

Run only after deploying ChronicleGate and setting CHRONICLE_GATE_ADDRESS.
This file intentionally does not create or fund accounts and is skipped by default.
"""
import os
import pytest

ADDRESS = os.getenv("CHRONICLE_GATE_ADDRESS", "")


@pytest.mark.skipif(not ADDRESS, reason="set CHRONICLE_GATE_ADDRESS to run hosted integration smoke test")
def test_studionet_address_is_configured():
    assert ADDRESS.startswith("0x")
    assert len(ADDRESS) == 42
