# SemVerGuard v1.1 — Blind Runtime Protocol

1. Freeze `SemVerGuard.py` and record its SHA-256 before creating final runtime vectors.
2. Deploy the exact frozen bytes to StudioNet 61999.
3. Use the natural N1 and N4 vectors in `TESTING.md`; do not add verdict labels, fixture markers or prompt-language hints to submitted text.
4. Do not preview, retry or rewrite a vector because a preferred verdict was not returned.
5. Run one critical transaction at a time and stop on mismatch.
6. For semantic transactions, record the full hash, consensus state, leader execution result, verdict and exact pending state.
7. For expected refusals, record the full hash, exact error and unchanged state.
8. Do not call a case PASS from `FINALIZED`, a screenshot or a frontend message alone.
9. After runtime completion, fetch deployed source, normalize only CRLF/LF and prove SHA-256 parity.

