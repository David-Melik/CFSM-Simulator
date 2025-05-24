# CFSM Simulator
This is a **student group project** developed as part of a university course on communication protocols.

This project is about a **Communicating Finite State Machine (CFSM) Protocol Simulator** for *N* protocol entities. Its purpose is to help developers and designers conveniently investigate the behavior of communication protocols.

The simulator requires loading a single file in which the user defines each FSM individually. At least two FSMs must be defined. It then simulates their interactions either in **step-by-step mode,** where the user selects one of the available transitions presented by the system or in **automatic mode**, where the system randomly selects one of the possible transitions.



## Installation
Clone the project
```
git clone https://github.com/David-Melik/CFSM-Simulator
```

Install required dependencies with:
```
pip3 install -r requirements.txt
```

## How to use it
To start the simulator, you must provide a YAML settings file using the `-s` (or `--settings`) flag:

```
> python3 main.py -s
usage: main.py [-h] -s SETTINGS
main.py: error: argument -s/--settings: expected one argument

```

For example:

```
> python3 main.py -s settings01.yaml

```

## Exemple of design

## 🛠️ Features

- Load FSM definitions from YAML configuration files
- Step-by-step simulation mode (user manually selects next valid transitions)
- Automatic mode (transitions are randomly selected from the valid ones)
- Visual display of current FSM states, channel contents, and transition logs
- And much more
