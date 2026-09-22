The chain is platform-independent by default and platform-specific on demand. The platform is declared **once**, in MRD Section 5, and carried in every downstream header block. Nothing below the MRD re-decides it; each stage just adds what its own layer owes that platform.

Where no platform is declared, write platform-neutrally and say so — "the user opens the overdue view," not "taps" or "clicks." An unstated platform silently becomes whatever the first engineer assumes, which is the failure this section exists to prevent.

| | Web | Mobile (iOS / Android) | Desktop (macOS / Windows / Linux) |
|---|---|---|---|
| **MRD** | Browser reach, no-install trial | Store discovery, store economics (commission, review) | Enterprise procurement, offline-capable field use |
| **BRD** | Hosting and bandwidth cost | Developer accounts, store fees, per-platform build cost | Code-signing certificates, notarization, distribution |
| **PRD** | Responsive breakpoints, browser support bar, SEO, PWA install | Permissions, offline and sync, push, deep links, store policy | Windowing, menu bar, file-system access, auto-update, OS login item |
| **Design Spec** | Breakpoints, hover and focus, keyboard, print | Touch targets, safe areas, system back, orientation, keyboard avoidance | Window states and resizing, native menus, keyboard shortcuts, multi-window, drag-and-drop, tray |
| **TRD** | Browser support matrix, bundle budget, CDN, CSP | Minimum OS versions, API deprecation, binary size, store review, OTA updates | Packaging and installers, signing and notarization, auto-update channel, per-OS filesystem and permissions |
| **QA** | Browser × OS × viewport matrix | Device × OS-version matrix, store submission, upgrade and permission flows | Per-OS install, upgrade, uninstall, offline, signed-build verification |

### Multi-platform

Several platforms is the normal case, not the exception, and it needs three things beyond a list.

**A primary platform.** Exactly one — it ships first and breaks ties when platforms want different things. Without it, every cross-platform disagreement is re-argued from scratch.

**A stated parity intent.** Full parity, deliberately reduced scope on some platforms, or capability that exists on only one. Unstated parity is the most expensive assumption in a multi-platform build, and it surfaces late — usually as "wait, that's not on Android?" during launch review.

**A platform column on every requirement.** This is the mechanism that keeps a multi-platform product traceable as it diverges. Every numbered item carries the platforms it applies to — `All` for the common case, a named subset when it doesn't:

```
NEED-04   Mobile only      capture a receipt at the moment of purchase
BR-09     Mobile           field staff capture without connectivity
PR-08     iOS, Android     capture a photo and attach it to an invoice
SCR-09    iOS, Android     receipt capture screen
CMP-07    iOS, Android     ReceiptCapture component
FR-12     iOS, Android     queue locally, upload on reconnect
TC-041    iOS, Android     capture offline, reconnect, verify upload order
```

Then one rule of construction *inside* a document: **specify shared behavior once and list only the deltas.** Where the same requirement behaves differently per platform, keep one row and put the difference in its acceptance criteria — never split it into near-duplicate rows, which drift apart by the second revision. Most functional requirements on a multi-platform product are a single shared-backend behavior serving several clients; mark those as shared, and the genuinely client-specific ones stand out as the ones needing per-platform attention.

### Per-platform documents

Where more than one platform is declared, four stages produce one complete document per platform rather than one document covering all of them: **PRD, Design Spec, TRD, and QA Test Plan**. The MRD and BRD stay single — market and business cases are not platform-bound.

`docs/<skill-name>/<slug>-<type>-<platform>-v<version>.md`, with `<platform>` drawn from a fixed vocabulary: `web`, `ios`, `android`, `macos`, `windows`, `linux`, `api`. One platform, or platform-neutral, means one file with no platform token.

Each file is standalone and complete — shared behavior written out in full, not cross-referenced — and four rules keep the set from drifting:

1. **IDs are global.** A requirement on several platforms carries the same ID in every file; a platform-only requirement takes the next ID from the same sequence and appears only in its own file. Never renumber per platform.
2. **Shared content is written identically.** A diff between two platform files should show real divergence and nothing else.
3. **A shared change touches every file** in the same run, each bumped to its next version. A new iOS file beside a stale Android one is the failure this structure invites.
4. **Parity is stated in every file** — full parity, reduced scope here, or unique to this platform — with the sibling files named.

The cost is deliberate and worth stating: shared requirements now exist in several copies, and keeping them identical is manual work at every revision. The consistency review below is what catches it when they diverge.
