import plotly.graph_objects as go
import pandas as pd

from utils.types import Scalar
import utils.constants as c



# General template for Plotly figures.
template = go.layout.Template()
template.layout = dict(
    autosize=False,
    showlegend=False,

    xaxis=dict( 
        showgrid=False,
        zeroline=False,
        showline=True,
        mirror=True,

        title=dict(
            font=dict(
                size=14,
                color=c.color
            ),
            standoff=10,
        ),
        tickfont=dict(
            size=10,
            color=c.color
        ),

        gridcolor=c.color,
        linecolor=c.color,
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=True,
        mirror=True,

        title=dict(
            font=dict(
                size=14,
            ),
            standoff=5,
        ),
        tickfont=dict(
            size=10,
            color=c.color
        ),

        gridcolor=c.color,
        linecolor=c.color, 
    ),
    margin=dict(t=10,b=30,r=50,l=50),
    paper_bgcolor='white',
    plot_bgcolor='white',
    width=c.width,
    height=c.height,
)


# Helpers for translating Data Frames into tables.
def _get_df_header_to_plotly(df):
    return list(df.columns)

def _get_df_cells_to_plotly(df):
    return [df[col].to_list() for col in df.columns]

# Template for Plotly tables.
def table_template(
        df: pd.DataFrame,  
        w: Scalar, 
        h: Scalar,
        columns: list[str] | None = None,
) -> go.Figure:
    
    if columns is None:
        columns = list(df.columns)

    df = df.copy()
    df.columns = columns
    fig = go.Figure()
    fig.add_trace(
        go.Table(
            header=dict(
                values=_get_df_header_to_plotly(df),
                font=dict(
                    size=11
                ),
                fill_color='rgba(0,0,0,0)',
                align='center',
                height=20,
            ),
            cells=dict(
                values=_get_df_cells_to_plotly(df),
                font=dict(
                    size=11
                ),
                fill_color='rgba(0,0,0,0)', 
                align='center',
                height=20,
            )
        )
    )

    fig.update_layout(
        margin=dict(b=10, t=10, l=10, r=10),
        width=w,
        height=h
    )

    return fig