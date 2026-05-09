import plotly.graph_objects as go
import pandas as pd
import numpy as np
import scipy.stats as stats

from utils.plotly_templates import template
import utils.constants as cte



def arrivals_histogram(df_group_arrivals: pd.DataFrame) -> go.Figure:
    mean_inter_arrival_times = df_group_arrivals['Interval'].mean()
    lambda_inter_group_arrivals = 1 / mean_inter_arrival_times
    x = np.linspace(df_group_arrivals['Interval'].min(), df_group_arrivals['Interval'].max(), 100)
    y = lambda_inter_group_arrivals * np.exp(-lambda_inter_group_arrivals * x)

    fig = go.Figure()

    # Frequency of the inter-arrival intervals.
    fig.add_trace(
        go.Histogram(
            x=df_group_arrivals['Interval'],
            histnorm='probability density',
            marker=dict( 
                color=cte.scolor,
            )
        )
    )

    # Comparative Exponential curve.
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode='lines',
            
            line=dict(
                color=cte.tcolor,
                width=2,
            )
        )
    )

    # Styling.
    fig.update_layout(
        template=template,

        showlegend=False,

        xaxis=dict(
            title=dict(
                text='Intervalo (segundos)',
                font=dict(
                    color=cte.color
                )
            )
        ),
        yaxis=dict(
            title=dict(
                text='Probabilidade',
                font=dict(
                    color=cte.color
                )
            )
        ),

        bargap=0.1,
    )

    return fig


def arrivals_qq(df_group_arrivals: pd.DataFrame) -> go.Figure:
    (theoretical_quantiles, ordered_data), (slope, intercept, r) = stats.probplot(
        df_group_arrivals['Interval'], 
        dist="expon", 
        plot=None
    )

    regression_line = slope * theoretical_quantiles + intercept

    fig = go.Figure()

    # Data points.
    fig.add_trace(
        go.Scatter(
            x=theoretical_quantiles,
            y=ordered_data,
            mode='markers',

            name='Dados Observados',

            marker=dict(
                size=5,
                color=cte.tcolor,
                opacity=0.8
            )
        )
    )

    # Regression line.
    fig.add_trace(
        go.Scatter(
            x=theoretical_quantiles,
            y=regression_line,
            mode='lines',

            name=f'R²={r**2:.3f}',

            line=dict(
                color=cte.scolor,
                width=2, 
            )
        )       
    )

    # Styling.
    fig.update_layout(
        template=template,

        xaxis=dict(
            title=dict(
                text='Quantis Teóricos (Exponencial)',
                font_color=cte.color,
            )
        ),
        yaxis=dict(
            title=dict(
                text='Quantis Amostrais',
                font_color=cte.color,
            )
        ),
    )

    return fig


def service_histogram(df_service_times) -> go.Figure:
    series_service_time = df_service_times.iloc[:, 0]
    mean_service_time_sec = series_service_time.mean()
    mu = 1 / mean_service_time_sec
    x_exp = np.linspace(series_service_time.min(), series_service_time.max(), 200)
    y_exp = mu * np.exp(-mu * x_exp)

    fig = go.Figure()

    # Frequency of the service times.
    fig.add_trace(
        go.Histogram(
            x=series_service_time,
            
            marker=dict(
                color=cte.scolor,
            ), 

            histnorm='probability density',
            nbinsx=16,
        )
    )

    # Comparative Exponential curve.
    fig.add_trace(
        go.Scatter(
            x=x_exp,
            y=y_exp,
            mode='lines',

            line=dict(
                width=2,
                color=cte.tcolor,
            ),
        )
    )

    # Styling.
    fig.update_layout(
        template=template,

        showlegend=False,

        xaxis=dict(
            title=dict(
                text='Intervalo (sec)',
                font_color=cte.color,
            ),
        ),
        yaxis=dict(
            title=dict(
                text='Probabilidade',
                font_color=cte.color,
            ),
        ),

        bargap=0.1,
    )   

    return fig


def service_qq(df_service_times: pd.DataFrame) -> go.Figure:
    series_service_time = df_service_times.iloc[:, 0]
    alpha, loc, beta = stats.gamma.fit(series_service_time)
    (theoretical_quantiles, ordered_data), (slope, intercept, r) = stats.probplot(
        series_service_time,
        dist="gamma",
        sparams=(alpha,), 
        plot=None
    )
    regression_line = slope * theoretical_quantiles + intercept

    fig = go.Figure()

    # Regression line.
    fig.add_trace(
        go.Scatter(
            x=theoretical_quantiles,
            y=regression_line,
            mode='lines',

            name=f'R²={r**2:.3f}',
            
            line=dict(
                width=2,
                color=cte.scolor,
            ),  
        )
    )
    
    # Data points.
    fig.add_trace(
        go.Scatter(
            x=theoretical_quantiles,
            y=ordered_data,
            mode='markers',

            name='Dados Observados',

            marker=dict(
                color=cte.tcolor,
                size=5,
                opacity=0.8,
            ),
        )
    )

    # Styling.
    fig.update_layout(
        template=template,

        xaxis=dict(
            title=dict(
                text='Quantis Teóricos (Gamma)',
                font=dict(
                    color=cte.color
                ),
            )
        ),
        yaxis=dict(
            title=dict(
                text='Quantis Amostrais',
                font=dict(
                    color=cte.color
                ),
            )
        ),
    )

    return fig
