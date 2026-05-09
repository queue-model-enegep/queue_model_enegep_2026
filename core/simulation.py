from collections import deque
import heapq
import random

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import scipy.stats as stats

from utils.plotting_helpers import *
from utils.types import DistType, DistParams, TimeInSeconds
import utils.constants as cte



def exponential_params(rate) -> DistParams:
    return {'rate': rate,}


def gamma_params(alpha, loc, beta) -> DistParams:
    return {'alpha': alpha, 'loc': loc, 'beta': beta,}


class QueueSimulator:
    def __init__(
        self,
        arrival_dist: DistType,
        arrival_params: DistParams,
        service_dist: DistType,
        service_params: DistParams,
        number_of_servers: int,
        number_of_seeds: int,
        number_of_customers: int,
    ) -> None:
        
        self.arrival_dist = arrival_dist
        self.arrival_params = arrival_params
        self.service_dist = service_dist
        self.service_params = service_params
        self.number_of_servers = number_of_servers
        self.number_of_seeds = number_of_seeds
        self.number_of_customers = number_of_customers

        self._initial_data: list[list[float, Scalar]] = []
        self._more_stations_data: list[list[float, Scalar]] = []


    def _generate_time(self, dist, params) -> float:
        if dist == 'Exponential':
            return random.expovariate(params['rate'])
        elif dist == 'Gamma':
            return random.gammavariate(params['alpha'], params['beta']) + params['loc']
        raise ValueError('Invalid distribution type')


    def _single_simulation(self, seed: int) -> pd.DataFrame:
        # Applying the seed.
        random.seed(seed)  

        # Main structure.
        CLOCK: TimeInSeconds = 0.0          
        QUEUE: deque[TimeInSeconds] = deque()      
        SERVERS: list[TimeInSeconds] = [] 
        RECORDS: list[dict] = [] 

        # Handling customers.
        customers_processed: int = 0
        customer_counter: int = 0

        # Generate the arrival time using the given distribution.
        arrival = self._generate_time(self.arrival_dist, self.arrival_params)
                
        # Loop until the customers threshold is hit.
        while customers_processed < self.number_of_customers:

            # Checking for the state of the servers.
            if SERVERS:
                next_departure = SERVERS[0]
            else:
                next_departure = float('inf')

            # Handling arrivals.
            if arrival < next_departure:
                
                # Updating the clock and the customer counter.
                CLOCK = arrival
                customer_counter += 1
                
                # Generate the service duration using the given distribution.
                duration = self._generate_time(dist=self.service_dist, params=self.service_params)
                
                # Create a customer data record.
                customer = {
                    'arrival_order': customer_counter,
                    'arrival': CLOCK,    
                    'start': None,    
                    'end': None,   
                    'duration': duration, 
                }

                # If a server is free, start service immediately.
                if len(SERVERS) < self.number_of_servers:
                    customer['start'] = CLOCK
                    customer['end'] = CLOCK + duration
                
                    # Add the departure time to the servers.
                    heapq.heappush(SERVERS, customer['end'])
                    
                    # Customer exit procedure: register its data and that he was processed.
                    RECORDS.append(customer)
                    customers_processed += 1 
                else:
                    # If all servers are busy, move the customer to the queue.
                    QUEUE.append(customer)
                
                # Schedule the next arrival
                if customer_counter < self.number_of_customers:
                    arrival = CLOCK + self._generate_time(self.arrival_dist, self.arrival_params)
                else:
                    arrival = float('inf')
                
            # Handling departures.
            else:
                CLOCK = next_departure
                
                # Remove the customer who just finished service.
                heapq.heappop(SERVERS)

                # If there are people on the queue, serve the next.
                if QUEUE:
                    # Pulling customer from the queue.
                    customer = QUEUE.popleft()

                    # Updating the clock.
                    customer['start'] = CLOCK
                    customer['end'] = CLOCK + customer['duration']
                    
                    # Moving customer to the servers.
                    heapq.heappush(SERVERS, customer['end'])
                    
                    # Saving individual data.
                    RECORDS.append(customer)

                    customers_processed += 1

        return RECORDS
    
    
    def _process_a_simulation(
        self, 
        records: list[dict], 
    ) -> tuple[Scalar, Scalar]:
        
        # Converting the simulation data to a Pandas Data Frame.
        df_records = pd.DataFrame(records)
        df_records = df_records.sort_values(by='arrival_order').reset_index(drop=True)
        df_records = df_records.round(2)

        # Measuring rho.
        total_capacity = df_records['end'].max() * self.number_of_servers 
        total_work = df_records['duration'].sum()
        RHO = total_work / total_capacity 

        # Measuring W.
        df_records['system_time'] = df_records['end'] - df_records['arrival'] 
        W = df_records['system_time'].mean()
        
        return RHO, W
    

    def _calculate_dynamic_sample_size(
        self, 
        significance_level: float, 
        relative_margin_of_error: float,
        W_values: list[Scalar]
    ) -> None:
        """
        Can only be run after at least one simulation.
        """
    
        W_array = np.array(W_values)

        n = W_array.shape[0]
        dof = n - 1

        sample_mean = W_array.mean()

        margin_of_error = sample_mean * relative_margin_of_error

        sample_std = np.std(W_array, ddof=1)

        t_value = stats.t.ppf(1 - (significance_level / 2), dof)

        proper_n = ((t_value * sample_std) / margin_of_error)**2

        additional_seeds = proper_n - n

        # Message for the dynamical adjusting of the sample size.
        if additional_seeds <= 0:
            print()
            print(f'The sample size is appropriate (we need {np.ceil(n + additional_seeds):.6g} seeds).')
        elif additional_seeds > 0:
            print()
            print(f'Add {np.ceil(additional_seeds):.6g} seeds!')
        else:
            raise ValueError('Error when checking sample size.')
        
    
    def simulate_initial_state(
            self, 
            sampling_significance_level: float, 
            sampling_relative_margin_of_error: float
    ) -> None:
        RHO_values: list[Scalar] = []
        W_values: list[Scalar] = []

        for seed in range(self.number_of_seeds):

            # Executing the simulation.
            records = self._single_simulation(seed=seed)
            RHO, W = self._process_a_simulation(records)

            RHO_values.append(RHO)
            W_values.append(W)

        RHO_0 = sum(RHO_values) / len(RHO_values)
        W_0 = sum(W_values) / len(W_values)
        self._initial_data.append([RHO_0, W_0])

        self._calculate_dynamic_sample_size(
            significance_level=sampling_significance_level,
            relative_margin_of_error=sampling_relative_margin_of_error,
            W_values=W_values
        )


    def add_stations(
        self,
        station_size: int,
        stations_to_add: int
    ) -> None:
        # Iteratively adding servers to the simulation.
        for i in range(stations_to_add):

            # Changing the number of servers for the simulation.
            self.number_of_servers += station_size

            RHO_values: list[Scalar] = []
            W_values: list[Scalar] = []

            for seed in range(self.number_of_seeds):

                # Executing the simulation.
                records = self._single_simulation(seed=seed)
                RHO, W = self._process_a_simulation(records)

                RHO_values.append(RHO)
                W_values.append(W)

            RHO_n = sum(RHO_values) / len(RHO_values)
            W_n = sum(W_values) / len(W_values)

            self._more_stations_data.append([RHO_n, W_n])


    def get_simulation_dataframe(
        self, 
        columns: list[str] = ['+Buffets', cte.rho_char, 'W (segundos)']
    ) -> pd.DataFrame:
        return pd.DataFrame(
            columns=columns[1:],
            data=[*self._initial_data, *self._more_stations_data]
        ).round(2).reset_index(names=columns[0])
    
    

    
