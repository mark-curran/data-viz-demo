# Data Visualization Demo

A project to demonstate some open source data visualization capabilities.

Contains a python package for generating visuals.

## Backend Setup

### Backend Dependencies

Generate Bazel dependencies

To install existing dependencies

```shell
bazel build backend
```

When dependencies are changed.

```shell
bazel run //backend:requirements.update
```

followed by building the backend again.

### VSCode Support

Install the correct version of python onto your machine.

```shell
pyenv install $(grep -m1 'python_version' MODULE.bazel | grep -o '[0-9]\+\.[0-9]\+') 
```

Then create a virtual environment in the repository root folder.

```shell
pyenv local $(grep -m1 'python_version' MODULE.bazel | grep -o '[0-9]\+\.[0-9]\+') && python -m venv .venv   
```

Then add the external dependencies

```shell
.venv/bin/pip install -r backend/requirements_lock.txt
```

## Binaries Required

- Bazel
- Buildifier
- Python
- PyEnv

## References

- [Official python_rules Documentation](https://rules-python.readthedocs.io/en/latest/index.html)
- [Build a python library with Bazel](https://buildkite.com/resources/blog/building-and-packaging-a-python-library-with-bazel/)