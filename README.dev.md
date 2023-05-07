# Development documentation

## Install

```bash
python -m venv env
. env/bin/activate
pip install --upgrade pip setuptools
pip install --no-cache-dir -e '.[dev]'
```

## Running

```bash
flask --app perprof_web/app.py run
```

## Linting

We use `pre-commit` to run a few linting tools.
Some of them should also be installed separately, for integration with IDEs.
If you install the `dev` version of this package (as suggested above), then your environment has all of these.
To run the linting commands use

```bash
pre-commit run -a
```

To install `pre-commit` as a pre-commit hook, run

```bash
pre-commit install
```

## Tests

TODO: Add tests

## Workflow information

TODO: Add workflows
