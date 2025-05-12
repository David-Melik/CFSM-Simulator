from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
import time


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
        allStates = data["States"].copy()
        saveAllStates = data["States"].copy()

        focusState = initialState
        allStates.remove(focusState)  # Remove 'S1' from wherever it is
        allStates.insert(0, focusState)  # Reinsert 'S1' at index 0

        i = 0
        j = len(allStates) + 1

        while (
            j != 0
        ):  # allow to know for all states, how much transitions they have and to who !
            if i == 0:
                focusState = allStates[0]
            else:
                console.print(transitionTo)
                transitionToFiltered = []
                transitionToFiltered = list(
                    dict.fromkeys(transitionTo)
                )  # remove duplicates

                if len(transitionTo) > 1:
                    console.print(
                        f"⚠️ their is {len(transitionTo)} transitions possibles ⚠️"
                    )
                    for transition in transitionToFiltered:
                        transitionCount = 0
                        transitionCount = transitionTo.count(transition)
                        console.print(
                            f"[green]─>[/green]their is {transitionCount} transitions possibles to go to {transition}"
                        )
                    selectTransition = str(
                        input(
                            f"Select the following state of the next transition you want to go (eg: S2): "
                        )
                    )
                    if selectTransition in transitionToFiltered:
                        console.print(
                            f"[green]✔️ You selected a valid transition: {selectTransition}[/green]"
                        )
                        possibleInputMultiple = []
                        selectTransitionCount = 0

                        for transition in transitions:
                            if (
                                transition.get("from") == focusState
                                and transition.get("to") == selectTransition
                            ):
                                selectTransitionCount = selectTransitionCount + 1
                                possibleInputMultiple.append(
                                    f"{transition.get('input')}"
                                )

                        if selectTransitionCount > 1:
                            for i in possibleInputMultiple:
                                console.print(
                                    f"[green]─>[/green] possible with inputs {i}"
                                )

                            while True:
                                selectOfMultipleTransition = str(
                                    input(
                                        f"Their are multiple way to go to {selectTransition} Select the following transition you want to use by their input (eg: a+):"
                                    )
                                )
                                if selectOfMultipleTransition in possibleInputMultiple:
                                    console.print(
                                        f"[green]✔️ You selected a valid inputs: {selectOfMultipleTransition}[/green]"
                                    )
                                    console.print(
                                        "will be added in the channel of the machine"
                                    )  # channel add it
                                    break
                                else:
                                    console.print(
                                        f"[red]❌ '{selectOfMultipleTransition}' is not a valid option. Valid options: {possibleInputMultiple}[/red]"
                                    )
                        else:
                            console.print(
                                f"we use the only input available {possibleInputMultiple}"
                            )
                            console.print("will be added in the channel of the machine")

                        focusState = selectTransition
                    else:
                        console.print(
                            f"[red]❌ '{selectTransition}' is not a valid option. Valid options: {transitionToFiltered}[/red]"
                        )

                else:
                    focusState = transitionTo[0]
            # focusState = transitionTo[0]

            transitionTo = []
            transitionToDisplay = []
            possibleInput = []
            i = i + 1

            console.print(f"the focus state is [orange1]{focusState}[/orange1]")

            # console.print(f"here allstates {allStates} and try to remove {focusState}")
            focusState = focusState.strip()

            if focusState in allStates:
                allStates.remove(focusState)
            # else:
            # console.print(f"[red]⚠️ '{focusState}' not found in {allStates}[/red]")

            for transition in transitions:

                if transition.get("from") == focusState:
                    transitionToDisplay.append(
                        f"{transition.get('to')} with {transition.get('input')}"
                    )
                    transitionTo.append(f"{transition.get('to')}")
                    possibleInput.append(f"{transition.get('input')}")

            if len(allStates) == 0:
                console.print(
                    f"[orange1]╰─>[/orange1] For {focusState} it can [orange1] go back to inital states [/orange1]{transitionToDisplay} so the possible input are {possibleInput}"
                )
            else:
                console.print(
                    f"[orange1]╰─>[/orange1] For {focusState}  it can go to  {transitionToDisplay} so the possible input are {possibleInput}"
                )
                # console.print(allStates)

            j = j - 1

            # till infinity

            if j == 0:
                continueSimulation = str(
                    input(
                        "Continue the simulation (y)/(n) -> go to next machine or stop if none is left): "
                    )
                )
                if continueSimulation == "y":
                    print("hey", initialState)
                    focusState = initialState
                    console.print(saveAllStates)
                    allStates = saveAllStates.copy()
                    allStates.remove(focusState)  # Remove 'S1' from wherever it is
                    allStates.insert(0, focusState)  # Reinsert 'S1' at index 0
                    i = 0
                    j = len(allStates) + 1

    # ┼ > ─ ╭ ╰ ╮ ╯
    #

    # then the from inital state -> to states

    # repeat the next state -> to sate
    # display_function(machines)
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
