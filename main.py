import yaml
import argparse

# python -m pip install rich
from rich.console import Console
from rich.prompt import Prompt
from rich.style import Style
from rich.table import Table

# Initialize the console for rich text output
console = Console()


def protocol_read(file_path):
    read_yaml_file(file_path)


def settings_read(file_path):
    read_yaml_file(file_path)
    # Print the settings in a table
    with open(file_path, "r") as file:
        content = yaml.safe_load(file)  # Load and parse the YAML file

        # Create a table for displaying the settings
        table_settings = Table(show_header=True, header_style="bold cyan")
        table_settings.add_column("Machine name", style="dim", width=12)
        table_settings.add_column("States")

        max_transition_number = 0

        for machine, machine_data in content.items():
            max_transition_number = max(
                max_transition_number, len(machine_data["Transitions"])
            )

        # Dynamically add columns for each transition
        for i in range(max_transition_number):
            table_settings.add_column(f"Transitions n°{i + 1}")

        for machine, machine_data in content.items():
            row_content = []
            row_content.append(machine)

            # Print states
            state_str = ", ".join(machine_data["States"])
            row_content.append(state_str)

            # Print transitions
            for transition in machine_data["Transitions"]:
                transition_info = f"event: {transition['event']} ({transition['from']} -> {transition['to']}) "
                row_content.append(transition_info)

            # Add row to the table
            table_settings.add_row(*row_content)

        # Print the table with the settings
        console.print(table_settings)


def read_yaml_file(file_path):
    # Open the YAML file and read its content
    with open(file_path, "r") as file:
        content = yaml.safe_load(file)  # Load and parse the YAML file

        # Print the content of the YAML file
        console.print("\nContent of the file:", style="bold cyan")
        console.print(content, style="italic green")


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
        protocol_read(args.protocol)
        # Read the settings settings YAML file
        settings_read(args.settings)

    except ValueError as e:
        # Catch invalid file extension or other ValueErrors
        console.print(f"[bold red]Error[/bold red]: {e}")
    except Exception as e:
        # Catch any unexpected errors
        console.print(f"[bold red]Error[/bold red]: {e}")


if __name__ == "__main__":
    main()
