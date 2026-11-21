# Qbus MQTT API

Python library for the MQTT protocol used by [Qbus](https://iot.qbus.be) home automation controllers. It powers the [Qbus integration](https://www.home-assistant.io/integrations/qbus/) in Home Assistant.

The library handles the conversion between Qbus MQTT messages and Python objects:

- **Discovery**: parse the controller configuration into devices and their outputs.
- **State**: read and write the state of outputs such as switches, dimmers, shutters, thermostats and weather stations.
- **Requests and topics**: build command payloads and the MQTT topics to publish them on.

It doesn't connect to an MQTT broker itself; use it together with your MQTT client of choice.

## Installation

```bash
pip install qbusmqttapi
```

## Development

Requires Python 3.12 or newer.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.dev.txt -e .
```

Linting and type checking:

```bash
ruff check src
ruff format src
pylint src/qbusmqttapi
mypy src
```

Ruff handles formatting and most lint rules. Pylint is used for the checks Ruff doesn't implement; overlapping messages are disabled in `.pylintrc.toml`.

Run tests with `pytest`.

When opening the project in VS Code, accept the prompt to install the recommended extensions (see `.vscode/extensions.json`).

