from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
import time
import traceback


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
    try:
        for machine, data in machines:

            console.print(f"[bold blue]FSM: {machine}[/bold blue]")

            transitions = data["Transitions"]
            initialState = " ".join(data["Initial_global_state"])
            allStates = data["States"].copy()

            saveAllStates = data["States"].copy()

            focusState = initialState
            allStates.remove(focusState)  # Remove 'S1' from wherever it is
            allStates.insert(0, focusState)  # Reinsert 'S1' at index 0

            i = 0
            j = len(allStates) + 1
            type = 0
            # type 1 -> one transition was available
            # type 2 -> multiple transition was available and the selected one has only one input
            # type 3 -> multiple transition was available and the selected one has multiple inputs available

            while (
                j != 0
            ):  # allow to know for all states, how much transitions they have and to who !

                # when is for the first time use initalState
                if i == 0:
                    focusState = initialState
                    data["actual_state"] = focusState

                # when is not the first time
                else:
                    # remove duplicates
                    transitionToFiltered = []
                    transitionToFiltered = list(dict.fromkeys(transitionTo))

                    # when you have multiple transition for the next action
                    if len(transitionTo) > 1:
                        console.print(
                            f"⚠️  Multiple transitions detected ({len(transitionTo)})"
                        )
                        # check how much transition is possible for each reachable states
                        for transition in transitionToFiltered:
                            transitionCount = 0
                            transitionCount = transitionTo.count(transition)

                            console.print(
                                f"   └─ [bold]{transition}[/bold]: {transitionCount} path(s)"
                            )
                        # ask for wich one want to go (would be manual mode)
                        selectTransition = str(
                            input(
                                f"❓ Select the next state to transition to (e.g. S2): "
                            )
                        )
                        # Check if the choice is correct and if yes start to apply
                        if selectTransition in transitionToFiltered:
                            console.print(
                                f"[green]✔️  You selected a valid transition: {selectTransition}[/green]"
                            )
                            possibleInputMultiple = []
                            selectTransitionCount = 0

                            # recount again how much way you can go the the desired states
                            for transition in transitions:
                                if (
                                    transition.get("from") == focusState
                                    and transition.get("to") == selectTransition
                                ):
                                    selectTransitionCount = selectTransitionCount + 1
                                    possibleInputMultiple.append(
                                        f"{transition.get('input')}"
                                    )
                            # if their is multiple way to do the transition -> so it mean multiple input to change to the same state
                            if selectTransitionCount > 1:
                                # show what possible input is available
                                console.print(f"   └─ Possible inputs:")
                                for availableInput in possibleInputMultiple:

                                    console.print(
                                        f"    └─ [green]{availableInput}[/green]"
                                    )
                                # so until he choose one correct input
                                while True:
                                    # ask wich input he want
                                    selectOfMultipleTransition = str(
                                        input(
                                            f"❓ Multiple paths to S2 — select input (e.g. +a): "
                                        )
                                    )
                                    # check if it is a correct input if yes it will apply it and move on
                                    if (
                                        selectOfMultipleTransition
                                        in possibleInputMultiple
                                    ):
                                        console.print(
                                            f"[green]✔️  You selected a valid inputs: {selectOfMultipleTransition}[/green]"
                                        )
                                        data["channel"].append(
                                            selectOfMultipleTransition
                                        )
                                        tmp = data["channel"]
                                        console.print(
                                            f"├─ Applied the transistion selected"
                                        )

                                        console.print(
                                            f"📥 Channel: [green]{tmp}[/green]"
                                        )
                                        type = 3
                                        break
                                    else:
                                        # here it mean was not a correct input
                                        console.print(
                                            f"[red]❌ '{selectOfMultipleTransition}' is not a valid option. Valid options: {possibleInputMultiple}[/red]"
                                        )
                            # it mean that the state choosen have only one input available
                            else:
                                if type != 3:
                                    console.print(
                                        f"we use the only input available {possibleInputMultiple}"
                                    )

                                    data["channel"].append(possibleInputMultiple[0])
                                    tmp = data["channel"]

                                    # for case (one input/multiple input) when choosen apply the choice
                                    focusState = selectTransition
                                    data["actual_state"] = selectTransition
                                    # tmp = data["actual_state"]
                                    # console.print(f"actual_state: {tmp}")
                                    console.print(
                                        f"├─ Applied the transistion selected"
                                    )
                                    console.print(f"📥 Channel: [green]{tmp}[/green]")

                        else:
                            # here mean that the state choosen is not correct
                            console.print(
                                f"[red]❌ '{selectTransition}' is not a valid option. Valid options: {transitionToFiltered}[/red]"
                            )

                    # when you have only one transition available it do automaticelly
                    else:
                        if type != 2 or type != 3:
                            focusState = transitionTo[0]
                            data["actual_state"] = focusState
                            # tmp = data["actual_state"]
                            # console.print(f"actual_state: {tmp} {focusState}")
                            data["channel"].append(possibleInput[0])
                            tmp = data["channel"]
                            console.print(f"├─ Applied the only transistion available")
                            console.print(f"📥 Channel: [green]{tmp}[/green]")

                # console.print(machines)

                transitionTo = []
                transitionToDisplay = []
                possibleInput = []

                # console.print(f"j is {j}")
                # console.print(f"all state {allStates}")

                console.print(f"\n🔸 Current state: [orange1]{focusState}[/orange1]")

                # console.print(f"here allstates {allStates} and try to remove {focusState}")

                # reformat focusState to avoid error
                focusState = focusState.strip()

                # remove the actual focusState in order to be able to check for the next available transition
                if focusState in allStates:
                    allStates.remove(focusState)
                # else:
                # console.print(f"[red]⚠️ '{focusState}' not found in {allStates}[/red]")

                for transition in transitions:
                    # search wich transition is available, by creating 1. a list of reachable state 2. and possibleInput use to save input when only one transition
                    if transition.get("from") == focusState:
                        transitionToDisplay.append(
                            f"{transition.get('to')} with {transition.get('input')}"
                        )
                        transitionTo.append(f"{transition.get('to')}")
                        possibleInput.append(f"{transition.get('input')}")

                # when is the last state so if the fsm is infinite it should go back to initalState
                if len(allStates) == 0:

                    console.print(
                        f"├─ Available transitions: [italic](can go back to intial states)[/italic]"
                    )

                    for t in transitionToDisplay:
                        state, input_val = t.split(" with ")
                        console.print(
                            f"│   └─ [green]{state}[/green] via input [green]{input_val}[/green]"
                        )

                # it show all the next avalaible transition multiple or single
                else:
                    console.print(f"├─ Available transitions:")

                    for t in transitionToDisplay:
                        state, input_val = t.split(" with ")
                        console.print(
                            f"│   └─ [green]{state}[/green] via input [green]{input_val}[/green]"
                        )

                # console.print(allStates)

                # till infinity
                i = i + 1
                j = j - 1

                if j == 0:
                    tmp = data["actual_state"]
                    console.print(f"acutual state {tmp} and inital {initialState}")
                    console.print("\n❓ Continue the simulation? (y/n):", style="bold")
                    console.print(
                        "(will go to next machine or stop if none is left)",
                        style="italic dim",
                    )
                    continueSimulation = input("> ")
                    if continueSimulation == "y":
                        focusState = initialState
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
    except Exception as e:
        print("Error:", e)
        traceback.print_exc()


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
