# FileShed

> An agentic workbench inside Open WebUI: work on data, documents and media, make precise edits, collaborate and hand back usable files. Persistent storage was its foundation, not its entire purpose.

**Retired.** FileShed remains available for its implementation and design ideas. OpenTerminal now covers much of the author's original need; this is his reason for retirement, not a promise of full feature equivalence or current Open WebUI compatibility.

## Work from a conversation

Through `shed_exec`, a tool-calling model could inspect, search, transform and package files with explicitly allowed programs. These commands require their host dependencies; an allowlisted program is not necessarily installed. This is not unrestricted shell access or an arbitrary Python execution service.

SQLite tools import CSV, run queries and export results. Intermediate data stays in files rather than being copied into every message. Pandoc, FFmpeg and other available commands can transform documents and media. PDF production and image processing require the relevant tools to be installed.

Line and pattern edits, byte patches and an explicit lock/edit/save-or-cancel workflow support precise changes. Documents and Groups have automatic Git history; Storage is a personal working area, not automatic versioning of every file.

## A private workshop and shared documents

Uploads imports attachments from the current conversation. Storage holds personal working files across conversations. Documents keeps personal Git-versioned documents. Groups uses Open WebUI membership and explicit `owner`, `group` and `owner_ro` modes for shared work.

ZIP creation and Open WebUI download links turn work into a deliverable. The links require an authenticated Open WebUI session; they are not public sharing URLs. Task-oriented `shed_help`, command discovery, limited output and corrective errors make the interface usable through model tool calls.

## Follow a complete workflow

The documented example starts with country data, converts JSON to CSV, imports it into SQLite, calculates population density, orders the results, exports CSV and returns a ZIP download. The walkthrough on this site illustrates the sequence rather than acting as a live agent or promising a fixed number of turns. Network retrieval needs explicit administrator permission.

## Boundaries that matter

Command allowlists, path and argument validation, quotas, timeouts and network modes (`disabled`, `safe`, `all`) are application-level safeguards, not an operating-system sandbox. The add-on depends on Open WebUI APIs. Locking is designed for a single instance, not distributed coordination.

The code also includes optional personal-file encryption using AES-256-GCM and Argon2id. Groups remain unencrypted, runtime keys are exposed to the host process, shell commands see encrypted bytes and losing the key loses access. This is not universal end-to-end encryption. Consult the source and the relevant guide together before enabling a feature: the retired project's documents and implementation are not a promise of compatibility with a newer host.

## Explore the project

- [Presentation](index.html): operations, workspaces and a complete data workflow.
- [Original guide](https://github.com/Fade78/Fileshed/blob/main/README.md): installation, examples and function reference.
- [Design specification](https://github.com/Fade78/Fileshed/blob/main/docs/SPEC.md): ownership, safeguards, architecture, locking and encryption.
- [Implementation](https://github.com/Fade78/Fileshed/blob/main/Fileshed.py): the public tools and their internal implementation.
- [License](https://github.com/Fade78/Fileshed/blob/main/LICENSE): original MIT license and attribution.
