from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.align import Align


def N_Machine_Row(n):
    if n % 2 == 0:
        return n // 2
    elif n % 2 != 0:
        return (n + 1) // 2


def even(n):
    if n % 2 == 0:
        return True
    elif n % 2 != 0:
        return False


def align_text(text):
    text = Align.center(text, vertical="middle")
    return text


def affect_display(machines_tuple, fromMachine, toMachine, transition):
    initial_state = transition[0]
    to_state = transition[1]
    event = transition[2]
    print(event)

    display_link(
        machines_tuple,
        fromMachine,
        toMachine,
        initial_state,
        to_state,
        event,
    )

    machines_list = list(machines_tuple)

    for i, (machine_name, machine_state) in enumerate(machines_list):
        if machine_name == fromMachine:
            machines_list[i] = (machine_name, to_state)
            # print(f"Updated {machine_name} state to {to_state}")
            break

    # Convert the list back to a tuple
    machines_tuple = tuple(machines_list)

    return machines_tuple


def display_link(
    machines_tuple, fromMachine, toMachine, initial_state, to_state, event
):
    print(f"{to_state}")
    print(machines_tuple)
    machine_index = None
    for i, (machine_name, state) in enumerate(machines_tuple, start=1):
        if machine_name == fromMachine:
            machine_index = i
            break  # Stop once the machine is found
    rowNumber = N_Machine_Row(machine_index)

    numberMachine = len(machines_tuple)
    console = Console(width=80)
    layout = Layout()  # Create the layout
    numberOfRow = N_Machine_Row(numberMachine)

    layouts = [Layout(name=f"Row{i}") for i in range(1, numberOfRow + 1)]
    layout.split_column(*layouts)

    for i in range(1, numberOfRow + 1):

        layout[f"Row{i}"].size = 10
        layout[f"Row{i}"].split_row(
            Layout(name="left"),
            Layout(name="center"),
            Layout(name="right"),
        )
    j = 0
    for i in range(1, numberOfRow + 1):
        if j != numberMachine:

            machine_name, machine_state = machines_tuple[j]
            layout[f"Row{i}"]["left"].update(
                Panel(
                    align_text(
                        f"{machine_name}\n[bold yellow]state[/bold yellow]: {machine_state}"
                    )
                )
            )
            j = j + 1
            layout[f"Row{i}"]["center"].update(Text(""))
        if j != numberMachine:

            machine_name, machine_state = machines_tuple[j]
            layout[f"Row{i}"]["right"].update(
                Panel(
                    align_text(
                        f"{machine_name}\n[bold yellow]state[/bold yellow]: {machine_state}"
                    )
                )
            )
            j = j + 1

    if numberMachine < numberOfRow * 2:
        layout[f"Row{numberOfRow}"]["right"].update(Text(""))
    if j == machine_index:
        if even(machine_index):
            # droite
            layout[f"Row{rowNumber}"]["right"].update(
                Panel(
                    align_text(
                        f"{toMachine}\nFrom [bold yellow]{initial_state}[/bold yellow] state to:\n➔ [bold green]{to_state}[/bold green]"
                    ),
                    border_style="bold yellow",
                )
            )
    else:
        # gauche
        layout[f"Row{rowNumber}"]["left"].update(
            Panel(
                align_text(
                    f"{toMachine}\nFrom [bold yellow]{initial_state}[/bold yellow] state to:\n➔ [bold green]{to_state}[/bold green]"
                ),
                border_style="bold yellow",
            )
        )
    console.print(layout)

    blockLink01 = (align_text(f"{event}\n---------------->"),)

    blockLink02 = (align_text(f"{event}\n<----------------"),)

    blockLink03 = (align_text(f"{event}\n<----------------"),)
    arrow_upper_center = align_text(
        Text(
            "---------------->\ntransition 1",
            style="bold cyan",
        )
    )

    # layout["Row1"]["center"].update(arrow_upper_center)

    link_down_left = align_text(Text("|\n|\n|\n|\n|\n----->\n Transition 2"))

    # Put content inside the "left" part of "lower"
    # layout["Row2"]["center"].update(link_down_left)
    link_down_right = align_text(
        Text("    |\n    |\n    |\n    |\n    |    \n<----\n Transition 2")
    )
    # Put content inside the "right" part of "lower"
    layout["Row2"]["center"].update(blockLink01)
    # Print the layout

    return True


def display_function(machines_tuple):
    numberMachine = len(machines_tuple)
    console = Console(width=80)
    layout = Layout()  # Create the layout
    numberOfRow = N_Machine_Row(numberMachine)
    # Split the layout into an upper and lower part
    layouts = [Layout(name=f"Row{i}") for i in range(1, numberOfRow + 1)]
    layout.split_column(*layouts)  # Now split the column using the generated layouts

    for i in range(1, numberOfRow + 1):
        # Split the "lower" part into left and right columns
        layout[f"Row{i}"].size = 10
        layout[f"Row{i}"].split_row(
            Layout(name="left"),
            Layout(name="center"),
            Layout(name="right"),
        )
    j = 0
    for i in range(1, numberOfRow + 1):
        if j != numberMachine:
            machine_name, machine_state = machines_tuple[j]
            layout[f"Row{i}"]["left"].update(
                Panel(
                    align_text(
                        f"{machine_name}\n[bold yellow]state[/bold yellow]: {machine_state}"
                    )
                )
            )
            j = j + 1
            layout[f"Row{i}"]["center"].update(Text(""))
        if j != numberMachine:
            machine_name, machine_state = machines_tuple[j]
            layout[f"Row{i}"]["right"].update(
                Panel(
                    align_text(
                        f"{machine_name}\n[bold yellow]state[/bold yellow]: {machine_state}"
                    )
                )
            )
            j = j + 1
    if numberMachine < numberOfRow * 2:
        layout[f"Row{numberOfRow}"]["right"].update(Text(""))

    console.print(layout)
