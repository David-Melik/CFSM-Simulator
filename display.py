from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

console = Console()


# Helper definition
def linkSeperation(States, settings):
    # from "states" check how to is refered
    return True


def even(n):
    if n % 2 == 0:
        return True
    elif n % 2 != 0:
        return False


def align_text(text):
    text = Align.center(text, vertical="middle")
    return text


# show every machine withe actual states on !
def displayFSM(machines):

    # intial state

    for machine, data in machines:
        transitions = data["Transitions"]
        console.print(f"FSM: {machine}", style="bold cyan")
        initialState = " ".join(data["Initial_global_state"])
        allStates = data["States"]
        focusState = initialState
        allStates.remove(focusState)  # Remove 'S1' from wherever it is
        allStates.insert(0, focusState)  # Reinsert 'S1' at index 0

        numberOfRow = 1

        while (
            len(allStates) != 0
        ):  # allow to know for all states, how much transitions they have and to who !
            focusState = allStates[0]

            transitionTo = []
            possibleInput = []

            allStates.remove(focusState)

            console.print(f"the focus state is [orange1]{focusState}[/orange1]")

            for transition in transitions:
                console.print(f"allstate list {allStates}")

                if transition.get("from") == focusState:
                    transitionTo.append(
                        f"{transition.get('to')} with {transition.get('input')}"
                    )
                    possibleInput.append(f"{transition.get('input')}")
            if len(allStates) == 0:
                console.print(
                    f"[orange1]╰─>[/orange1] For {focusState} it can [orange1] go back to inital states [/orange1]{transitionTo} so the possible input are {possibleInput}"
                )
            else:
                console.print(
                    f"[orange1]╰─>[/orange1] For {focusState}  it can go to  {transitionTo} so the possible input are {possibleInput}"
                )
                # console.print(allStates)

            numberOfRow += 1

    # ┼ > ─ ╭ ╰ ╮ ╯
    #

    # then the from inital state -> to states

    # repeat the next state -> to sate
    display_function(machines)
    return True


def Channels(Machine, content):
    return True


def displayTablePossibility(settings):
    return True


def changeStateFSM(machine, states, settings):

    return True


# ----------------------------


def display_function(machines_tuple):
    numberMachine = len(machines_tuple)

    console = Console(width=80)
    layout = Layout()  # Create the layout
    numberOfRow = 3
    # Split the layout into an upper and lower part
    layouts = [Layout(name=f"Row{i}") for i in range(1, numberOfRow + 1)]
    layout.split_column(*layouts)  # Now split the column using the generated layouts

    console.print(numberOfRow)

    for i in range(1, numberOfRow + 1):
        # Split the "lower" part into left and right columns
        layout[f"Row{i}"].size = 5
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
                    align_text(f"[bold yellow]state[/bold yellow]: hey1"),
                    padding=(0, 0),
                )
            )
            j = j + 1
            layout[f"Row{i}"]["center"].update(Text(""))
        if j != numberMachine:
            machine_name, machine_state = machines_tuple[j]
            layout[f"Row{i}"]["right"].update(
                Panel(
                    align_text(f"[bold yellow]state[/bold yellow]: hey2"),
                    padding=(0, 0),
                )
            )
            j = j + 1
    if numberMachine < numberOfRow * 2:
        layout[f"Row{numberOfRow}"]["right"].update(Text(""))

    console.print(layout)
