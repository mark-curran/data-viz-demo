from datetime import datetime
from typing import List, cast

import numpy as np
from scipy.stats import linregress

from backend.types import Actual, SciPyresultLinregressResult


class Regressor:

    _res: SciPyresultLinregressResult
    x: List[int]
    y: List[int]
    _is_fitted: bool

    def __init__(self, actuals: List[Actual]) -> None:

        # x and y need to be initiated as empty lists
        self.x = []
        self.y = []
        self._is_fitted = False

        # Eliminate dates for which we have no data.
        for j in range(len(actuals)):
            dt = actuals[j].datetime
            actual = actuals[j].actual
            if actual is not None:
                self.x.append(int(dt.timestamp()))
                self.y.append(actual)

        return

    def fit(self) -> None:

        self._res = cast(SciPyresultLinregressResult, linregress(self.x, self.y))

        self._is_fitted = True

        return

    def predict(self, dt: datetime) -> int:

        return int(self._res.intercept + self._res.slope * dt.timestamp())
