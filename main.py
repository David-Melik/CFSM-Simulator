import yaml
import argparse
from time import sleep

"""
python3 -m pip install rich
python3 -m pip install rich-cli
"""
from rich.console import Console
from rich.table import Table

from display import *
import random

# Initialize the console for rich text output
console = Console()


def settings_read(file_path):
    # Print the settings in a table
    with open(file_path, "r") as file:
        content = yaml.safe_load(file)  # Load and parse the YAML file

        machines = content.items()

        # Create a table for displaying the settings
        console.print(f"Imported Settings:", style="bold cyan")
        table_settings = Table(show_header=True, header_style="bold cyan")
        table_settings.add_column("Machine name", style="dim", width=12)
        table_settings.add_column("Inital global state")
        table_settings.add_column("All possible state", style="dim", width=20)
        table_settings.add_column("Transition (Event name | input | change of states)")

        for machine, machine_data in content.items():
            # Initialise

            row_content = [machine]

            initial_global_state = ", ".join(
                machine_data["Initial_global_state"]
            )  # For table
            row_content.append(initial_global_state)

            states = ", ".join(machine_data["States"])
            row_content.append(states)
            transitions = machine_data["Transitions"]

            # For checking if the fsm are infinite
            listOfto = []
            listOfStates = machine_data["States"]

            # Create the row content for each state
            # Find all transitions where the 'from' state is the current state
            transition_info = []
            i = 1
            for transition in transitions:

                if i > 1:
                    transition_info = []
                    row_content = []
                    row_content.append("")
                    row_content.append("")
                    row_content.append("")

                transition_info.append(transition.get("event", "N/A"))
                transition_info.append(transition.get("input", "N/A"))
                transition_info.append(
                    f"({transition.get('from')} -> {transition.get('to')})"
                )
                listOfto.append(f"{transition.get('to')}")

                # If there are transitions, join them with a comma. Otherwise, display "No transitions"
                if transition_info:
                    row_content.append(" | ".join(transition_info))

                else:
                    row_content.append("No transitions")
                i = i + 1

                table_settings.add_row(*row_content)
            # check if the fsm is infinte or not
            if all(state in listOfto for state in listOfStates) == False:
                raise ValueError(
                    f"The FSM '{machine}' is not infinite: some states cannot be reached (no transition leads to them)."
                )
        # Print the table
        console.print(table_settings)
        return tuple(machines)


def update_machine_file(file_path):
    machines = file_path
    updated_machines = []

    for name, data in machines:

        data["actual_state"] = data[
            "Initial_global_state"
        ]  # put the actual states by the values of the inital states

        machine_names_list = [name for name, _ in machines]
        machine_names_list.remove(name)

        for other_machines_names in machine_names_list:
            data[f"Channel {name} -> {other_machines_names}"] = []

        updated_machines.append((name, data))

    # Optional: print to verify
    # console.print(updated_machines)
    return updated_machines


def validate_settings_file(file_path):
    try:
        with open(file_path, "r") as file:
            content = yaml.safe_load(file)
            # Check if there are at least two machines if len(content) < 2:
            # Check if there are at least two machines
        if len(content) < 2:
            raise ValueError(
                "There must be at least two machines in the settings file."
            )

        # Check that every machine has at least one initial state
        for machine_name, machine_data in content.items():
            if "Initial_global_state" not in machine_data:
                raise ValueError(
                    f"Machine '{machine_name}' is missing an 'initial_global_state'."
                )
            if not machine_data["Initial_global_state"]:
                raise ValueError(
                    f"Machine '{machine_name}' has no initial state defined."
                )

            for transition in machine_data.get("Transitions", []):
                input_val = transition.get("input", "")
                if not input_val.startswith(("+", "-", "τ", "!", "?")):
                    raise ValueError(
                        f"❌ Invalid input '{input_val}' in machine '{machine_name}' have to be in Zafiropulo notations"
                    )

        # If all checks pass
        return True, "Settings file is valid."

    except ValueError as e:
        console.print(f"[bold red]Error in settings files[/bold red]: {e}")
        return False


def read_yaml_file(file_path):
    # Open the YAML file and read its content
    with open(file_path, "r") as file:
        content = yaml.safe_load(file)  # Load and parse the YAML file

        # Print the content of the YAML file
        console.print("\nContent of the file:", style="bold cyan")
        console.print(content, style="italic green")


# Start the simulation
def choose_simulation_mode():
    while True:
        mode = str(input("Select simulation mode (S - Step by step | A - Automatic): "))

        if mode == "S" or mode == "s":
            console.print("[green]✔️  Step by step mode selected[/green]")
            return "S"

        elif mode == "A" or mode == "a":
            console.print("[green]✔️  Automatic mode selected[/green]")
            return "A"

        else:
            console.print("[bold red]Please select a valid options[/bold red]")


def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(
        description="Simulator, executor for N protocol entities"
    )

    parser.add_argument(
        "-s",
        "--settings",
        type=str,
        help="Path to the settings settings file (in YAML extension)",
        required=True,
    )

    # Parse the arguments
    args = parser.parse_args()

    try:
        # Validate both files have the correct extension
        for file_path in [args.settings]:
            if not file_path.endswith((".yaml", ".yml")):
                raise ValueError(
                    f"The file '{file_path}' is not a valid YAML file (must have .yaml or .yml extension)."
                )

        if validate_settings_file(args.settings):
            machines_settings = settings_read(args.settings)
            machines_settings = update_machine_file(machines_settings)
            mode = choose_simulation_mode()
            simulation(machines_settings, mode)

    #            displayFSM(machines_tuple)

    # lauch_simulation(machines_tuple, protocol_transitions_tuple)

    except ValueError as e:
        # Catch invalid file extension or other ValueErrors
        console.print(f"[bold red]Error[/bold red]: {e}")
    except Exception as e:
        # Catch any unexpected errors
        console.print(f"[bold red]Error[/bold red]: {e}")


if __name__ == "__main__":
    main()
