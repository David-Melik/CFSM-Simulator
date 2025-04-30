import time
import random


class SenderFSM:
    def __init__(self):
        self.state = "READY"

    def send(self):
        if self.state == "READY":
            print("Sender: Sending message...")
            self.state = "SENDING"
            time.sleep(1)  # Simulate time taken to send
            self.state = "READY"
            print("Sender: Message sent.")
        else:
            print("Sender: Cannot send, not ready.")

    def __str__(self):
        return f"Sender is {self.state}"


class ReceiverFSM:
    def __init__(self):
        self.state = "WAITING"

    def receive(self):
        if self.state == "WAITING":
            print("Receiver: Waiting for message...")
            time.sleep(1)  # Simulate waiting time
            if random.choice([True, False]):  # Simulate message received or lost
                self.state = "RECEIVED"
                print("Receiver: Message received.")
            else:
                print("Receiver: Message lost.")
            self.state = "WAITING"  # Reset to waiting state
        else:
            print("Receiver: Cannot receive, not in waiting state.")

    def __str__(self):
        return f"Receiver is {self.state}"


class ConnectionManagerFSM:
    def __init__(self):
        self.state = "DISCONNECTED"

    def connect(self):
        if self.state == "DISCONNECTED":
            self.state = "CONNECTED"
            print("Connection Manager: Connected.")
        else:
            print("Connection Manager: Already connected.")

    def disconnect(self):
        if self.state == "CONNECTED":
            self.state = "DISCONNECTED"
            print("Connection Manager: Disconnected.")
        else:
            print("Connection Manager: Already disconnected.")

    def __str__(self):
        return f"Connection Manager is {self.state}"


def simulate_udp_protocol():
    sender = SenderFSM()
    receiver = ReceiverFSM()
    connection_manager = ConnectionManagerFSM()

    # Simulate connection
    connection_manager.connect()

    for _ in range(5):  # Simulate 5 message sends
        print(sender)
        print(receiver)
        print(connection_manager)

        # Sender sends a message
        sender.send()

        # Receiver attempts to receive a message
        receiver.receive()

        # Wait for a second before the next iteration
        time.sleep(1)

    # Simulate disconnection
    connection_manager.disconnect()


if __name__ == "__main__":
    simulate_udp_protocol()
