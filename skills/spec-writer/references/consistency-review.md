When asked to check an existing set, report on:

1. **Coverage** — every parent ID has at least one child; list the ones that don't.
2. **Orphans** — every child cites a real parent; list the ones that don't.
3. **Unmarked orphans** — a child whose Upstream cell is blank or `—` instead of `[no upstream — new in this document]`. More common than a fabricated parent, and it reads as traced when it isn't.
4. **Layer violations** — content sitting in the wrong document.
5. **Staleness** — a child whose upstream document has a newer version file on disk than the version the child cites in its header.
6. **Contradictions** — the same rule, limit, or metric stated differently in two documents. Log both; don't pick a winner.
7. **Platform drift** — where a stage produced per-platform files, a shared ID whose text, acceptance criteria, or priority differs between them, and any platform file left at an older version than its siblings.
8. **Untracked change** — a document whose newest version added no Revision History row, or whose row leaves the ID columns blank. Both break the diff every downstream stage depends on.
9. **Missing changelog entry** — a document version on disk with no bullet in `docs/CHANGELOG.md`, or an entry whose ID deltas disagree with that version's Revision History row.
