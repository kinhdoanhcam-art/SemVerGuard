# SemVerGuard v1.1 — Runtime Evidence

## Status

`PASS` for fresh deployment, source parity, authorization, natural `NON_BREAKING` consensus, natural `BREAKING` consensus and deterministic activation enforcement. `FINALIZED` was not treated as success: every PASS below also records the observed execution result and post-state.

## Deployment

- Network: StudioNet 61999, API v0.2
- Contract: `0xBCD6E7c030d58a9B9B5C13FB8306f977ad9bf960`
- Deploy tx: `0xdf64363b2377f4351bc359aa0cdf027bbed3bc8bd1b921fcaab13386d8374fbb`
- Deployer/maintainer: `0x3065E31B1D993d7C0D59E6786844cBa56780B2d3`
- Explorer: https://explorer-studio.genlayer.com/address/0xBCD6E7c030d58a9B9B5C13FB8306f977ad9bf960
- Frozen normalized source SHA-256: `bcb38cc46512ead09f762368070f7c2389c1f80aa8dfb4b74549f3a9e56996ad`
- RPC raw deployed-source SHA-256: `1b290fd96ad74859d815a21774d732b47621b523c1394ae37b0d722ab2305d27`
- RPC deployed-source SHA-256 after CRLF→LF: `bcb38cc46512ead09f762368070f7c2389c1f80aa8dfb4b74549f3a9e56996ad`
- Source parity: `PASS` — normalization was limited to line endings
- `get_config()` confirmed v1.1, immutable single maintainer and `pending_can_be_cancelled = false`

## Transaction evidence

| Case | Full transaction hash | Observed execution | Verified post-state | Status |
|---|---|---|---|---|
| N5a outsider `propose_change` | `0x6fff121d6371d52623c16f3fe77e64aa86f8d9279d04593c5465b87d1c7c05e8` | ERROR `Only maintainer` | Version 1.0; pending empty | PASS |
| N5b outsider `activate_pending(1,1)` | `0xef49aa0280195ff85e9bd5d171cccea93d0d5a1171103c3865ad5f0bea262908` | ERROR `Only maintainer` | Pending empty | PASS |
| N1 wording-only proposal | `0x24babc81f066d6755b144fd9540fc044e90407bbc04cf05bed1fce70971b326f` | SUCCESS; consensus `NON_BREAKING` | Version 1.0; proposal pending | PASS |
| N3 invalid NB activation `(2,0)` | `0x862d832762ea2d414eb3ff4100e4b6e42d2efab2be42803954a50cce0790063c` | ERROR `Non-breaking change must keep major version` | N1 remains pending unchanged | PASS |
| N2 valid NB activation `(1,1)` | `0xc2dd58ab1aab5d31413e1b6529b71e54e4a3bb021771ccdb7ff4c65cf24c355f` | SUCCESS | Version 1.1; pending empty | PASS |
| N4 optional-label proposal | `0xd277437edbb8763a8dc93208068a95eb53adaeab18ac323d1a3cc72b35f86969` | SUCCESS; consensus `NON_BREAKING` | Version 1.1; proposal pending | PASS |
| N4b valid NB activation `(1,2)` | `0x3a52a8badd0f1c45f590878e15309b6fec5ca983d908bd6ad3a822453f44bb14` | SUCCESS | Version 1.2; pending empty | PASS |
| Breaking required-token proposal | `0xdd6c1d3fdcc6343b1bff46db826ae75dccc8a507b9b0dab1d522b39e3dcb38a9` | SUCCESS; consensus `BREAKING` | Version 1.2; proposal pending | PASS |
| Invalid breaking activation `(1,3)` | `0xb4a8e91d105ce793e059945f47a0d8ba3185c1ff436b584da67a666b4c7119a8` | ERROR `Breaking change requires major version bump` | Breaking proposal remains pending | PASS |
| Invalid breaking activation `(2,1)` | `0x611eb1b82c1007648527ee9e406d9e77d7a6f709d56fc78a151b46696e321b6d` | ERROR `Breaking release must start at minor 0` | Breaking proposal remains pending | PASS |
| Valid breaking activation `(2,0)` | `0xc1cf7bb02a3ca7f1294729c6617e60e1248fc52f5a683e3927a9519419ace8f9` | FINALIZED + SUCCESS | Version 2.0; `last_classification=BREAKING`; pending empty | PASS |

The Studio/Explorer records showed consensus `Accepted`; successful calls showed GenVM `SUCCESS`, while expected rollback cases showed the exact errors above. Postconditions were read through `get_pending()` and `get_summary()` after finalization.

## Not run / not claimed

- 500-character `propose_change` gas probe: `NOT RUN`
- 1,500-character `propose_change` gas probe: `NOT RUN`
- 3,000-character `propose_change` gas probe: `NOT RUN`
- Real Direct Mode load-bearing suite: `NOT RUN`
- GenVM/static lint tool: `NOT RUN`

Local Python stub suite: `PASS — 11/11`; this is deterministic unit evidence, not a substitute for the StudioNet records above.
