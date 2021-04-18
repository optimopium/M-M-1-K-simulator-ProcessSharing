import bisect
from typing import List

from numpy import random

from event import Event
from process import Process


class Simulation:
    def __init__(self, arrival_rate) -> None:
        # Mu
        self.arrival_rate = arrival_rate
        # time
        self.time = 0
        # count of processes passed deadline
        self.deadProcess = 0
        # process count
        self.process_count = 0
        # count of processes dropped out because queue is full
        self.blockedProcess = 0
        # queue to serve process if server is full
        self.queue: List[Process] = []
        # list of events
        self.events: List[Event] = []
        # list of processes
        self.processes: List[Process] = []

    def nextArrivalTime(self) -> float:
        return self.time + random.exponential(1/self.arrival_rate)

    def handleArrivalEvent(self, process: Process, event_time) -> Event:
        self.time = event_time
        if len(self.queue) == 12:
            # Queue is Full Block Process
            self.blockedProcess += 1
            return None
        elif 0 <= len(self.queue) < 12:
            # Put process in queue
            self.queue.append(process)
            self.updateEvents()
            deadline_event = Event(
                etype="Deadline",
                pid=process.pid,
                q_size=len(self.queue),
                start_time=self.time,
                end_time=(self.time + process.deadline)
            )

            departure_event = Event(
                etype="Departure",
                pid=process.pid,
                q_size=len(self.queue),
                start_time=self.time,
                end_time=self.time + process.service * len(self.queue)
            )
            return deadline_event, departure_event

    def handleEvent(self, process: Process, event: Event):
        self.time = event.time
        self.queue.remove(process)
        self.events.remove(process)
        if(event.type == "Deadline"):
            self.deadProcess += 1
        self.updateEvents()

    def updateEvents(self):
        for i in range(len(self.events)):
            if self.events[i].type == "Deadline":
                continue
            new_service_time = self.processes[self.events[i].pid].service - (
                self.time - self.events[i].start_time)/self.events[i].queue_size
            self.processes[self.events[i].pid].service = new_service_time
            assert self.events[i].start_time <= self.time
            self.events[i].start_time = self.time
            self.events[i].queue_size = len(self.queue)
            self.events[i].time = self.time + new_service_time * len(self.queue)
        self.events.sort()

    def simulate(self, waiting_time, service_rate, problem_size, is_exponential=True):
        arrival = 0
        while self.process_count < problem_size:
            if not self.events or self.events[0] >= arrival:
                self.processes.append(
                    Process(
                        pid=self.process_count,
                        arrival=arrival,
                        deadline_time=waiting_time,
                        service_rate=service_rate,
                        expo_deadline=is_exponential
                    )
                )
                result_events = self.handleArrivalEvent(
                    self.processes[self.process_count],
                    arrival)
                if result_events:
                    for retevent in result_events:
                        bisect.insort_left(self.events, retevent)
                arrival = self.nextArrivalTime()
                self.process_count += 1
            else:
                event = self.events.pop(0)
                self.handleEvent(self.processes[event.pid], event)

        Pb = self.blockedProcess/problem_size
        Pd = self.deadProcess/problem_size
        return Pb, Pd
