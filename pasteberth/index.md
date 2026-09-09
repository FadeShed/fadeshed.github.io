# Pasteberth

> Your files. Ready for what is next.

**Beta.** Pasteberth is a self-hosted place to stage and retrieve working files across browsers, clipboards, terminals and filesystems. A person, an agent or a script can use whichever interface fits. It is useful alone as well as between participants.

## Put it down once; pick it up your way

Paste a screenshot or text, drop a PDF or workbook, or publish a script's output. Retrieve supported content through the clipboard, copy a server-side filesystem reference, download the file, or collect a selection as a ZIP when enabled. A copied reference is not a public URL: its consumer needs filesystem access to that path. Pasteberth stores arbitrary allowed files, but does not edit their document formats.

## Try the workspace

The [interactive demo](https://fadeshed.github.io/pasteberth/#interface) includes sample files, project views, selection, comments, transfers and downloads. Additions remain in the browser tab's memory and disappear on reset or reload. The sandbox is not an authenticated or persistent Pasteberth installation.

## Ordinary files, explicit publication

A managed item consists of a data file and its JSON sidecar. `register FILE` creates or refreshes the sidecar of a completed local regular file without rewriting data or contacting the daemon. It does not apply the running daemon's retention or per-zone free-space policy. Use a fresh name and the [safe registration recipe](reference/docs/recipes/register-file.md) rather than overwriting an existing managed pair.

`drop` asks the daemon to publish; even direct local staging still contacts it. HTTP supports the documented browsing and managed operations. MCP currently exposes only `drop` to a known zone. None of these interfaces assigns a human or agent to a particular side.

## Project conventions

A collection can discover existing exchange directories such as `/repo/<project>/ignoredbygit/exchange`. Configure the rule and a group once; project templates provide eligible directories and permissions. A later overview refresh exposes new matching zones. This is request-triggered scanning, not an instantaneous watcher. Discovery creates neither projects nor managed files. Groups can provide focused views without duplicating data.

## Context, not an imposed process

Zones can be organized by project, subject or stage. Comments can carry context; copies and moves can support review. There is no enforced order, assignment or approval system. Retention can delete older items, and multi-file operations may partially succeed. Important deliverables belong in durable storage outside the working area.

## Documentation

- [Task map](reference/GUIDE.md)
- [Using Pasteberth](reference/docs/using-pasteberth.md)
- [Integrations](reference/docs/integrations.md)
- [Project provisioning](reference/docs/provisioning.md)
- [Deployment and trust boundaries](reference/docs/deployment.md)
- [Agent index](llms.txt)

The service uses shared authentication, not individual accounts or per-zone ACLs. The documentation snapshot describes the pinned source used for this site; follow the release matching your installation. Pasteberth is AGPL-3.0-or-later.
