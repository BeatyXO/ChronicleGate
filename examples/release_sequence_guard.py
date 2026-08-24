# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *


@gl.contract_interface
class IChronicleGate:
    class View:
        def can_import(self, relation_id: u256, expected_relation: str) -> bool:
            pass

    class Write:
        pass


class ReleaseSequenceGuard(gl.Contract):
    chronicle_gate: Address
    required_relation: str

    def __init__(self, chronicle_gate: Address) -> None:
        self.chronicle_gate = chronicle_gate
        self.required_relation = "A_BEFORE_B"

    @gl.public.view
    def sequence_is_valid(self, relation_id: u256) -> bool:
        gate = gl.get_contract_at(self.chronicle_gate, IChronicleGate)
        return gate.can_import(relation_id, self.required_relation)
