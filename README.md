# PERD workflow starter

A working [PERD](https://perd.app) workflow to start yours from: four operations,
a page to use them in the browser, and the tests PERD's build would run.

**Guide:** [Publish your first workflow](https://perd.app/docs/getting-started/first-workflow/)

## Use it

1. Select **Use this template › Create a new repository**, and keep the new
   repository **public**: PERD builds from public repositories.
2. Clone it, then run the tests:

   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install "perd-worker[page]" pytest
   pytest
   ```

3. In the PERD console, open your project, then **Workflows › Publish new**,
   and paste your repository's address.

## Files

| File | Purpose |
| --- | --- |
| `workflow.py` | The operations PERD exposes, one per decorated function. |
| `page.py` | The browser page, written with perdlit. |
| `perd.toml` | The compute class and the Store listing. |
| `requirements.txt` | Your own Python dependencies. |
| `setup.sh` | Optional system packages, installed at build time. |
| `favicon.ico` | The icon on the desktop and in the Store. |
| `CHANGELOG.md` | Shown on the workflow's Changelog tab. |
| `tests/` | Calls the operations and checks the page. |

## The four call modes

| Decorator | Shape | In the starter |
| --- | --- | --- |
| `@workflow.unary` | One request, one answer | `add` |
| `@workflow.input_stream` | A stream in, one answer | `total` |
| `@workflow.output_stream` | One request, a stream out | `count_up` |
| `@workflow.bi_di` | Streams both ways | `running_mean` |

Arguments and results are scalars: `float`, `int`, `str`, `bool` or `bytes`.
Streams carry tuples of them.

## Licence

MIT. Replace this README with your workflow's own: PERD shows it on the
workflow's Store page.
