from rich.console import Console, Group
from rich.layout import Layout
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich.align import Align
from rich.table import Table
from rich import padding, print
from rich.layout import Layout
import time
import traceback

from rich.live import Live
from rich.layout import Layout
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


def align_text_right(text):
    text = Align.right(text, vertical="middle")
    return text


def align_text_left(text):
    text = Align.left(text, vertical="middle")
    return text


# show every machine withe actual states on !
def displayFSM(machines):
    try:
        for machine, data in machines:

            console.print(f"[bold blue]FSM: {machine}[/bold blue]")

            # initalize
            transitions = data["Transitions"]
            allStates = data["States"].copy()

            # saveAllStates = data["States"].copy()

            countDown = 0
            i = 0
            j = len(allStates) + 1
            type = 0
            # type 1 -> one transition was available
            # type 2 -> multiple transition was available and the selected one has only one input
            # type 3 -> multiple transition was available and the selected one has multiple inputs available

            while (
                j != 0
            ):  # allow to know for all states, how much transitions they have and to who !

                # console.print(machines)

                # initialize display
                transitionTo = []
                transitionToDisplay = []
                possibleInput = []
                type = 0
                countDown = countDown + 1

                # console.print(f"j is {j}")
                # console.print(f"all state {allStates}")

                console.print(
                    f"\n🔸 Current state: [orange1]{data['actual_state'][0]}[/orange1]"
                )

                # console.print(f"here allstates {allStates} and try to remove {focusState}")

                # check in all transition
                for transition in transitions:
                    # search wich transition is available, by creating 1. a list of reachable state 2. and possibleInput use to save input when only one transition
                    if transition.get("from") == data["actual_state"][0]:
                        transitionToDisplay.append(
                            f"{transition.get('to')} with {transition.get('input')}"
                        )
                        transitionTo.append(f"{transition.get('to')}")
                        possibleInput.append(f"{transition.get('input')}")

                # when is the last state so if the fsm is infinite it should go back to initalState
                if transition.get("to") == data["actual_state"]:

                    console.print(
                        f"├─ Available transitions: [italic](can go back to intial states)[/italic]"
                    )

                    # it show all the next avalaible transition multiple or single
                else:
                    console.print(f"├─ Available transitions:")

                    for t in transitionToDisplay:
                        state, input_val = t.split(" with ")
                        console.print(
                            f"│   └─ [green]{state}[/green] via input [green]{input_val}[/green]"
                        )

                # if multiple transition is available -> APPLY
                # type 2 and type 3
                console.print(f"hey {transitionTo}")

                if len(transitionTo) > 1:
                    # remove duplicates
                    transitionToFiltered = []
                    transitionToFiltered = list(dict.fromkeys(transitionTo))
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
                        input(f"❓ Select the next state to transition to (e.g. S2): ")
                    )
                    # Check if the choice is correct and if yes start to apply
                    if selectTransition in transitionToFiltered:
                        console.print(
                            f"[green]✔️  You selected a valid transition: {selectTransition}[/green]"
                        )
                        possibleInputMultiple = []
                        counterOfSelectedTransition = 0

                        # recount again how much way you can go the the desired states
                        for transition in transitions:
                            if (
                                transition.get("from") == data["actual_state"][0]
                                and transition.get("to") == selectTransition
                            ):
                                counterOfSelectedTransition = (
                                    counterOfSelectedTransition + 1
                                )
                                possibleInputMultiple.append(
                                    f"{transition.get('input')}"
                                )
                        # if their is multiple way to do the transition -> so it mean multiple input to change to the same state
                        # for type 3
                        if counterOfSelectedTransition > 1:
                            # show what possible input is available
                            console.print(f"   └─ Possible inputs:")
                            for availableInput in possibleInputMultiple:
                                console.print(f"    └─ [green]{availableInput}[/green]")
                            # so until he choose one correct input
                            exit = True
                            while exit == True:
                                # ask wich input he want
                                selectedInputOfMultiple = str(
                                    input(
                                        f"❓ Multiple paths to S2 — select input (e.g. +a): "
                                    )
                                )
                                # check if it is a correct input if yes it will apply it and move on
                                if selectedInputOfMultiple in possibleInputMultiple:
                                    console.print(
                                        f"[green]✔️  You selected a valid inputs: {selectedInputOfMultiple}[/green]"
                                    )
                                    data["channel"].append(selectedInputOfMultiple)
                                    tmp = data["channel"]
                                    console.print(
                                        f"├─ Applied the transistion selected"
                                    )
                                    data["actual_state"][0] = selectTransition
                                    console.print(
                                        f"actual state = {data['actual_state']}"
                                    )

                                    console.print(f"📥 Channel: [green]{tmp}[/green]")
                                    type = 3
                                    console.print(f"type is {type}")
                                    exit = True
                                else:
                                    # here it mean was not a correct input
                                    console.print(
                                        f"[red]❌ '{selectedInputOfMultiple}' is not a valid option. Valid options: {possibleInputMultiple}[/red]"
                                    )
                        # it mean that the state choosen have only one input available
                        # for type 2
                        else:
                            console.print(
                                f"we use the only input available {possibleInputMultiple}"
                            )

                            data["channel"].append(possibleInputMultiple[0])
                            tmp = data["channel"]

                            # for case (one input/multiple input) when choosen apply the choice
                            data["actual_state"][0] = selectTransition
                            console.print(f"actual state = {data['actual_state']}")
                            # tmp = data["actual_state"]
                            # console.print(f"actual_state: {tmp}")
                            console.print(f"├─ Applied the transistion selected")
                            console.print(f"📥 Channel: [green]{tmp}[/green]")
                            type = 2
                            console.print(f"type is {type}")

                    else:
                        # here mean that the state choosen is not correct
                        console.print(
                            f"[red]❌ '{selectTransition}' is not a valid option. Valid options: {transitionToFiltered}[/red]"
                        )

                # when you have only one transition available it do automaticelly
                # for type = 0
                else:
                    console.print(transitionTo)

                    data["actual_state"][0] = transitionTo[0]
                    console.print(f"actual state = {data['actual_state']}")
                    # tmp = data["actual_state"]
                    # console.print(f"actual_state: {tmp} {focusState}")
                    data["channel"].append(possibleInput[0])
                    console.print(f"├─ Applied the only transistion available")
                    console.print(f"📥 Channel: [green]{data['channel']}[/green]")
                    type = 1
                    console.print(f"type is {type}")

                    # till infinity

                if (
                    countDown != 1
                    and data["actual_state"][0] == data["Initial_global_state"][0]
                ):
                    console.print(machines)
                    tmp = data["actual_state"]
                    console.print("\n❓ Continue the simulation? (y/n):", style="bold")
                    console.print(
                        "(will go to next machine or stop if none is left)",
                        style="italic dim",
                    )
                    continueSimulation = input("> ")
                    if continueSimulation == "y":
                        data["actual_state"][0] = data["Initial_global_state"][0]
                        countDown = 0
                        allStates = data["States"].copy()

        # ┼ > ─ ╭ ╰ ╮ ╯
        #

        # then the from inital state -> to states

        # repeat the next state -> to sate
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
    try:
        numberMachine = len(machines_tuple)
        panel1 = Panel("Left Panel Content", title="Left", border_style="blue")
        panel2 = Panel("Right Panel Content", title="Right", border_style="green")

        # Print side-by-side
        console.print(Columns([panel1, panel2]))

        while True:
            layout = Layout()
            numberOfRow = 3
            layouts = [Layout(name=f"Row{i}") for i in range(1, numberOfRow + 1)]
            layout.split_column(*layouts)

            layout[f"Row{1}"].split_row(
                Layout(name="left"),
                Layout(name="center"),
                Layout(name="right"),
            )

            i = 1
            layout[f"Row{i}"]["left"].update(
                Panel(
                    f"[bold blue]Machine A[/bold blue]\n[bold yellow]state[/bold yellow]: hey1",
                    title="FSM 2",
                )
            )
            layout[f"Row{i}"]["center"].update(
                Align.center(
                    Group(
                        Panel(
                            f"[bold yellow]state[/bold yellow]: hey1",
                            title="Channel A <- B",
                            border_style="yellow",
                            height=4,
                            width=30,
                        ),
                        Panel(
                            f"[bold yellow]state[/bold yellow]: hey2",
                            title="Channel A -> B",
                            border_style="yellow",
                            height=4,
                            width=30,
                        ),
                    ),
                    vertical="middle",
                )
            )
            layout[f"Row{i}"]["right"].update(
                Panel(
                    f"[bold blue]Machine B[/bold blue]\n[bold yellow]Actual state[/bold yellow]: hey2\n├─ Available transitions:\n│   └─ S2 via input -R\n│   └─ S1 via input +A",
                    title="FSM 1",
                )
            )

            table = Table(title="FSM Transition Table")
            table.add_column("Choice", justify="center", style="cyan", no_wrap=True)
            table.add_column("FSM", justify="center", style="green")
            table.add_column("Type", justify="center", style="magenta")
            table.add_column("Transition", justify="center", style="yellow")
            table.add_row("1", "Machine A", "Send", "S1 --a--> S2")
            table.add_row("2", "Machine B", "Receive", "S2 <--a-- S1")
            table.add_row("3", "Machine A", "Internal", "S2 --b--> S3")

            layout[f"Row{2}"].update(table)

            with Live(layout, refresh_per_second=10, screen=False, console=console):
                time.sleep(1.5)  # Let layout be visible for a short moment

            # Ask the user if they want to continue
            answer = input("❓ Continue the simulation? (y/n): ").strip().lower()
            if answer == "n":
                break

        return True
    except Exception as e:
        print("Error:", e)
        traceback.print_exc()
