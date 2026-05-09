import pandas as pd
import plotly.graph_objects as go
import numpy as np

from utils.plotly_templates import template
import utils.constants as cte



def heatmap(df_coordinates: pd.DataFrame) -> go.Figure:
    # Removing attendant coordinates.
    attendant_coords_to_remove = [
        (808, 447),
        (507, 435),
        (1120, 556)
    ]
    radius = 50
    for r_x, r_y in attendant_coords_to_remove:
        distance = np.sqrt((df_coordinates['x'] - r_x)**2 + (df_coordinates['y'] - r_y)**2)
        df_coordinates = df_coordinates[distance > radius]

    fig = go.Figure()

    # Marking the points.
    fig.add_trace(
        go.Histogram2d(
            x=df_coordinates['x'],
            y=df_coordinates['y'],

            showscale=False,
            
            nbinsx=300,
            nbinsy=150,
            colorscale=[
                [0, 'rgba(0,0,0,0)'],
                [0.01, '#000000'],    
                [0.02, "#c6c3cf"],
                [0.1, "#fffcd2"],
                [0.3, "#fffcd2"],
                [0.5, "#ff4848"],
                [1.0, "#ff4848"],     
            ],
        )
    )

    # Styling.
    fig.update_layout(
        template=template,

        xaxis=dict(
            range=[200, 1550],
            showticklabels=False,
            ticks=""
        ),
        yaxis=dict(
            range=[850, 100],
            showticklabels=False,
            ticks=""
        ),

        margin=dict(b=10, t=10, l=10, r=10)
    )

    # Adding the comments to the plot.
    labels = [
        (1011, 176, 'Catracas'),
        (1427, 444, 'Mesas'),
    ]
    for lx, ly, ltext in labels:
        fig.add_annotation(
            x=lx,
            y=ly,

            showarrow=False,

            text=ltext,
            font=dict(
                size=11,
                color=cte.color,
            ),

            bgcolor="rgba(0,0,0,0)", 
        )
        
    return fig


def occupancy_over_time(df_occupancy: pd.DataFrame) -> go.Figure:
    df_occupancy['Cumulative_Mean'] = df_occupancy['C_i'].expanding().mean()

    fig = go.Figure()

    # Creating the scatter plot.
    fig.add_trace(
        go.Scatter(
            x=df_occupancy['Snapshot'],
            y=df_occupancy['C_i'],
            mode='lines+markers',
            marker=dict(
                color=cte.noise_color,
                size=2,
            ),
            name='Ocupação',
        )
    )

    # Adding the cumulative mean.
    fig.add_trace(
        go.Scatter(
            x=df_occupancy['Snapshot'],
            y=df_occupancy['Cumulative_Mean'],
            mode='lines',

            name='Média Cumulativa da Ocupação',

            line=dict(
                color=cte.scolor,
                width=2,
            ),
        )
    )

    # Styling.
    fig.update_layout( 
        template=template,

        xaxis=dict(
            title=dict(
                text='Tempo',
                font=dict(
                    color=cte.color,
                ),
            ),
            showticklabels=False
        ),
        yaxis=dict(
            title=dict(
                text='Ocupação',
                font=dict(
                    color=cte.color,
                ),
            )
        ),
        margin=dict(b=20)
    )

    return fig
