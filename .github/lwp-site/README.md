# LightWebPres portal: one source of truth

The editable portal lives in `sources/`. `engine-lock.json` identifies the reviewed renderer in `tools/lightwebpres`; kit manifests and themes travel with each series. The build does not import `.github/bilingual/lwp` or execute a historical payload.

## Build and check

Install `requirements.txt` in a virtual environment, then run from the repository root:

```sh
python3 .github/lwp-site/build.py --output work/site --report work/native-qa
python3 .github/lwp-site/qa.py work/site work/browser-qa
```

Use a new output directory and serve only that directory. The builder regenerates both portal editions, examples, guide, four identity comparisons, gallery and downloadable source projects. It verifies native output before applying the shared FadeShed navigation. It also produces `downloads/publication.html`: a complete series with embedded images and matching native verification options.

The browser shell, Pyodide distribution, reference documents and illustrations are tracked static inputs assembled with those generated pages. They are not fetched silently from a moving upstream branch. Review and update them alongside the renderer lock. Browser QA performs actual ZIP builds in both languages. The builder checks that the workshop home, FileShed and Pasteberth remain unchanged. Source downloads are native projects, not a full hosting environment.

## Kit migration

`migrate-chrome.py` explicitly moves the previously vendored guide and Field Notes visual chrome to typed Theme properties, retaining structural wrappers and localized content. The initial migration records `migration-state.json`; subsequent builds use the committed source files directly. It does not modify LightWebPres or migrate arbitrary third-party kits.

## Publication

Two maintained workflows remain:

- `publish-minisites.yml`: builds and checks canonical source changes, then pushes one tested candidate to `publication/lwp-<run-id>`. Its report records the exact parent and candidate commit.
- `check-live-reader-refresh.yml`: checks deployed bytes and browser journeys when generated files reach main. GitHub Pages keeps its current hosting configuration.

Advance main to the candidate only when it still matches the recorded parent; never force-push or overwrite other work. With authenticated Git:

```sh
git fetch origin
git switch main
git pull --ff-only
git merge --ff-only origin/publication/lwp-<run-id>
git push origin main
```

An authorized connector can also fast-forward main to the recorded candidate. That final user-authenticated action triggers Pages; a runner's repository token push alone does not. No personal token from a conversation is embedded in the workflow.

Historical workflows are preserved under `.github/legacy-workflows/`, outside the active directory. Do not restore them or replay the old bundles over current sources.

## Checks and conventions

The suite reads the renderer lock and checks current native controls. Role destinations, locale routes, comparator choices, downloaded documents and actual browser builds are the contracts. Tests are ordinary Python; no source substitution followed by `exec` occurs in the test runner.

English is the neutral URL; French uses `/fr/`. Keep native zoom, no redundant Reading & zoom button, versionless public prose, and original licenses. Visually review the two languages and the comparison images after kit changes. Chromium mobile emulation is not physical iOS/Android testing.
