# FileShed

> A retired Open WebUI add-on that gave tool-calling language models an integrated workbench for data, documents, media, editing, versioning, collaboration and deliverables. Persistent storage was its foundation, not the whole product.

FileShed is a project by Fade78, presented here as part of FadeShed. Its author has retired it from active development because Open WebUI's OpenTerminal now covers much of his original need. That is the author's reason for retirement, not a claim of complete feature equivalence. This page preserves the project and its design ideas without promising maintenance or compatibility with current Open WebUI releases.

## What it enabled

- **Tool-driven work from conversation.** `shed_exec` mediated approved command-line programs through explicit arguments. The model could inspect, search, transform and package files. This was not unrestricted shell access or an arbitrary Python execution service.
- **Data workflows.** Built-in SQLite operations supported CSV import, queries and CSV export. Commands could write stdout and stderr to files. A query without an explicit limit normally returned a short sample; `output_csv` wrote results to a file. This helped avoid filling the model context with intermediate data, but was not a universal memory or token-use guarantee.
- **Documents and media.** Pandoc, FFmpeg and other allowed programs could produce and transform deliverables when installed in the host environment. PDF production and image-processing features had additional dependencies. An allowlisted command was not necessarily installed.
- **Precise editing and history.** Text edits by line or pattern, byte patches, and an explicit lock/edit/save-or-cancel workflow. Documents and Groups spaces supported automatic Git versioning; Storage did not automatically version every file.
- **Collaboration.** Open WebUI group membership governed access to shared group documents. The ownership modes were `owner`, `group`, and `owner_ro`. Personal workspaces and group publication were deliberately distinct.
- **Deliverables.** ZIP creation and Open WebUI download-link integration let the model hand back a file. These links required an authenticated Open WebUI session; they were not public sharing URLs.
- **Model-facing ergonomics.** Task-oriented `shed_help` guides, command availability discovery, configuration introspection and structured errors with corrective hints. Public `Tools.shed_*` methods were separated from `_FileshedCore` internals.

## Four workspace contexts

Uploads was a conversation-scoped import area. Storage was the personal working area for transformations and persistent artifacts. Documents was the personal Git-versioned area. Groups provided shared, Git-versioned document spaces with membership and ownership rules.

The specification calls these three personal zones plus group spaces, not four interchangeable storage buckets.

## The documented example

The original README describes downloading country data, converting JSON to CSV, importing it into SQLite, adding and computing a population-density column, sorting results, exporting CSV, creating a ZIP and returning a download link. The repository includes a capture of this workflow with a 20B model and the resulting spreadsheet.

The microsite condenses these operations into a readable walkthrough. It is not a live agent, a newly executed benchmark, a complete runnable script or a guarantee of success in a fixed number of turns. The original capture includes retries and continuation prompts. Network downloads require explicit administrator enablement.

## Boundaries and safeguards

The design includes command allowlists, argument and path validation, user/group quotas, subprocess timeouts and resource limits, and network modes (`disabled`, `safe`, `all`). These are application-level controls in an Open WebUI add-on, not an operating-system security boundary. The source depends on Open WebUI internal APIs. The specification identifies single-instance locking constraints and does not support distributed locking across several Open WebUI instances.

The supplied 1.1.0 source contains optional per-user encryption using AES-256-GCM and Argon2id. This is at-rest protection with explicit limits: group files are not encrypted, runtime keys remain exposed to the host process, shell commands see encrypted bytes, and key loss means lost access. It is not universal end-to-end encryption. This source-level addition should not be silently attributed to the earlier 1.0.5 release documentation.

## Source boundaries

The requested basis for this microsite is `Fileshed-main.zip`, whose Git archive comment identifies revision `e69757ccab2aed5ce19dd615ffa2d86b16a08ba9`. Links below are pinned to that revision. The two images used by the microsite match the Git blob hashes returned for that revision.

The sources differ in ways worth preserving:

- `Fileshed.py` declares **1.1.0** and contains **44 public `shed_*` methods** in `Tools` (counted from the Python syntax tree).
- The README displays **1.0.5** and documents **38 functions**. The two encrypted-read methods and four encryption-management methods in the supplied code account for the six additional methods.
- The archived execution report states **1,200 passing tests for 1.0.5**. It is a historical report supplied by the project, not a new test run of this archive. The ZIP does not include the runner that produced that report.
- The supplied security reviews are **AI-assisted historical reviews**, not an independent audit or a current security certification. Their ratings are not used as a product guarantee here.

No industry-first claim, current compatibility guarantee, comparative OpenTerminal benchmark or new release status has been inferred from these documents.

## Reading map

- [Original README](https://github.com/Fade78/Fileshed/blob/e69757ccab2aed5ce19dd615ffa2d86b16a08ba9/README.md): product overview, workflows, Open WebUI installation, model configuration, function reference and optional dependencies.
- [Design specification](https://github.com/Fade78/Fileshed/blob/e69757ccab2aed5ce19dd615ffa2d86b16a08ba9/docs/SPEC.md): workshop/group philosophy, layered architecture, ownership modes, safeguards, model-oriented help, locking trade-offs and encryption.
- [Source](https://github.com/Fade78/Fileshed/blob/e69757ccab2aed5ce19dd615ffa2d86b16a08ba9/Fileshed.py): `_FileshedCore` (lines 578–4692), command execution (2651–2865), public tool API (4851–10009), SQLite (7562–8339), download links (8346–8669), help/introspection (8677–9009), encryption-management methods (9235–9589), and group collaboration (9597–10009).
- [Historical workflow capture](https://github.com/Fade78/Fileshed/blob/e69757ccab2aed5ce19dd615ffa2d86b16a08ba9/assets/Fileshed_dl_to_sqlite_to_archive.png): source image shown on this page.
- [Historical test report](https://github.com/Fade78/Fileshed/blob/e69757ccab2aed5ce19dd615ffa2d86b16a08ba9/docs/audits/fileshed/reports/Exec_tests.md): reported 1.0.5 execution results.
- [Historical Claude review](https://github.com/Fade78/Fileshed/blob/e69757ccab2aed5ce19dd615ffa2d86b16a08ba9/docs/audits/fileshed/reports/anthropic_claude_opus_4.5_thinking.md): review assumptions and residual risks.
- [Historical ChatGPT review](https://github.com/Fade78/Fileshed/blob/e69757ccab2aed5ce19dd615ffa2d86b16a08ba9/docs/audits/fileshed/reports/openai_chatgpt_5.2_instant.md): second AI-assisted review.
- [License](https://github.com/Fade78/Fileshed/blob/e69757ccab2aed5ce19dd615ffa2d86b16a08ba9/LICENSE): the original project is MIT licensed. The README credits Fade78 as original author and Claude Opus 4.5 as co-developer.
