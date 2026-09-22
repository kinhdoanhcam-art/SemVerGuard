# Supporting files

The submission root is kept intentionally small. These files provide audit, runtime and maintenance evidence:

- `RUNTIME_EVIDENCE.md` — StudioNet deployment, transaction hashes and verified post-state.
- `SOURCE_SHA256.txt` and `FINAL_CHECKSUMS.txt` — source parity and package integrity.
- `LOCKED_SPEC.md` and `BLIND_RUNTIME_PROTOCOL.md` — frozen requirements and execution protocol.
- `SECURITY.md` and `CHANGELOG.md` — security notes and release history.
- `SUBMISSION_NOTE.md` — concise release metadata.
- `tests/` — local deterministic unit suite.
- `snapshots/` — optional runtime screenshots, if a submission portal requires them.

None of these files changes the deployed contract logic in `../SemVerGuard.py`.
