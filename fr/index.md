# FadeShed

> Tools for agentic work, built from real problems and shared with the community.

FadeShed is Fade78's software workshop: practical tools that help people, agents, terminals, browsers and filesystems work together. Most began as a tool the author needed himself. Publishing them is his way of giving back to developers, sysadmins, tinkerers and fellow nerds.

These are independent projects, not a single product suite. They do not require one another, and an agentic orientation does not mean they are only useful to agents. A project may retire without a promise of ongoing maintenance.

## Projects

### FileShed — Retired

An Open WebUI add-on that let tool-calling language models perform work inside a conversation: command-driven operations, SQLite and CSV pipelines, document and media conversion, precise editing, Git history, group collaboration and authenticated file delivery. Persistent storage was the foundation, not the full purpose.

The author retired FileShed when OpenTerminal covered much of his own workflow. The code and design remain available; this is not a claim of complete feature equivalence.

[FileShed overview](fileshed/overview.md) · [FileShed agent index](fileshed/llms.txt)

### Pasteberth — Beta

A self-hosted staging and exchange area for artifacts, backed by ordinary filesystem directories. Put an item in through the Web UI or a tool; retrieve it as supported clipboard content, a reference, a file or a selection. Useful alone, between people, between agents, or between scripts and tools. Local `cp` plus `register` does not require a network upload.

[Pasteberth overview](pasteberth/index.md) · [Pasteberth agent index](pasteberth/llms.txt)

### LightWebPres — Beta

A single-file Python publishing tool that turns Markdown into self-contained HTML articles and presentations. The same output can be read as a page or navigated in landscape. Themes, presentation presets, identity kits, publishing checks and a browser builder support both human and automated authoring.

[LightWebPres overview](lightwebpres/index.md) · [LightWebPres agent index](lightwebpres/llms.txt)

## Source and documentation

The project sites are hosted together in `FadeShed/fadeshed.github.io`; the original application repositories remain under `Fade78` until transferred. Consult the documentation matching the chosen source revision or release for installation and compatibility.

[FadeShed on GitHub](https://github.com/FadeShed) · [Agent-oriented documentation index](llms.txt)
