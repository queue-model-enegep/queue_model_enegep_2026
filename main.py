from pathlib import Path

from scipy.stats import gamma

import core.data_handling as data_handler
from core.flowcharts import service_area_flowchart, method_flowchart
from core.calculations import get_lambda, get_mu, calibration
import core.system_analysis as system_analysis
import core.analysis_of_distribution as analysis_of_distribution
from core.simulation import gamma_params, exponential_params, QueueSimulator

from utils.plotting_helpers import Downloader
import utils.constants as cte
from utils.print_styles import label, result, big_line
from utils.execution_helpers import MarkRuntime
from utils.plotly_templates import table_template


# Creating the folder to hold the outputs.
output_dir = Path('outputs')
output_dir.mkdir(exist_ok=True)

# Creating the file for the script results.
file_path = output_dir / "results.txt"

# Creating the plots subfolder.
plots_dir = output_dir / 'plots'
plots_dir.mkdir(exist_ok=True)

# Setting the dowload of the plots.
d = Downloader(plots_dir)


# Getting the data arrivals and for service times.
df_arrivals = data_handler.get_arrivals_df()
df_group_arrivals = data_handler.get_arrivals_df(group_arrivals=True)
df_service_times = data_handler.get_service_time_df()

# Getting the data from the video OpenCV analysis.
df_coordinates = data_handler.get_heatmap_coordinates_df()
df_occupancy = data_handler.get_occupancy_df()


# Core of the project: 
# running the entire analysis;
# providing monitoring via terminal;
# saving the outputs (calculations, plots) on a folder.
with MarkRuntime():
    with open(file_path, 'w') as f:

        # Baseline.
        big_line()
        print('PROCESSING STARTED')

        print('RESULTS', file=f)
        print(file=f)


        # Generating the plots for the initial analysis (flowcharts).
        big_line()
        print('Setting initial analysis...')

        fig = service_area_flowchart()
        d.download_graphviz(fig, 'service_area_layout.svg')

        fig = method_flowchart()
        d.download_graphviz(fig, 'method_flowchart.svg')


        # Calculating main queue parameters.
        big_line()
        print("Calculating main queue parameters...")

        big_line(file=f)
        print('Main queue parameters:', file=f)
        big_line(file=f)

        LAMBDA, se_arrivals = get_lambda(df_arrivals)
        print(label('Arrival Rate:'), result(LAMBDA * 3600), 'arrivals per hour.', file=f)
        print(label('Standard Error of the Dataset:'), result(se_arrivals), 'seconds', file=f)
        print(file=f)

        MU, se_service_times = get_mu(df_service_times)
        print(label('Service Rate per Server:'), result(MU * 3600), 'services per hour per server.', file=f)
        print(label('Standard Error of the Dataset:'), result(se_service_times), 'seconds', file=f)
        print(file=f)
        print(file=f)


        # Calibrating the model.
        big_line()
        print('Calibrating the model...')

        big_line(file=f)
        print('Model Calibration:', file=f)
        big_line(file=f)

        df_calibration = calibration(LAMBDA, MU, 59, slice(0, 3), columns=['Servers', cte.rho_char, 'Lq (people)', 'W (seconds)'])
        table_calibration = table_template(df_calibration, w=400, h=102, columns=['Servidores', cte.rho_char, 'Lq (pessoas)', 'W (segundos)'])
        d.download_plotly(table_calibration, 'calibration_table.svg', w=400, h=102)
        print(df_calibration, file=f) 
        print(file=f)
        print(file=f)

        
        # Generating the plots for the analysis of the queue system.
        big_line()
        print('Analyzing the model...')

        fig = system_analysis.heatmap(df_coordinates)
        d.download_plotly(fig, 'heatmap.png', w=cte.width, h=cte.height)

        fig = system_analysis.occupancy_over_time(df_occupancy)
        d.download_plotly(fig, 'occupancy_over_time.svg', w=cte.width, h=cte.height - 10)

        fig = analysis_of_distribution.arrivals_histogram(df_group_arrivals)
        d.download_plotly(fig, 'arrivals_hist.svg', w=cte.width, h=cte.height)

        fig = analysis_of_distribution.arrivals_qq(df_group_arrivals)
        d.download_plotly(fig, 'arrivals_qq.svg', w=cte.width, h=cte.height)

        fig = analysis_of_distribution.service_histogram(df_service_times)
        d.download_plotly(fig, 'service_hist.svg', w=cte.width, h=cte.height)

        fig = analysis_of_distribution.service_qq(df_service_times)
        d.download_plotly(fig, 'service_qq.svg', w=cte.width, h=cte.height)


        # Running M/M/c simulation.
        big_line()
        print('Running M/M/c simulation...')

        big_line(file=f)
        print('M/M/c Simulation:', file=f)
        big_line(file=f)

        arrival_params = exponential_params(LAMBDA)
        service_params = exponential_params(MU)

        MMc = QueueSimulator(
            arrival_dist='Exponential',
            arrival_params=arrival_params,
            service_dist='Exponential',
            service_params=service_params,
            number_of_servers=38,
            number_of_customers=903,
            number_of_seeds=49,
        )

        MMc.simulate_initial_state(sampling_significance_level=0.05, sampling_relative_margin_of_error=0.05)

        MMc.add_stations(station_size=12, stations_to_add=3)

        df_MMc = MMc.get_simulation_dataframe(columns=['+Stations', cte.rho_char, 'W (seconds)'])
        table_MMc = table_template(df_MMc, w=400, h=122, columns=['+Buffets', cte.rho_char, 'W (segundos)'])
        d.download_plotly(table_MMc, 'MMc_table.svg', w=400, h=122)
        print(df_MMc, file=f)
        print(file=f)
        print(file=f)


        # Running M/G/c simulation.
        big_line()
        print('Running M/G/c simulation...')

        big_line(file=f)
        print('M/G/c Simulation:', file=f)
        big_line(file=f)

        arrival_params = exponential_params(LAMBDA)

        ALPHA, LOC, BETA = gamma.fit(df_service_times.iloc[:, 0])
        service_params = gamma_params(ALPHA, LOC, BETA)

        MGc = QueueSimulator(
            arrival_dist='Exponential',
            arrival_params=arrival_params,
            service_dist='Gamma',
            service_params=service_params,
            number_of_servers=38,
            number_of_customers=903,
            number_of_seeds=49,
        )

        MGc.simulate_initial_state(sampling_significance_level=0.05, sampling_relative_margin_of_error=0.05)

        MGc.add_stations(station_size=12, stations_to_add=3)

        df_MGc = MGc.get_simulation_dataframe(columns=['+Stations', cte.rho_char, 'W (seconds)'])
        table_MGc = table_template(df_MGc, w=400, h=122, columns=['+Buffets', cte.rho_char, 'W (segundos)'])
        d.download_plotly(table_MGc, 'MGc_table.svg', w=400, h=122)
        print(df_MGc, file=f)









        

    






