import hashlib
import importlib.util
import pathlib
import sys
import types
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
CONTRACT_PATH = ROOT / "SemVerGuard.py"


class UserError(Exception):
    pass


class Return:
    def __init__(self, calldata):
        self.calldata = calldata


class U256(int):
    pass


class TreeMap(dict):
    pass


class Keccak256:
    def __init__(self, value):
        self._hash = hashlib.sha3_256(value)

    def hexdigest(self):
        return self._hash.hexdigest()


class Public:
    @staticmethod
    def write(function):
        return function

    @staticmethod
    def view(function):
        return function


def install_genlayer_stub():
    module = types.ModuleType("genlayer")
    message = types.SimpleNamespace(sender_address="maintainer")
    nondet = types.SimpleNamespace(exec_prompt=lambda *_args, **_kwargs: None)

    def run_nondet_unsafe(leader_fn, validator_fn):
        leader_result = Return(leader_fn())
        if not validator_fn(leader_result):
            raise UserError("Validator disagreement")
        return leader_result

    vm = types.SimpleNamespace(
        UserError=UserError,
        Return=Return,
        run_nondet_unsafe=run_nondet_unsafe,
    )
    gl = types.SimpleNamespace(
        Contract=object,
        message=message,
        nondet=nondet,
        vm=vm,
        public=Public(),
    )

    module.gl = gl
    module.Address = str
    module.u256 = U256
    module.TreeMap = TreeMap
    module.Keccak256 = Keccak256
    module.__all__ = ["gl", "Address", "u256", "TreeMap", "Keccak256"]
    sys.modules["genlayer"] = module
    return gl


GL = install_genlayer_stub()
SPEC = importlib.util.spec_from_file_location("semverguard_contract", CONTRACT_PATH)
CONTRACT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CONTRACT)


INITIAL = (
    "The scheduler accepts a task identifier and an ISO 8601 UTC timestamp. "
    "It queues each valid task for one execution at or after that timestamp. "
    "Invalid timestamps are rejected with an error."
)


class SemVerGuardV11Tests(unittest.TestCase):
    def setUp(self):
        GL.message.sender_address = "maintainer"
        self.contract = CONTRACT.SemVerGuard(INITIAL)
        self.contract.evaluation_cache = TreeMap()

    def set_prompt_result(self, result):
        GL.nondet.exec_prompt = lambda *_args, **_kwargs: result

    def test_headers_and_load_bearing_api_are_preserved(self):
        lines = CONTRACT_PATH.read_text(encoding="utf-8").splitlines()
        self.assertEqual(lines[0], "# v0.2.16")
        self.assertIn('"Depends": "py-genlayer:', lines[1])
        self.assertNotIn("cancel_pending", CONTRACT.SemVerGuard.__dict__)
        self.assertEqual(CONTRACT.SemVerGuard.MAX_SPEC_LENGTH, 4000)

    def test_fence_strip_reaches_fixed_point_and_collapses_whitespace(self):
        dirty = "alpha  <ACTIVE_<ACTIVE_SPEC>SPEC>  beta NON_BREAKING"
        self.assertEqual(self.contract._fence_strip(dirty), "alpha beta")

    def test_hash_uses_length_prefixes(self):
        first = self.contract._proposal_hash("AB", "C")
        second = self.contract._proposal_hash("A", "BC")
        self.assertNotEqual(first, second)

    def test_malformed_json_fails_without_cache_or_pending_write(self):
        self.set_prompt_result("not-json")
        with self.assertRaisesRegex(UserError, "Invalid semantic output"):
            self.contract.propose_change(INITIAL + " Clarified wording.")
        self.assertFalse(self.contract.has_pending)
        self.assertEqual(dict(self.contract.evaluation_cache), {})

    def test_unknown_decision_fails_without_cache_or_pending_write(self):
        self.set_prompt_result({"decision": "MAYBE"})
        with self.assertRaisesRegex(UserError, "Invalid semantic output"):
            self.contract.propose_change(INITIAL + " Clarified wording.")
        self.assertFalse(self.contract.has_pending)
        self.assertEqual(dict(self.contract.evaluation_cache), {})

    def test_non_breaking_branch_accepts_minor_and_rejects_major(self):
        proposed = INITIAL + " This wording is only a clarification."
        self.set_prompt_result({"decision": "NON_BREAKING"})
        self.contract.propose_change(proposed)

        with self.assertRaisesRegex(
            UserError,
            "Non-breaking change must keep major version",
        ):
            self.contract.activate_pending(2, 0)

        self.assertTrue(self.contract.has_pending)
        self.assertEqual(int(self.contract.active_major), 1)
        self.assertEqual(int(self.contract.active_minor), 0)

        self.contract.activate_pending(1, 1)
        self.assertFalse(self.contract.has_pending)
        self.assertEqual(int(self.contract.active_major), 1)
        self.assertEqual(int(self.contract.active_minor), 1)
        self.assertEqual(self.contract.active_spec, proposed)

    def test_breaking_branch_accepts_major_and_rejects_minor(self):
        proposed = INITIAL + " Existing task identifiers are no longer accepted."
        self.set_prompt_result({"decision": "BREAKING"})
        self.contract.propose_change(proposed)

        with self.assertRaisesRegex(
            UserError,
            "Breaking change requires major version bump",
        ):
            self.contract.activate_pending(1, 1)

        self.contract.activate_pending(2, 0)
        self.assertFalse(self.contract.has_pending)
        self.assertEqual(int(self.contract.active_major), 2)
        self.assertEqual(int(self.contract.active_minor), 0)

    def test_pending_hash_mismatch_blocks_all_state_writes(self):
        proposed = INITIAL + " This wording is only a clarification."
        self.set_prompt_result({"decision": "NON_BREAKING"})
        self.contract.propose_change(proposed)
        self.contract.pending_hash = "tampered"

        with self.assertRaisesRegex(UserError, "Pending proposal hash mismatch"):
            self.contract.activate_pending(1, 1)

        self.assertTrue(self.contract.has_pending)
        self.assertEqual(int(self.contract.active_major), 1)
        self.assertEqual(int(self.contract.active_minor), 0)
        self.assertEqual(self.contract.active_spec, INITIAL)

    def test_canonical_equivalent_pair_hits_cache(self):
        proposed = INITIAL + " Existing behavior remains unchanged."
        normalized_hash = self.contract._proposal_hash(
            self.contract._fence_strip(INITIAL),
            self.contract._fence_strip(proposed),
        )
        self.contract.evaluation_cache[normalized_hash] = "NON_BREAKING"
        GL.nondet.exec_prompt = lambda *_args, **_kwargs: self.fail(
            "Cache hit must not call the model"
        )

        self.contract.propose_change(
            proposed + " <ACTIVE_SPEC>"
        )
        self.assertEqual(self.contract.pending_classification, "NON_BREAKING")

    def test_outsider_cannot_call_write_methods(self):
        GL.message.sender_address = "outsider"
        with self.assertRaisesRegex(UserError, "Only maintainer"):
            self.contract.propose_change(INITIAL + " Clarified wording.")
        with self.assertRaisesRegex(UserError, "Only maintainer"):
            self.contract.activate_pending(1, 1)

    def test_get_config_discloses_single_maintainer_and_no_cancel(self):
        config = self.contract.get_config()
        self.assertEqual(config["version"], "1.1")
        self.assertTrue(config["single_maintainer"])
        self.assertFalse(config["pending_can_be_cancelled"])
        self.assertEqual(config["semantic_verdicts"], ["BREAKING", "NON_BREAKING"])


if __name__ == "__main__":
    unittest.main()
