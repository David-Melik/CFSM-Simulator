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


def protocol_read(file_path):
    protocol_transitions_tuple = []
    with open(file_path, "r") as file:
        content = yaml.safe_load(file)  # Load and parse the YAML file

        # Create a table for displaying the settings
        table_protocol = Table(show_header=True, header_style="bold cyan")
        table_protocol.add_column("State", style="dim", width=20)
        table_protocol.add_column("Event")
        table_protocol.add_column("Transition")

        row_content = []
        protocol_name = content.get("protocol_name", [])
        console.print(f"Protocol: {protocol_name}", style="bold cyan")
        states = content.get("states", [])
        transitions = content.get("transitions", [])

        for state in states:
            # Create the row content for each state
            row_content = [state]

            # Find all transitions where the 'from' state is the current state
            transition_info = []
            event_info = []
            for transition in transitions:
                if transition.get("from") == state:
                    transition_info.append(
                        f"({transition.get('from')} -> {transition.get('to')})"
                    )
                    event_info.append(transition.get("event", "N/A"))

                    protocol_transitions_tuple.append(
                        (
                            transition.get("from"),
                            transition.get("to"),
                            transition.get("event"),
                        )
                    )

            # If there are transitions, join them with a comma. Otherwise, display "No transitions"
            if transition_info:
                row_content.append(" | ".join(event_info))
                row_content.append(" | ".join(transition_info))

            else:
                row_content.append("No transitions")
                row_content.append("No event")

            # Add the row to the table
            table_protocol.add_row(*row_content)

        # Print the table with the settings
        console.print(table_protocol)
    return tuple(protocol_transitions_tuple)


def validate_protocol_file(file_path):
    """
    try:
        with open(file_path, "r") as file:
            content = yaml.safe_load(file)

        # Check for required keys
        required_keys = ["protocol_name", "states", "transitions"]
        for key in required_keys:
            if key not in content:
                console.print(f"[bold red]Error:[/bold red] Missing key: {key}")
                return False

        # Check if states is a non-empty list
        states = content["states"]
        if not isinstance(states, list) or len(states) < 1:
            console.print(
                "[bold red]Error:[/bold red] States should be a non-empty list"
            )
            return False

        # Check if transitions is a non-empty list
        transitions = content["transitions"]
        if not isinstance(transitions, list) or len(transitions) < 1:
            console.print(
                "[bold red]Error:[/bold red] Transitions should be a non-empty list"
            )
            return False

        # Check for duplicates in states
        if len(states) != len(set(states)):
            console.print("[bold red]Error:[/bold red] Duplicate states found")
            return False

        # Check for states with no transitions
        state_set = set(states)
        state_with_no_transitions = [
            state
            for state in states
            if not any(t["from"] == state for t in transitions)
        ]
        if state_with_no_transitions:
            console.print(
                f"[bold red]Error:[/bold red] States with no transitions: {', '.join(state_with_no_transitions)}"
            )
            return False

        # Check each transition for valid from/to states and non-empty events
        for transition in transitions:
            if not all(k in transition for k in ["from", "to", "event"]):
                console.print(
                    "[bold red]Error:[/bold red] Each transition must contain 'from', 'to', and 'event'"
                )
                return False
            if transition["from"] not in state_set or transition["to"] not in state_set:
                console.print(
                    f"[bold red]Error:[/bold red] Invalid state in transition: {transition}"
                )
                return False
            if not isinstance(transition["event"], str) or not transition["event"]:
                console.print(
                    f"[bold red]Error:[/bold red] Event must be a non-empty string in transition: {transition}"
                )
                return False

        # If all checks pass
        return True

    except Exception as e:
        console.print(f"[bold red]Error reading protocol file:[/bold red] {e}")
        return False
    """
    return True


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
                    f"The FSM ({machine}) is not infinite because one of the states is a deadlock."
                )
        # Print the table
        console.print(table_settings)
        return tuple(machines)


def update_machine_file(file_path):
    machines = file_path
    updated_machines = []
    for name, data in machines:
        data["actual_states"] = data[
            "Initial_global_state"
        ]  # put the actual states by the values of the inital states
        data["channel"] = []
        updated_machines.append((name, data))

    # Optional: print to verify
    console.print(updated_machines)
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
def lauch_simulation(machines_tuple, protocol_transitions_tuple):
    mode = str(input("Select simulation mode (M - Manual | A - Automatic): "))
    if mode == "M" or mode == "m":
        print("manual mod work in progress")

    elif mode == "A" or mode == "a":
        print("automatic mode work in proress")
        display_function(machines_tuple)
        # here have to check wich transition to choose and wich Tomachine have the required states

        # Randomly select a transition from protocol_transitions_tuple
        for random_transition in protocol_transitions_tuple:
            # Extract the transition details
            initial_global_state = random_transition[0]
            to_state = random_transition[1]
            event = random_transition[2]

            # Print the randomly selected transition
            # print(f"Random transition: {initial_global_state} -> {to_state}, Event: {event}")

            # Start selecting random machines
            match_found = False
            for _ in range(10):  # Limit the number of trials (10 tries)
                # Select two random machines from machines_tuple
                machine_name1, machine_state_1 = random.choice(machines_tuple)
                machine_name2, machine_state_2 = random.choice(machines_tuple)
                while (
                    machine_name2 == machine_name1
                ):  # Ensure the machines are not the same
                    machine_name2, machine_state_2 = random.choice(machines_tuple)

                # print(f"Machine 1: {machine_name1} with state: {machine_state_1}")
                # print(f"Machine 2: {machine_name2} with state: {machine_state_2}")

                # Check if machine 2's state matches the 'to_state' of the transition
                if machine_state_2 == to_state:
                    # console.print(
                    #   f"[bold yellow]Match found![/bold yellow] {machine_name2} state matches transition 'to_state': {to_state}"
                    # )
                    match_found = True
                    break  # Break if match is found

                # else:
                # print("No match. Trying again...")

            # If no match is found after 10 attempts, move to the next transition
            # if not match_found:
            # print(
            #    f"No match found after 10 attempts for transition: {initial_global_state} -> {to_state}. Moving to next transition."
            # )
            # continue  # Skip to the next transition

            # If a match is found, perform the action and break out of the transition loop
            fromMachine = machine_name1
            toMachine = machine_name2

            break  # Break after processing the transition

        machines_tuple = affect_display(
            machines_tuple, fromMachine, toMachine, random_transition
        )
        # console.print(machines_tuple)

        display_function(machines_tuple)
    else:
        console.print("[bold yellow]Please select a valid simulation mode[bold yellow]")
        lauch_simulation(machines_tuple, protocol_transitions_tuple)


def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(
        description="Simulator, executor for N protocol entities"
    )

    parser.add_argument(
        "-p",
        "--protocol",
        type=str,
        help="Path to the protocol file (in YAML extension)",
        required=True,
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
        # Check if the protocol file and settings file are the same
        if args.protocol == args.settings:
            raise ValueError("Protocol file and settings file cannot be the same.")
        # Validate both files have the correct extension
        for file_path in [args.protocol, args.settings]:
            if not file_path.endswith((".yaml", ".yml")):
                raise ValueError(
                    f"The file '{file_path}' is not a valid YAML file (must have .yaml or .yml extension)."
                )

        # Read the protocol YAML file
        if validate_protocol_file(args.protocol) and validate_settings_file(
            args.settings
        ):
            protocol_transitions_tuple = protocol_read(args.protocol)
            machines_tuple = settings_read(args.settings)
            machines_tuple = update_machine_file(machines_tuple)

            displayFSM(machines_tuple)

        # lauch_simulation(machines_tuple, protocol_transitions_tuple)

    except ValueError as e:
        # Catch invalid file extension or other ValueErrors
        console.print(f"[bold red]Error[/bold red]: {e}")
    except Exception as e:
        # Catch any unexpected errors
        console.print(f"[bold red]Error[/bold red]: {e}")


if __name__ == "__main__":
    main()
