# SemVerGuard v1.1 — Submission Note

## Title

**SemVerGuard — Semantic Compatibility With Deterministic Version Enforcement**

## Submission note

SemVerGuard is a single-maintainer GenLayer Intelligent Contract that classifies behavioral specification changes as `BREAKING` or `NON_BREAKING`, then deterministically restricts the valid version transition. A breaking proposal requires a higher major version starting at minor 0; a non-breaking proposal must retain the major version and increase the minor version. Validators see only the canonical active/proposed specification pair, never the proposed version. The original pending text is stored, its canonical pair hash is verified again during activation, and malformed semantic output aborts without creating or caching a verdict. A classified proposal cannot be cancelled, preventing verdict grinding through repeated withdrawal and resubmission.

## Release fields

- Contract: `0xBCD6E7c030d58a9B9B5C13FB8306f977ad9bf960`
- Deploy tx: `0xdf64363b2377f4351bc359aa0cdf027bbed3bc8bd1b921fcaab13386d8374fbb`
- Explorer: https://explorer-studio.genlayer.com/address/0xBCD6E7c030d58a9B9B5C13FB8306f977ad9bf960
- GitHub: https://github.com/kinhdoanhcam-art/SemVerGuard
- Normalized source SHA-256: see `SOURCE_SHA256.txt`
- Runtime evidence: `PASS` for deployment, parity, authorization, both semantic verdict branches and deterministic version enforcement; see `RUNTIME_EVIDENCE.md`

Gas probes, real Direct Mode and GenVM/static lint remain explicitly `NOT RUN` and are not claimed.
