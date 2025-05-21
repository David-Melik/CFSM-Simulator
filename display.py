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
import random

from rich.live import Live
from rich.layout import Layout
import time


console = Console()


# Helper definition


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
        stop_simulation = False
        n_run = 0
        automatic_run = 0

        if mode == "A":  # set number of automatic run until
            while True:
                try:
                    user_input_number_run = int(
                        input(
                            "🔁 Enter how many automatic steps to run before pausing and asking if you want to continue: "
                        )
                    )
                    if user_input_number_run <= 0:
                        print("⚠️ Please enter a positive number.")
                    else:
                        automatic_run_limit = user_input_number_run
                        break
                except ValueError:
                    print("❌ Invalid input. Please enter a valid integer.")

        while stop_simulation == False:
            option = 0
            choice_metadata = []

            table = Table(title="Possible transitions", box=MINIMAL)
            table.add_column("Choice", justify="center", style="cyan", no_wrap=True)
            table.add_column("FSM", justify="center", style="green")
            table.add_column("Type", justify="center", style="magenta")
            table.add_column("Transition", justify="center", style="yellow")

            # add to the table the possibility of transition
            for actual_machine, data in machines_settings:

                for element_states in range(len(data["States"])):
                    if data["States"][element_states][0] == data["actual_state"][0]:
                        data["States"][element_states][1] = 1

                # console.print(f"[bold blue]FSM: {actual_machine}[/bold blue]")

                # initalize
                transitions = data["Transitions"]
                machine_names = [name for name, _ in machines_settings]
                channel_info = []
                for _, data_element in machines_settings:
                    for key, value in data_element.items():
                        if key.startswith("Channel "):
                            channel_info.append((key, value))

                # console.print(f"ACTUAL CHANNEL WANT TO REMOVE {actual_machine}")
                for channel in channel_info[:]:
                    if (
                        channel[0].startswith((f"Channel {actual_machine} ->"))
                        or actual_machine not in channel[0]
                    ):

                        channel_info.remove(channel)
                        # console.print(f"REMOVED {channel}")

                    # console.print(channel)

                # List of tuples: (channel name, content)

                # check in all transition
                for transition in transitions:

                    if transition.get("from") == data["actual_state"][0]:

                        event_val = transition.get("event", "")

                        if event_val == "τ":
                            type_transition = "Silent"
                            event_content = event_val
                            option += 1

                            table.add_row(
                                f"{option }",
                                f"{actual_machine}",
                                f"{type_transition}",
                                f"{transition.get('from')} --{event_content}--> {transition.get('to')}",
                            )

                            choice_metadata.append(
                                {
                                    "option": option,
                                    "fsm": actual_machine,
                                    "type": type_transition,
                                    "transition": transition,
                                    "event": event_content,
                                }
                            )

                        elif event_val.startswith(("-")) or event_val.startswith(("!")):
                            # console.print("Hey sending signal ADD TO AVAILABLE ACTION")
                            type_transition = "Send"
                            event_content = event_val[1:]
                            channel_poiting = transition.get("channel")
                            option += 1

                            table.add_row(
                                f"{option }",
                                f"{actual_machine}",
                                f"{type_transition}",
                                f"{transition.get('from')} --{event_content}--> {transition.get('to')}",
                            )

                            choice_metadata.append(
                                {
                                    "option": option,
                                    "fsm": actual_machine,
                                    "type": type_transition,
                                    "transition": transition,
                                    "event": event_content,
                                    "channel_pointing": channel_poiting,
                                }
                            )
                        elif event_val.startswith(("+")) or event_val.startswith(("?")):
                            # console.print("HEY receiving signal")
                            type_transition = "Receving"
                            without_first_char = event_val[1:]
                            event_content = event_val[1:]

                            # Channel Machine B -> Machine A
                            # [('Channel Machine A -> Machine B', []), ('Channel Machine B -> Machine A', [])]
                            required_event_val = event_val[1:]
                            for channel in channel_info:
                                # console.print(channel)
                                # console.print(required_event_val)
                                if channel[1] and channel[1][-1] == required_event_val:
                                    # console.print("we find it")
                                    option += 1

                                    table.add_row(
                                        f"{option}",
                                        f"{actual_machine}",
                                        f"{type_transition}",
                                        f"{transition.get('from')} --{event_content}--> {transition.get('to')}",
                                    )

                                    choice_metadata.append(
                                        {
                                            "option": option,
                                            "fsm": actual_machine,
                                            "type": type_transition,
                                            "transition": transition,
                                            "event": event_content,
                                        }
                                    )

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
            n_run = n_run + 1
            display_function(machines_settings, table, n_run)
            choice = -1

            if option == 1:
                if n_run == 1:
                    console.print(
                        "[red bold]💥 Deadlock detected![/red bold] [yellow]No transitions are possible from the start (initial deadlock).[/yellow]"
                    )
                else:
                    console.print(
                        "[red bold]💥 Deadlock detected![/red bold] [yellow]No further transitions are possible from the current state.[/yellow]"
                    )

                console.print("[green]✅ Thank you for using our simulator![/green]")
                stop_simulation = True
                break

            elif mode == "S":
                while choice not in range(1, option + 1):
                    try:
                        choice = int(
                            input(
                                "Choose an action between what is proposed in the table: "
                            )
                        )
                        if choice not in range(1, option + 1):
                            console.print(
                                f"[red]Invalid choice. Please select a number between 1 and {option}.[/red]"
                            )
                    except ValueError:
                        console.print(
                            "[red]Invalid input. Please enter a number.[/red]"
                        )
            elif mode == "A":
                # Automatically choose a random action, excluding the stop option
                time.sleep(1)  # 500 milliseconds
                automatic_run = automatic_run + 1

                if automatic_run == automatic_run_limit:
                    automatic_run = 0
                    try:
                        user_input = (
                            input("Do you want to continue the simulation? (y/n): ")
                            .strip()
                            .lower()
                        )
                        if user_input not in ("y", "n"):
                            console.print(
                                "[red]Invalid choice. Please enter 'y' for yes or 'n' for no.[/red]"
                            )
                        elif user_input == "n":
                            console.print(
                                "[yellow]Simulation stopped by user.[/yellow]"
                            )
                            possible_non_executable_state(machines_settings)

                            console.print(
                                "[bold green]Thank you for using our simulator :)[/bold green]"
                            )
                            stop_simulation = True
                            break  # or return/exit depending on context
                    except Exception:
                        console.print(
                            "[red]Unexpected input. Please enter 'y' or 'n'.[/red]"
                        )

                choice = random.randint(1, option - 1)
                console.print(
                    f"[bold cyan]Automatic mode:[/bold cyan] randomly selected choice [green]{choice}[/green]"
                )

            if choice == option:
                possible_non_executable_state(machines_settings)
                console.print(
                    "[bold green]Thank you for using our simulator :)[/bold green]"
                )
                stop_simulation = True

            else:
                channel_info = []
                for _, data_element in machines_settings:
                    for key, value in data_element.items():
                        if key.startswith("Channel "):
                            channel_info.append((key, value))
                # console.print(f"try to apply {channel_info}")
                selected = next(
                    (item for item in choice_metadata if item["option"] == choice), None
                )
                if selected["type"] == "Silent":
                    # Just update the state
                    # console.print(selected)
                    # {'option': 1, 'fsm': 'Machine A', 'type': 'Send', 'transition': {'from': 'S1', 'to': 'S2', 'input': '-R', 'event': 'Sending signal R'}, 'input': 'R'}

                    for machine_name, data in machines_settings:
                        if machine_name == selected["fsm"]:
                            data["actual_state"][0] = selected["transition"]["to"]

                elif selected["type"] == "Send":
                    # Append to the correct channel
                    # console.print("HEY")
                    # console.print(selected)

                    for channel in channel_info:
                        # console.print(channel)
                        if channel[0].startswith(
                            (
                                f"Channel {selected['fsm']} -> {selected['channel_pointing']}"
                            )
                        ):

                            channel[1].append(selected["event"])
                            # console.print(f"was added{channel[1]}")

                    for machine_name, data in machines_settings:
                        if machine_name == selected["fsm"]:
                            data["actual_state"][0] = selected["transition"]["to"]

                elif selected["type"] == "Receving":
                    # console.print("appy receiving")
                    # Pop from the channel

                    # console.print("HEY")
                    event_val = selected["transition"]["event"]
                    required_event_val = event_val[1:]

                    for channel in channel_info[:]:

                        if channel[1] and channel[1][-1] == required_event_val:
                            channel[1].pop()
                            # console.print(f"was pop{channel[1]}")

                            # console.print(f"change to {data['actual_state'][0]} to {selected['transition']['to']}")
                            for machine_name, data in machines_settings:
                                if machine_name == selected["fsm"]:
                                    data["actual_state"][0] = selected["transition"][
                                        "to"
                                    ]

        # ┼ > ─ ╭ ╰ ╮ ╯
        #

        # then the from inital state -> to states

        # repeat the next state -> to sate
        return True
    except Exception as e:
        print("Error:", e)
        traceback.print_exc()


# ----------------------------
def possible_non_executable_state(machines_settings):
    possible_non_executable_state_list = []

    for name, data in machines_settings:
        for state_info in data["States"]:
            state_name, value = state_info
            if value == 0:
                possible_non_executable_state_list.append((name, state_name))

    if possible_non_executable_state_list:
        console.print(
            "[yellow bold]\n⚠️ Possible non-executable states detected:[/yellow bold]"
        )
        for machine_name, state in possible_non_executable_state_list:
            console.print(
                f" • FSM [cyan]{machine_name}[/cyan] has state [magenta]{state}[/magenta] set to 0"
            )
        console.print(
            "\n[bold red]❗ These states might be non-executable in the FSMs[/bold red]\n"
        )
    else:
        console.print(
            "[green]✅ Non-executable error is not present in this design.\n[/green]"
        )


def display_available_transition(machines_settings, machine_name):
    content_to_print = ""

    for name, data in machines_settings:
        if name == machine_name:

            inital_global_state = (data.get("Initial_global_state", []),)
            all_states = (data.get("States", []),)
            transitions = data.get("Transitions", [])

            # console.print(transitions)
            # content_to_print += f"[bold blue]FSM: {name}[/bold blue]\n"

            type = 0
            # type 1 -> one transition was available
            # type 2 -> multiple transition was available and the selected one has only one event
            # type 3 -> multiple transition was available and the selected one has multiple events available

            # initialize display
            transitionTo = []
            transitionToDisplay = []
            possible_event = []
            type = 0

            content_to_print += f"🔸 [bold]Current state:[/bold] [orange1]{data['actual_state'][0]}[/orange1]\n"

            # console.print(f"here allstates {allStates} and try to remove {focusState}")

            # check in all transition
            for transition in transitions:
                # search wich transition is available, by creating 1. a list of reachable state 2. and possible_event use to save event when only one transition
                if transition.get("from") == data["actual_state"][0]:
                    transitionToDisplay.append(
                        f"{transition.get('to')} with {transition.get('event')}"
                    )
                    transitionTo.append(f"{transition.get('to')}")
                    possible_event.append(f"{transition.get('event')}")

                    # when is the last state so if the fsm is infinite it should go back to initalState
            content_to_print += f"├─ Available transitions:\n"

            for t in transitionToDisplay:
                state, event_val = t.split(" with ")
                content_to_print += f"│   └─ [green]{state}[/green] via event [green]{event_val}[/green]\n"

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
        if 54 == len(machines_settings):

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

        console.print(Rule(f"Run n°{n_run}"))

        # List of machine names
        machine_names = [name for name, _ in machines_settings]

        # List of tuples: (channel name, content)
        channel_info = []
        for _, data_element in machines_settings:
            for key, value in data_element.items():
                if key.startswith("Channel "):
                    channel_info.append((key, value))

        panels = []

        for element in range(len(machines_settings)):
            content_to_print = display_available_transition(
                machines_settings, machine_names[element]
            )

            panel = Align.center(
                Panel(
                    align_text(content_to_print),
                    title=f"FSM {element + 1} ({machine_names[element]})",
                    width=50,
                    height=10,
                ),
                vertical="middle",
            )

            panels.append(panel)

        channel_panels = []

        for name, content in channel_info:
            formatted_content = ", ".join(content) if content else "[dim]Empty[/dim]"
            panel = Panel(
                align_text_left(formatted_content),
                title=name,
                border_style="yellow",
                height=4,
                width=40,
            )
            channel_panels.append(panel)

        panel4 = Align.center(table, vertical="middle")

        # Display FSM panels side by side
        fsm_panel_group = Columns(panels, expand=True)

        # Display channel panels below or above (stacked)
        channel_panel_group = Group(*channel_panels)

        console.print(Group(fsm_panel_group, channel_panel_group))

        # Row 2: 1 full-width panel (centered)
        console.print(Columns([panel4], expand=True))

    except Exception as e:
        print("Error:", e)
        traceback.print_exc()
