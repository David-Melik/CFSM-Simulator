from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# Create a console object for rendering
console = Console()

# Create rich text content
text = Text("This is a vertically centered panel with rich text!", style="bold magenta")

# Calculate the necessary padding for vertical centering
# This assumes the terminal height is 20, you can adjust it accordingly
terminal_height = 20
text_height = text.splitlines().__len__()

top_padding = (terminal_height - text_height) // 2
bottom_padding = terminal_height - text_height - top_padding

# Create the panel with vertical padding
panel = Panel(text, expand=True, padding=(top_padding, 0, bottom_padding, 0))

# Render the panel to the console
console.print(panel)
