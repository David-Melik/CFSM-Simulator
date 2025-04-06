from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

# Create a console object to output to the terminal
console = Console(width=80)

# Create the layout
layout = Layout()

# Split the layout into an upper and lower part
layout.split_column(Layout(name="upper"), Layout(name="lower"))

# Split the "lower" part into left and right columns
layout["upper"].split_row(
    Layout(name="left"),
    Layout(name="center"),
    Layout(name="right"),
)
layout["upper"].size = 10
layout["lower"].split_row(
    Layout(name="left"),
    Layout(name="center"),
    Layout(name="right"),
)
layout["lower"].size = 10


def align_text(text):
    text = Align.center(text, vertical="middle")
    return text


layout["upper"]["left"].update(Panel(align_text("Machine 1")))
layout["upper"]["right"].update(Panel(align_text("Machine 2")))
layout["lower"]["center"].update(Panel(align_text("Machine 3")))


arrow_upper_center = align_text(
    Text(
        "---------------->\ntransition 1",
        style="bold cyan",
    )
)
layout["upper"]["center"].update(arrow_upper_center)


link_down_left = align_text(Text("|\n|\n|\n|\n|\n----->\n Transition 2"))

# Put content inside the "left" part of "lower"
layout["lower"]["left"].update(link_down_left)
link_down_right = align_text(
    Text("    |\n    |\n    |\n    |\n    |    \n<----\n Transition 2")
)

# Put content inside the "right" part of "lower"
layout["lower"]["right"].update(link_down_right)

# Print the layout
console.print(layout)
