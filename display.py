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


def display_link(FromMachine, ToMachine, Event):
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
    # layout["Row2"]["center"].update(link_down_right)
    # Print the layout

    return True


def align_text(text):
    text = Align.center(text, vertical="middle")
    return text


def display_function(numberMachine):
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
            layout[f"Row{i}"]["left"].update(Panel(align_text("NAME")))
            j = j + 1
            layout[f"Row{i}"]["center"].update(Text(""))
        if j != numberMachine:
            layout[f"Row{i}"]["right"].update(Panel(align_text("NAME")))
            j = j + 1
    if numberMachine < numberOfRow * 2:
        layout[f"Row{numberOfRow}"]["right"].update(Text(""))

    console.print(layout)
