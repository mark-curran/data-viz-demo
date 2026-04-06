from datetime import datetime
from typing import Any, List, cast

import numpy as np
from scipy.stats import linregress, t

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

    def point_predict(self, dt: datetime) -> int:

        if not self._is_fitted:
            raise ValueError("Regressor is not fitted.")

        return int(self._res.intercept + self._res.slope * dt.timestamp())

    def distribution_predict(self, dt: datetime) -> Any:

        # TODO: Double check this methodology against wikipedia:
        # https://en.wikipedia.org/wiki/Simple_linear_regression#Variance_of_the_mean_response
        if not self._is_fitted:
            raise ValueError("Regressor is not fitted.")

        x_pred = dt.timestamp()
        y_pred = self.point_predict(dt)
        n = len(self.x)

        x_mean = np.mean(self.x)
        x_ss = np.var(self.x) * n

        # Derive residual standard error from slope's stderr:
        # stderr = s / sqrt(x_ss)  →  s = stderr * sqrt(x_ss)
        s = self._res.stderr * np.sqrt(x_ss)

        se = s * np.sqrt(1 + 1 / n + (x_pred - x_mean) ** 2 / x_ss)

        return t(df=n - 2, loc=y_pred, scale=se)
