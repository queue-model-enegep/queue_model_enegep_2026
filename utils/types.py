from typing import Literal



DistType = Literal['Exponential', 'Gamma']

type DistParams = dict[str, float]


type TimeInSeconds = float


type Scalar = int | float

Units = Literal['m', 's']

