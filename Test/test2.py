import time


class LightFSM:
    def __init__(self):
        self.state = "OFF"

    def transition(self):
        if self.state == "OFF":
            self.state = "ON"
        else:
            self.state = "OFF"

    def __str__(self):
        return f"Light is {self.state}"


class ThermostatFSM:
    def __init__(self):
        self.state = "OFF"

    def transition(self):
        if self.state == "OFF":
            self.state = "HEATING"
        elif self.state == "HEATING":
            self.state = "COOLING"
        else:
            self.state = "OFF"

    def __str__(self):
        return f"Thermostat is {self.state}"


class SecuritySystemFSM:
    def __init__(self):
        self.state = "DISARMED"

    def transition(self):
        if self.state == "DISARMED":
            self.state = "ARMED"
        else:
            self.state = "DISARMED"

    def __str__(self):
        return f"Security System is {self.state}"


def simulate_fsm():
    light = LightFSM()
    thermostat = ThermostatFSM()
    security_system = SecuritySystemFSM()

    for _ in range(6):  # Simulate 6 transitions
        print(light)
        print(thermostat)
        print(security_system)

        # Transition states
        light.transition()
        thermostat.transition()
        security_system.transition()

        # Wait for a second before the next transition
        time.sleep(1)


if __name__ == "__main__":
    simulate_fsm()
