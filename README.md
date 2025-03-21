# Galvanet

A playground for running Distributed Systems in Python

> You can, but shouldn't, ignore everything below and for now simply use:
>
> ```sh
> python3 -m pip install fastapi[standard]
> python3 -m fastapi dev src/galvanet/app.py
> ```

## Set up package development environment

### Install [pipx](https://pipx.pypa.io/stable/)

```sh
python3 -m pip install --user pipx
python3 -m pipx ensurepath
sudo pipx ensurepath --global # optional to allow pipx actions with --global argument
```

### Install [poetry](https://python-poetry.org/docs/) package manager

```sh
pipx install poetry
```

### Install [galvanet](https://github.com/slottwo/galvanet) dependencies

```sh
poetry install
```

## Launch server application

> Activating the virtual environment:
>
> ```sh
> $ eval $(poetry env activate)
> galvanet-py3.12 $  # Virtualenv entered
> ```

### With [taskipy](https://github.com/taskipy/taskipy)

```sh
task run
```

### With [fastapi](https://fastapi.tiangolo.com/pt/)

```sh
fastapi dev scr/galvanet/app.py
```

### Without activate an environment

```sh
poetry run task run
```

or

```sh
poetry run fastapi dev src/galvanet/app.py
```
