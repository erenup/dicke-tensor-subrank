# Review record

These reports record the independent informal AI-agent audits of the
paper's mathematics. Each auditor worked separately from the other and from
the authors, derived the key steps independently before reading the proof,
checked every step, and ran its own exact tests. No report claims formal
certification or external peer review.

| Report | Scope | Verdict |
|---|---|---|
| [01](01-referee-A.md) | Complete statement and proof (limits, entropy inequality, collision counting, hashing and global isolation, asymptotics, upper bound), the exact checks, and the comparison with the cited sources; addendum on the source convention | Accept; no mathematical corrections (the addendum confirms correction C1 of report 02) |
| [02](02-referee-B.md) | Same scope, independent referee | Accept with corrections (one source-convention correction, C1) |
| [03](03-referee-B-executable-checks.md) | Component of report 02: the exact checks and the upper bound for arbitrary linear maps | Accept |

All corrections are incorporated. The one requested correction, C1 (the
monomial-degeneration convention of Christandl–Vrana–Zuiddam's Question
1.58), is applied in item 3 of [SOURCES.md](../core/proofs/SOURCES.md) and in
the paper's comparison with that question (`paper/sections/history.tex`).
The proof reviewed is byte-identical to [PROOF.md](../core/proofs/PROOF.md),
so the proof line numbers in report 02 refer to that file; the reviewed
statement differs from [STATEMENT.md](../core/proofs/STATEMENT.md) only in
non-mathematical heading text, and the two checkers are byte-identical to the
reviewed ones.

In addition, Wenqi Zhu (University of Oxford) checked the complete argument,
and Chunlin Liu (University of Science and Technology of China), a co-author
working on entropy, reviewed the proof.
