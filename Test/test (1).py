import time


class TrafficLightFSM:
    def __init__(self):
        self.state = "RED"

    def transition(self):
        if self.state == "RED":
            self.state = "GREEN"
        elif self.state == "GREEN":
            self.state = "YELLOW"
        elif self.state == "YELLOW":
            self.state = "RED"

    def __str__(self):
        return f"Traffic Light is {self.state}"


class PedestrianSignalFSM:
    def __init__(self):
        self.state = "DON'T WALK"

    def transition(self):
        if self.state == "DON'T WALK":
            self.state = "WALK"
        elif self.state == "WALK":
            self.state = "DON'T WALK"

    def __str__(self):
        return f"Pedestrian Signal is {self.state}"


def simulate_fsm():
    traffic_light = TrafficLightFSM()
    pedestrian_signal = PedestrianSignalFSM()

    for _ in range(6):  # Simulate 6 transitions
        print(traffic_light)
        print(pedestrian_signal)

        # Transition states
        traffic_light.transition()
        pedestrian_signal.transition()

        # Wait for a second before the next transition
        time.sleep(1)


if __name__ == "__main__":
    simulate_fsm()
