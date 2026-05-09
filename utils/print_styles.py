from utils.types import Scalar

from io import TextIOWrapper



# Formatting the display of metrics.
def label[T](val: T) -> str:
    return f'{val:<40}'


# Formatting numeric values.
def result(val: Scalar) -> str: 
    return f'{val:.6g}'


# Creating a big line, to get a more clear output.
def big_line(file: TextIOWrapper | None = None) -> None:
    if file is not None:
        print(90*'-', file=file)
    else:
        print(90*'-')