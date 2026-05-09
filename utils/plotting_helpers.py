from pathlib import Path

import plotly.graph_objects as go
import graphviz

from utils.types import Scalar



# Class to be instantiated with a path store the plots on.
class Downloader:
    def __init__(self, path: Path) -> None:
        self.path = path

    def download_plotly(self, plot: go.Figure, filename: str, w: Scalar, h: Scalar) -> None:
        output_file = self.path / filename
        plot.write_image(output_file, width=w, height=h)

    def download_graphviz(self, plot: graphviz.Digraph, filename: str) -> None:
        plot.render(
            filename=filename, 
            directory=self.path,
            view=False,
            cleanup=True,
            format='svg'
        )


# For visualization on a Jupyter Notebook.
def show_plot(plot: go.Figure) -> None:
    plot.show(config={'staticPlot': True})





