import yaml
import argparse

# python -m pip install rich
from rich.console import Console
from rich.prompt import Prompt
from rich.style import Style

# Initialize the console for rich text output
console = Console()


def protocol_file(file_path):
    read_yaml_file(file_path)


def environment_file(file_path):
    read_yaml_file(file_path)


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
        "--environment",
        type=str,
        help="Path to the settings environment file (in YAML extension)",
        required=True,
    )

    # Parse the arguments
    args = parser.parse_args()

    try:
        # Check if the protocol file and environment file are the same
        if args.protocol == args.environment:
            raise ValueError("Protocol file and environment file cannot be the same.")
        # Validate both files have the correct extension
        for file_path in [args.protocol, args.environment]:
            if not file_path.endswith((".yaml", ".yml")):
                raise ValueError(
                    f"The file '{file_path}' is not a valid YAML file (must have .yaml or .yml extension)."
                )

        # Read the protocol YAML file
        protocol_file(args.protocol)
        # Read the environment settings YAML file
        environment_file(args.environment)

    except ValueError as e:
        # Catch invalid file extension or other ValueErrors
        console.print(f"[bold red]Error[/bold red]: {e}")
    except Exception as e:
        # Catch any unexpected errors
        console.print(f"[bold red]Error[/bold red]: {e}")


if __name__ == "__main__":
    main()
