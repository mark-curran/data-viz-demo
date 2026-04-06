from dataclasses import dataclass
from datetime import datetime

import numpy as np


@dataclass
class Estimate:
    name: str
    estimate: int


@dataclass
class Actual:
    datetime: datetime
    actual: int | None


@dataclass
class SciPyresultLinregressResult:
    # SciPy doesn't expose a class for linear regression results.
    slope: np.float64
    intercept: np.float64
    intercept_stderr: np.float64
    stderr: np.float64
    pvalue: np.float64
    rvalue: np.float64
