# Galvanet

A playground for running Distributed Systems in Python

## Set up package development environment

- Install [pipx](https://pipx.pypa.io/stable/)

```sh
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

> Optional to allow pipx actions with `--global` argument:
>
> ```sh
> sudo pipx ensurepath --global
> ```

- Install [poetry](https://python-poetry.org/docs/) package manager

```sh
pipx install poetry
```

- Install [galvanet](https://github.com/slottwo/galvanet) dependencies

```sh
cd path/to/galvanet
poetry install
```

## Usage

> Activating the virtual environment (some code editor can do this automatically):
>
> ```sh
> eval $(poetry env activate)
> ```
>
> You can execute a command without entering in the environment with:
>
> ```sh
> poetry run <command>
> ```

### Launch server application

- With [taskipy](https://github.com/taskipy/taskipy)

  ```sh
  task run
  ```

- With [fastapi](https://fastapi.tiangolo.com/pt/)

  ```sh
  fastapi dev scr/galvanet/app.py
  ```


### Execute tests from `src/tests`

```sh
task test
```


### List all tasks

```sh
task --list
```
