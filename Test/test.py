from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout

# Create a console object to output to the terminal
console = Console()

# Create the panels
panel1 = Panel("Panel 1", border_style="green")
panel2 = Panel("Panel 2", border_style="blue")
panel3 = Panel("Panel 3", border_style="red")
panel4 = Panel("Panel 4", border_style="yellow")

# Create the layout with rows and columns
layout = Layout()

# Split the layout into two columns (left and right)
layout.split_row(
    Layout(name="left", size=20),  # Left column, fixed width of 20
    Layout(name="right", size=20),  # Right column, fixed width of 20
)

# Now split the "left" column into two rows (top and bottom)
layout["left"].split_column(
    Layout(name="top", size=5),  # First row (top) in the left column, height of 5
    Layout(
        name="bottom", size=5
    ),  # Second row (bottom) in the left column, height of 5
)

# Now split the "right" column into two rows (top and bottom)
layout["right"].split_column(
    Layout(name="top", size=5),  # First row (top) in the right column, height of 5
    Layout(
        name="bottom", size=5
    ),  # Second row (bottom) in the right column, height of 5
)

# Update the layout with the panels
layout["left"]["top"].update(panel1)
layout["left"]["bottom"].update(panel3)
layout["right"]["top"].update(panel2)
layout["right"]["bottom"].update(panel4)
# Create an arrow with the transition text
arrow_text = "[bold magenta]Transition Event 1 →[/bold magenta]"

# Place the arrow text between Panel 1 and Panel 2
layout["left"]["bottom"].update(arrow_text)

# Display the layout
console.print(layout)
