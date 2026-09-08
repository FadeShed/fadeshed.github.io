# Pasteberth

> Your files, ready for what's next. A self-hosted artifact staging and exchange layer backed by ordinary filesystem directories.

Status: **Beta**. Pasteberth is a FadeShed project. It helps move work between clipboard-oriented, browser-oriented and filesystem-oriented contexts without requiring a separate artifact interface for every tool.

## Artifacts, not just pasted screenshots

An artifact can be an image, text, HTML clipboard content, a PDF, a spreadsheet, CSV, an archive, a log or another allowed file. Storing and retrieving a format is not the same as interpreting it. Specialized previews and clipboard-copy behavior are available only for supported content types.

An item can be deposited once and picked up later as supported clipboard content, a filesystem reference or path, a downloaded file, or part of a multi-selection. A solo user can paste something now and copy it again later. Two people, a person and an agent, two agents, or scripts and processes can also exchange artifacts. Pasteberth does not require the human to use the graphical interface or the agent to use the CLI.

## A zone is a real directory

A zone is a named staging or exchange point on the filesystem used by the Pasteberth service. Managed items pair a data file with a JSON sidecar. A coherent sidecar identifies a file as managed; unrelated files do not automatically become Pasteberth items.

The filesystem is an interface, not an opaque storage implementation. Normal tools can produce ordinary files. A copied file can be registered where it already belongs:

```sh
cp report.pdf /repo/atlas/ignoredbygit/exchange/
pasteberth register /repo/atlas/ignoredbygit/exchange/report.pdf
```

`register` validates the existing file and creates or refreshes its sidecar. It does not rewrite the data file or contact the daemon. This is not an upload.

`drop` is different: it contacts the service. Local staging can avoid transferring a large payload through HTTP, but the operation is still daemon-backed. The optional MCP adapter provides a publication path for compatible tools; its existence does not imply a full browsing or administration API.

## Automatic project discovery

Zone collections can discover directories that match a convention such as `/repo/<project>/ignoredbygit/exchange`. Project templates create the directories with suitable permissions; Pasteberth discovers eligible matches on refresh. No per-project configuration edit or daemon restart is needed.

Discovery uses background scanning, not instantaneous filesystem notifications. It does not create the project directories, bypass permissions or turn Pasteberth into an unrestricted recursive file browser. Groups organize views of zones; they are not access-control boundaries.

## Working with the interface

Browse project zones, preview an artifact, spot new arrivals and select several files for the next task. For supported content, copy it back to the clipboard. Use a file reference when another tool works on the same filesystem, or download the actual file when that is what the next context needs.

Multi-selection and zone transfers support working sets rather than only individual files. Commands and available operations should be checked against the installed release.

## Common workflows

- Personal staging: paste now, copy or retrieve later.
- Document handoff: stage a workbook and requirements document, then retrieve a generated report or archive.
- Agent and script outputs: keep producing files while Pasteberth provides the interface for inspection and retrieval.
- QA and debugging: collect screenshots, logs and diagnostic bundles in a project zone.
- Template-provisioned exchange: let new workspaces appear through a common directory convention.

## Boundaries

Pasteberth is not a cloud drive, a public file host, a document editor, a synchronization service between independent servers, or an identity-management platform. A server-side path is useful only in a context that can access that filesystem. Rich clipboard support is not universal file-format support. Review authentication, permissions and deployment guidance before exposing the service beyond its intended environment.

## Documentation

- [README](https://github.com/Fade78/pasteberth/blob/main/README.md): product entry point and release-specific requirements.
- [User guide](https://github.com/Fade78/pasteberth/blob/main/GUIDE.md): installation, configuration, CLI and operational guidance.
- [Agent index](llms.txt): the short path to relevant documentation.
- [FadeShed](../index.md): related projects.
