# SemVerGuard v1.1

**Single-maintainer Intelligent Contract:** the wallet that deploys an instance is its permanent maintainer. Only that wallet can call either write method. A reviewer who wants to exercise the write flow must deploy a separate instance with their own `initial_spec`.

SemVerGuard uses GenLayer semantic consensus to classify a proposed behavioral specification as `BREAKING` or `NON_BREAKING`, then deterministically restricts the version numbers with which that exact proposal may be activated.

## Why it exists

A syntactic diff cannot always determine whether behavior remains backward compatible. For example, an API may change from retrying a failed webhook once to retrying indefinitely. The method signature is unchanged, but consumers relying on a bounded number of deliveries may break.

The semantic verdict is load-bearing:

- `BREAKING` requires `new_major > current_major` and `new_minor == 0`;
- `NON_BREAKING` requires `new_major == current_major` and `new_minor > current_minor`.

The model never sees or chooses the version number. The contract owns authorization, pending state, hash binding and version enforcement.

## Fixed v1.1 invariants

- Malformed, non-object or out-of-schema model output aborts with `Invalid semantic output`; no verdict, cache entry or pending state is manufactured.
- Prompt fences and verdict literals are removed to a fixed point, then whitespace is normalized.
- The cache key hashes the exact canonical active/proposed pair shown to the model, using length-prefixed concatenation.
- The original proposed text remains in `pending_spec`.
- `activate_pending()` recomputes and verifies `pending_hash` before any activation write.
- `activate_pending()` accepts only `new_major` and `new_minor`; it never accepts replacement specification text.
- A classified pending proposal cannot be cancelled or replaced. The maintainer must activate it with a valid version before proposing another change.

The final rule is deliberate. It prevents repeated model calls until a preferred verdict appears. There is no `cancel_pending()`, withdrawal or timeout.

## Lifecycle

1. The maintainer calls `propose_change(proposed_spec)`.
2. The contract canonicalizes the active/proposed pair for both model input and cache hashing.
3. GenLayer validators return one closed-schema verdict.
4. The contract stores the original proposal, its canonical pair hash and classification as pending.
5. The maintainer calls `activate_pending(new_major, new_minor)`.
6. The contract verifies the pending hash and applies the verdict-specific SemVer rules.
7. A valid activation makes the pending specification active and clears pending state.

## Public methods

### Writes

- `propose_change(proposed_spec: str)` — maintainer only; classifies and stores one pending proposal.
- `activate_pending(new_major: int, new_minor: int)` — maintainer only; verifies the stored hash and activates only a verdict-compatible version.

### Views

- `get_config()` — returns v1.1 configuration, verdict values, specification bounds, maintainer address and the explicit no-cancellation policy.
- `get_summary()` — returns active version/specification and pending summary.
- `get_pending()` — returns the current pending classification and specification.

## How to try it

1. Open GenLayer Studio on **StudioNet, chain ID 61999, API v0.2**.
2. Deploy `SemVerGuard.py` from the wallet that will act as maintainer.
3. Supply the `initial_spec` from `TESTING.md` or another specification of 20–4,000 characters.
4. Record the new address, deployment transaction and normalized source SHA-256.
5. Run the N1–N5 flow in `TESTING.md`, one critical state-changing transaction at a time.
6. For every transaction, verify the authoritative leader execution result and the exact post-state. `FINALIZED` alone is not success.

## Honest limitations

- The contract classifies the declared specifications; it does not prove that deployed software or source code implements either specification.
- Each deployment is single-tenant and has one immutable maintainer wallet.
- A classified pending proposal cannot be cancelled. A maintainer who does not want to activate it cannot submit another proposal on that instance.
- Semantic classification depends on GenLayer consensus and may conservatively return `BREAKING` when compatibility is meaningfully ambiguous.
- There is no native GEN transfer, external URL, or clock-dependent logic.

## Deployment status

- Network: StudioNet 61999
- Contract address: `0xBCD6E7c030d58a9B9B5C13FB8306f977ad9bf960`
- Deploy transaction: `0xdf64363b2377f4351bc359aa0cdf027bbed3bc8bd1b921fcaab13386d8374fbb`
- Maintainer: `0x3065E31B1D993d7C0D59E6786844cBa56780B2d3`
- Source parity: `PASS` — deployed source equals the frozen source after CRLF→LF normalization
- Runtime authorization, NON_BREAKING and BREAKING flows: `PASS`
- Explorer: https://explorer-studio.genlayer.com/address/0xBCD6E7c030d58a9B9B5C13FB8306f977ad9bf960
- GitHub: https://github.com/kinhdoanhcam-art/SemVerGuard

## Verification status

Local stub-backed tests exercise deterministic state behavior, both verdict branches, malformed-output rollback, canonical cache identity, authorization and pending-hash integrity. StudioNet evidence covers live semantic consensus, authorization and deterministic activation rules. Real Direct Mode, gas probes and GenVM/static lint remain `NOT RUN` and are not claimed.

The submission root intentionally contains only the contract and the two primary guides. Supporting evidence, checksums, security notes and unit-test code are grouped under `supporting/`; see `supporting/README.md` for the index.
