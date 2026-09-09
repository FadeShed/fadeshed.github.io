# LightWebPres

> Write one Markdown source. Read it on a phone, present it in landscape, publish it as a static site.

Status: **Beta**. LightWebPres is a single-file Python tool for generating self-contained HTML articles with slide navigation, optional long-form text and a series index. The website package uses engine **0.56.0**, identified by its build information as **unreleased**; that is not a claim about the latest public release.

## One source, several reading contexts

Readers can scroll in portrait and navigate the same content in landscape. Generated pages carry their CSS and JavaScript and do not require the reader to install LightWebPres or hold a presentation-service account. Long-form content, notes, images, math and series navigation support more than a fixed slide deck.

## Appearance and publishing

Identity, presentation preset and theme are distinct choices. Native and Commons choices coexist with self-contained Identity Kits. Typed configuration and per-series settings support repeatable output; advanced custom CSS remains outside some automated checks.

The CLI can build unattended, return exit codes, audit sources and styles, verify output drift, and watch a series for changes. This makes it useful to human authors, scripts and agents. Markdown remains the source of truth; the generated site is an artifact to inspect, publish and share.

## Authoring interfaces

The Python CLI runs with the standard library. The included browser builder runs the same engine under vendored Pyodide. It requires HTTP(S), not `file://`. ZIP builds stay in the browser tab. Its GitLab synchronization mode talks to the configured instance and creates or updates files; it does not delete stale output.

The browser builder is not the separate `lightwebpres-gui` editor. Do not treat the CLI, browser builder and external editor as the same component.

## Agent-oriented documentation

The format skill specifies the article grammar. The separate sourced-presentation skill is an optional editorial method, not a prerequisite for rendering. A useful automated workflow is to author or update sources, build, audit with strict checks where appropriate, verify with matching options, then inspect the generated result before publishing.

## Trust boundaries

LightWebPres renders trusted sources; it is not an HTML sanitizer. Raw HTML can include scripts. Sanitize untrusted input upstream. Speaker notes are embedded in the output and are not private; source-only comments serve a different purpose. Tags are viewing filters, not access controls. Deleting a source does not automatically remove stale published files.

## License

The engine is GPL v3 or later with the LightWebPres Output Exception. Keep the relevant notices when redistributing the executable or vendored runtime. Generated presentations and the generator itself are not the same licensing case; consult the supplied legal texts.

## Documentation

- [README](https://raw.githubusercontent.com/Fade78/lightwebpres/a43cb344f34f6a8d282f8d1dc9b54863103dc795/README.md): product entry point.
- [Guide](https://raw.githubusercontent.com/Fade78/lightwebpres/a43cb344f34f6a8d282f8d1dc9b54863103dc795/GUIDE.md): operational manual.
- [Format skill](https://raw.githubusercontent.com/Fade78/lightwebpres/a43cb344f34f6a8d282f8d1dc9b54863103dc795/agent/skills/lightwebpres/SKILL.md): article grammar.
- [Agent index](llms.txt): documentation routes and limits.
