# SemVerGuard v1.1 — Testing

## Truth standard

`SUBMITTED ≠ ACCEPTED ≠ FINALIZED ≠ EXECUTION SUCCESS ≠ POSTCONDITION PASS`

No StudioNet case below is marked PASS until its full transaction hash, authoritative leader execution result and exact post-state are recorded in `supporting/RUNTIME_EVIDENCE.md`.

## Local deterministic tests

Run from the repository root:

```text
py -3 -m unittest discover -s supporting/tests -v
```

Fallback:

```text
python -m unittest discover -s supporting/tests -v
```

These tests use a local GenLayer stub. They check contract state logic but are not GenVM, Direct Mode or StudioNet proof.

Executed on 2026-09-22 with Python 3.12.14: `PASS — 11/11 tests`. `python3 -m py_compile SemVerGuard.py supporting/tests/test_semverguard_v1_1.py` also passed.

## Fresh deployment setup

- Network: StudioNet
- Chain ID: `61999`
- API: `v0.2`
- Contract address: `0xBCD6E7c030d58a9B9B5C13FB8306f977ad9bf960`
- Maintainer: `0x3065E31B1D993d7C0D59E6786844cBa56780B2d3`
- Outsider: `0xdaE8968571C6E84f44F86d06F1071bbc8F807500`

Constructor `initial_spec`:

```text
The scheduler accepts a task identifier and an ISO 8601 UTC timestamp. It queues each valid task for one execution at or after that timestamp. Invalid timestamps are rejected with an error.
```

Initial version: `1.0`.

## Runtime execution order

Use one critical transaction at a time. Stop on any mismatch. The practical order is N5 → N1 → N3 → N2 → N4 → N4b so the invalid NON_BREAKING major activation is attempted before N2 clears the pending proposal.

### N5a — outsider proposes

- Wallet: outsider
- Method: `propose_change`
- Parameter: the N1 proposal below
- Expected execution: rollback `Only maintainer`
- Expected post-state: version `1.0`, `has_pending = false`, empty cache for this pair
- Status: `PASS`
- CẦN SNAP: `KHÔNG CẦN`, unless result differs

### N5b — outsider activates

- Wallet: outsider
- Method: `activate_pending(1, 1)`
- Expected execution: rollback `Only maintainer`
- Expected post-state: unchanged
- Status: `PASS`
- CẦN SNAP: `KHÔNG CẦN`, unless result differs

### N1 — wording-only proposal

- Wallet: maintainer
- Method: `propose_change`
- Parameter:

```text
A task identifier together with a valid ISO 8601 UTC timestamp is accepted by the scheduler. Every valid task is queued to execute once, no earlier than that timestamp. The scheduler rejects an invalid timestamp with an error.
```

- Category: pure wording cleanup/clarification; not `units or meaning of returned values`
- Expected verdict: `NON_BREAKING`
- Expected post-state: version stays `1.0`, `has_pending = true`, `pending_classification = NON_BREAKING`
- Status: `PASS`
- CẦN SNAP: `CÓ` — first natural NON_BREAKING consensus checkpoint

### N3 — reject a major bump for NON_BREAKING

- Wallet: maintainer
- Method: `activate_pending(2, 0)`
- Expected execution: rollback `Non-breaking change must keep major version`
- Expected post-state: version `1.0`; the N1 proposal remains pending and unchanged
- Status: `PASS`
- CẦN SNAP: `KHÔNG CẦN`, unless result differs

### N2 — activate the wording-only proposal

- Wallet: maintainer
- Method: `activate_pending(1, 1)`
- Expected execution: success
- Expected post-state: version `1.1`, N1 text becomes active, `has_pending = false`
- Status: `PASS`
- CẦN SNAP: `CÓ` — first successful NON_BREAKING activation

### N4 — compatible optional input

- Wallet: maintainer
- Method: `propose_change`
- Parameter:

```text
A task identifier together with a valid ISO 8601 UTC timestamp is accepted by the scheduler. Every valid task is queued to execute once, no earlier than that timestamp. The scheduler rejects an invalid timestamp with an error. A client may additionally provide an optional display label; omitting the label preserves every existing request, result, and error behavior.
```

- Category: compatible addition to accepted input semantics; not `units or meaning of returned values`
- Expected verdict: `NON_BREAKING`
- Expected post-state: version stays `1.1`, `has_pending = true`, `pending_classification = NON_BREAKING`
- Status: `PASS`
- CẦN SNAP: `CÓ` — second natural NON_BREAKING form

### N4b — activate the compatible addition

- Wallet: maintainer
- Method: `activate_pending(1, 2)`
- Expected execution: success
- Expected post-state: version `1.2`, N4 text becomes active, `has_pending = false`
- Status: `PASS`
- CẦN SNAP: `KHÔNG CẦN`, unless result differs

## Additional BREAKING branch

After N4b, the maintainer proposed a specification requiring a mandatory authorization token. Natural consensus classified it `BREAKING`. Two invalid activations preserved the pending proposal: `(1, 3)` rolled back with `Breaking change requires major version bump`, and `(2, 1)` rolled back with `Breaking release must start at minor 0`. Activation `(2, 0)` then succeeded; the final version is `2.0`, `last_classification = BREAKING`, and pending state is empty. Status: `PASS`.

## Additional required gates

| Gate | Required evidence | Status |
|---|---|---|
| Fresh deployment | Address, deploy tx and source | `PASS` |
| Source parity | Only CRLF/LF normalization; matching SHA-256 | `PASS` |
| Natural semantic consensus | NON_BREAKING and BREAKING proposals after source freeze | `PASS` |
| Authorization | N5a and N5b rollback plus unchanged state | `PASS` |
| Gas probes | `propose_change` at 500 / 1,500 / 3,000 characters | `NOT RUN` |
| Explorer | Actual v1.1 deployment and transaction history | `PASS` |
| GenVM/static lint | Real tool output | `NOT RUN` |
| Direct Mode | Production contract load-bearing suite | `NOT RUN` |

## Runtime result template

```text
Case:
Wallet/role:
Method and exact parameters:
Full transaction hash:
Consensus status:
Leader execution result:
Observed return/error:
Pre-state:
Post-state:
Expected vs actual:
Status: PASS / FAIL
```
