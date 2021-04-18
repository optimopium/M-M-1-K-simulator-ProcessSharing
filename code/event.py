from process import Process


class Event:
    """
    Simulation is event-based therefore everything like new process arrival into system or already 
    serviced process departure is an event
    """

    def __init__(self, etype, pid, q_size, start_time, end_time) -> None:
        super().__init__()
        # Arrival Deadline Departure
        self.type = etype
        self.pid = pid
        self.queue_size = q_size
        self.start_time = start_time
        self.time = end_time

    def __lt__(self, other: object) -> bool:
        return self.time < other

    def __le__(self, other: object) -> bool:
        return self.time <= other

    def __gt__(self, other: object) -> bool:
        return self.time > other

    def __ge__(self, other: object) -> bool:
        return self.time >= other

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Process):
            return self.pid == other.pid
        else:
            return self.time == other

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Process):
            return self.pid != other.pid
        else:
            return self.time != other

    def __repr__(self) -> str:
        return ("Type ={0}\tProcess={1}\tTime={2}\tstart_time={3}\tqueue_size={4}".format(
            self.type,
            self.pid,
            self.time,
            self.start_time,
            self.queue_size
        ))
