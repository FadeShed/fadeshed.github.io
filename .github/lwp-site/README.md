# LightWebPres published site sources

The editable sources corresponding to the approved product portal are in this directory.

- `sources/en/` and `sources/fr/`: the seven portal chapters and their Identity Kit.
- `sources/comparisons/`: the same article rendered with native, documentation, Field Notes and Nebula presentation choices.
- `sources/guides/`: the reader guide source editions.
- `tools/`: the renderer, required notices and reviewed integration helpers.

Keep the complete published portal under `lightwebpres/` and `fr/lightwebpres/`. An isolated native rebuild does not reproduce every gallery, browser-builder, download or shared navigation resource. Do not replace the complete portal with that partial output.

## Preview a source edit

From the repository root, with a new output directory:

```sh
python3 .github/lwp-site/tools/render-native.py --lang en --output work/lwp-en-check
python3 .github/lwp-site/tools/render-native.py --lang fr --output work/lwp-fr-check
```

The helper builds, audits and verifies the native source pages. Serve only its generated `public/` directory when inspecting it. The helpers have not become a one-command deployment system for the complete portal.

## Publication checks

Install the browser-check dependencies in an isolated environment and run `.github/lwp-publication/qa.py` against a public-only staging directory. The `check-live-reader-refresh.yml` workflow exercises the deployed portal and compares committed bytes to served files.

The fragment files and `resume.py` in `.github/lwp-publication/` are historical recovery inputs for one interrupted transfer. Recovery is manual-only; it is not the source format for subsequent edits. Do not replay an old restoration or bilingual bootstrap over the current portal.

Neutral URLs are English; French lives explicitly under `/fr/`. Keep both editions, native LightWebPres controls and the language/navigation conventions together. Changes outside the product portal need a separate, explicit scope.
