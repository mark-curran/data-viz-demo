from csv import DictReader
from datetime import datetime
from os import environ
from typing import List

from backend.logger import logger
from backend.regression import Regressor
from backend.types import Actual, Estimate

# TODO: Move to a config module instead.
estimates_source = environ["ESTIMATES_SOURCE"]
actuals_source = environ["ACTUALS_SOURCE"]


def main() -> None:

    with open(estimates_source) as file:
        data = list(DictReader(file))
        estimates: List[Estimate] = [
            Estimate(name=d["name"], estimate=int(d["estimate"])) for d in data
        ]

    with open(actuals_source) as file:
        data = list(DictReader(file))
        actuals: List[Actual] = [
            Actual(
                datetime=datetime.strptime(d["datetime"], "%m/%d/%Y %H:%M:%S"),
                actual=int(d["actual"]) if d["actual"] else None,
            )
            for d in data
        ]

    regressor = Regressor(actuals)

    return


if __name__ == "__main__":
    logger.debug("Starting Data Viz Demo Backend.")

    main()
