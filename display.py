from typing_extensions import Required
from rich.console import Console, Group
from rich.box import *
from rich.rule import Rule
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
def simulation(machines_settings, mode):
    try:
        option = 0
        n_run = 1
        choice_metadata = []

        table = Table(title="Possible transitions", box=MINIMAL)
        table.add_column("Choice", justify="center", style="cyan", no_wrap=True)
        table.add_column("FSM", justify="center", style="green")
        table.add_column("Type", justify="center", style="magenta")
        table.add_column("Transition", justify="center", style="yellow")

        # add to the table the possibility of transition
        for actual_machine, data in machines_settings:

            console.print(f"[bold blue]FSM: {actual_machine}[/bold blue]")

            # initalize
            transitions = data["Transitions"]
            machine_names = [name for name, _ in machines_settings]

            # List of tuples: (channel name, content)
            channel_info = []
            for _, data_element in machines_settings:
                for key, value in data_element.items():
                    if key.startswith("Channel "):
                        channel_info.append((key, value))

            console.print(f"ACTUAL CHANNEL WANT TO REMOVE {actual_machine}")
            for channel in channel_info[:]:
                if (
                    channel[0].startswith((f"Channel {actual_machine} ->"))
                    or actual_machine not in channel[0]
                ):

                    channel_info.remove(channel)
                    console.print(f"REMOVED {channel}")

            # check in all transition
            for transition in transitions:

                if transition.get("from") == data["actual_state"][0]:

                    input_val = transition.get("input", "")

                    if input_val == "τ":
                        type_transition = "Silent"
                        input_content = input_val
                        option += 1

                        table.add_row(
                            f"{option }",
                            f"{actual_machine}",
                            f"{type_transition}",
                            f"{transition.get('from')} --{input_content}--> {transition.get('to')}",
                        )

                        choice_metadata.append(
                            {
                                "option": option,
                                "fsm": actual_machine,
                                "type": type_transition,
                                "transition": transition,
                                "input": input_content,
                            }
                        )

                    elif input_val.startswith(("-")) or input_val.startswith(("!")):
                        console.print("Hey sending signal ADD TO AVAILABLE ACTION")
                        type_transition = "Send"
                        input_content = input_val[1:]
                        option += 1

                        table.add_row(
                            f"{option }",
                            f"{actual_machine}",
                            f"{type_transition}",
                            f"{transition.get('from')} --{input_content}--> {transition.get('to')}",
                        )

                        choice_metadata.append(
                            {
                                "option": option,
                                "fsm": actual_machine,
                                "type": type_transition,
                                "transition": transition,
                                "input": input_content,
                            }
                        )
                    elif input_val.startswith(("+")) or input_val.startswith(("?")):
                        console.print("HEY receiving signal")
                        type_transition = "Receving"
                        without_first_char = input_val[1:]
                        input_content = input_val[1:]

                        # Channel Machine B -> Machine A
                        # [('Channel Machine A -> Machine B', []), ('Channel Machine B -> Machine A', [])]
                        required_input_val = "-" + input_val[1:]
                        for channel in channel_info:
                            console.print(channel)
                            if channel[1] and channel[1][-1] == required_input_val:
                                option += 1

                                table.add_row(
                                    f"{option}",
                                    f"{actual_machine}",
                                    f"{type_transition}",
                                    f"{transition.get('from')} --{input_content}--> {transition.get('to')}",
                                )

                                choice_metadata.append(
                                    {
                                        "option": option,
                                        "fsm": actual_machine,
                                        "type": type_transition,
                                        "transition": transition,
                                        "input": input_content,
                                    }
                                )

                                # channel[1].pop()
                                # console.print(f"was pop{channel[1]}")

                                # console.print(
                                #    f"change to {data['actual_state'][0]} to {transition.get('to')}"
                                # )
                                # data["actual_state"][0] = transition.get("to")
                                # do the change

                        # now have to check if inside their is the sending signal corresponding to the receving signal asked

                        # List of machine names

                        # check in the correct channel

        option += 1
        table.add_row(
            f"{option}",
            "---",
            "Stop simulation",
            "---",
        )
        display_function(machines_settings, table, 1)
        n_run += 1

        choice = int(input("Choose a action between what is proposed in the table: "))

        if choice == option:
            console.print("Thank you to use our simulator :)")
            return True
        else:
            selected = next(
                (item for item in choice_metadata if item["option"] == choice), None
            )
            if selected["type"] == "Silent":
                # Just update the state
                console.print(selected)

            elif selected["type"] == "Send":
                # Append to the correct channel
                console.print("HEY")
                console.print(selected)

            elif selected["type"] == "Receving":
                # Pop from the channel
                console.print("HEY")

        # ┼ > ─ ╭ ╰ ╮ ╯
        #

        # then the from inital state -> to states

        # repeat the next state -> to sate
        return True
    except Exception as e:
        print("Error:", e)
        traceback.print_exc()


# ----------------------------


def display_available_transition(machines_settings, machine_name):
    content_to_print = ""

    for name, data in machines_settings:
        if name == machine_name:

            inital_global_state = (data.get("Initial_global_state", []),)
            all_states = (data.get("States", []),)
            transitions = data.get("Transitions", [])

            # console.print(transitions)
            content_to_print += f"[bold blue]FSM: {name}[/bold blue]\n"

            type = 0
            # type 1 -> one transition was available
            # type 2 -> multiple transition was available and the selected one has only one input
            # type 3 -> multiple transition was available and the selected one has multiple inputs available

            # initialize display
            transitionTo = []
            transitionToDisplay = []
            possibleInput = []
            type = 0

            content_to_print += f"🔸 [bold]Current state:[/bold] [orange1]{data['actual_state'][0]}[/orange1]\n"

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
                    content_to_print += f"├─ Available transitions:\n"

                    for t in transitionToDisplay:
                        state, input_val = t.split(" with ")
                        content_to_print += f"│   └─ [green]{state}[/green] via input [green]{input_val}[/green]\n"

            # if multiple transition is available -> APPLY
            # type 2 and type 3

        # if len(transitionTo) > 1:
        #     # remove duplicates
        #     transitionToFiltered = []
        #     transitionToFiltered = list(dict.fromkeys(transitionTo))
        #     content_to_print += (
        #         f"⚠️  Multiple transitions detected ({len(transitionTo)})\n"
        #     )
        #     # check how much transition is possible for each reachable states
        #     for transition in transitionToFiltered:
        #         transitionCount = 0
        #         transitionCount = transitionTo.count(transition)

        #         content_to_print += (
        #             f"   └─ [bold]{transition}[/bold]: {transitionCount} path(s)\n"
        #         )

    # ┼ > ─ ╭ ╰ ╮ ╯
    #

    return content_to_print


def display_function(machines_settings, table, n_run):

    try:
        if 2 == len(machines_settings):

            console.print(Rule(f"Run n°{n_run}"))

            # List of machine names
            machine_names = [name for name, _ in machines_settings]

            # List of tuples: (channel name, content)
            channel_info = []
            for _, data_element in machines_settings:
                for key, value in data_element.items():
                    if key.startswith("Channel "):
                        channel_info.append((key, value))

            content_to_print = display_available_transition(
                machines_settings, machine_names[0]
            )

            panel1 = Align.center(
                Panel(
                    align_text(content_to_print),
                    title="FSM 1",
                    width=50,
                    height=10,
                ),
                vertical="middle",
            )

            content_channel_1 = ", ".join(channel_info[0][1])
            content_channel_2 = ", ".join(channel_info[1][1])

            panel2 = Align.center(
                Group(
                    Panel(
                        align_text_left(f"{content_channel_1}"),
                        title=channel_info[0][0],
                        border_style="yellow",
                        height=4,
                        width=40,
                    ),
                    Panel(
                        align_text_right(f"{content_channel_2}"),
                        title=channel_info[1][0],
                        border_style="yellow",
                        height=4,
                        width=40,
                    ),
                ),
                vertical="middle",
            )

            content_to_print = display_available_transition(
                machines_settings, machine_names[1]
            )
            panel3 = Align.center(
                Panel(
                    align_text(content_to_print),
                    title="FSM 2",
                    width=50,
                    height=10,
                ),
                vertical="middle",
            )

            panel4 = Align.center(table, vertical="middle")

            console.print(Columns([panel1, panel2, panel3], expand=True))

            # Row 2: 1 full-width panel (centered)
            console.print(Columns([panel4], expand=True))

        if 3 == len(machines_settings):
            console.print("work in progress")

        if len(machines_settings) != 2 and len(machines_settings) != 3:
            console.print(len(machines_settings))
            console.print("do not support that number of FSM")

    except Exception as e:
        print("Error:", e)
        traceback.print_exc()
