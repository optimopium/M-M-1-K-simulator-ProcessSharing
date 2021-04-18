from numpy import random


class Process:
    """
    Process is job that code tries to simulate
    """    
    def __init__(self, pid, arrival, deadline_time, service_rate, expo_deadline=True) -> None:
        super().__init__()
        self.pid = pid
        self.arrival = arrival
        self.deadline = random.exponential(
            deadline_time) if expo_deadline else deadline_time
        self.service = random.exponential(1 / service_rate)

    def __eq__(self, other: object) -> bool:
        return self.pid == other.pid

    def __repr__(self) -> str:
        return("P{0}:: arrival={1}\tdeadline={2}\tservice time={3}\n".format(
            str(self.pid),
            str(self.arrival),
            str(self.deadline),
            str(self.service)
        ))
