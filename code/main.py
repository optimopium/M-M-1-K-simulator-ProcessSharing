import csv
import time as tm

from analyze import Analyze
from simulation import Simulation


def writeDownResult(result: list):
    """
    function to write the result into csv file

    Args:
        result (list): line you want to write into csv file
    """
    with open('result.csv', 'a', newline='') as csvfile:
        result_writer = csv.writer(csvfile, delimiter=',')
        result_writer.writerow(result)


def simulationTerminalLogger(arrival_rate, waiting_time_type, start):
    """
    Write Simulation execution log to

    Args:
        arrival_rate (float): processes arrival rate
        waiting_time_type (string): constant or exponential
        start (float): start point where you want to log passed time.
    """
    print("simulation process time for arrival-rate={}  and {} waiting time : {}".format(
        arrival_rate, waiting_time_type, tm.time() - start))


if __name__ == "__main__":
    # arrival_rates = [i/10 for i in range(1,201,1)]
    arrival_rates = [5,10,15]
    problem_size = 10**6
    waiting_time_types = ["Constant", "Exponential"]

    print("Problem Size is : {}".format(problem_size))

    with open('result.csv', 'a', newline='') as csvfile:
        result_writer = csv.writer(csvfile, delimiter=',')
        result_writer.writerow(
            ["Waiting_Time_Type", "Teta", "Mu", "Lambda", "Analysis_type", "PB", "PD"])

    with open("parameters.conf", 'r') as reader:
        while True:
            try:
                waiting_time = int(reader.readline())
                service_rate = int(reader.readline())
            except:
                break

            for arrival_rate in arrival_rates:
                for waiting_time_type in waiting_time_types:
                    is_exp = False if waiting_time_type == "Constant" else True
                    start = tm.time()
                    simulator = Simulation(arrival_rate)
                    simulation_pb, simulation_pd = simulator.simulate(waiting_time,
                                                                      service_rate,
                                                                      problem_size,
                                                                      is_exponential=is_exp)
                    simulationTerminalLogger(
                        arrival_rate, waiting_time_type, start)

                    result = [waiting_time_type, waiting_time, service_rate,
                              arrival_rate, "Simulation", simulation_pb, simulation_pd]
                    writeDownResult(result)

                    statistical_pb, statistical_pd = Analyze(mu=service_rate,
                                                             teta=waiting_time,
                                                             lam=arrival_rate,
                                                             is_expnential=is_exp).analyze()

                    writeDownResult([waiting_time_type, waiting_time, service_rate, arrival_rate,
                                     "Statistical", statistical_pb, statistical_pd])

    print("results are stored in result.csv")
