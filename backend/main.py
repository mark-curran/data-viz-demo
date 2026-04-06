from csv import DictReader
from datetime import datetime
from os import environ
from typing import List

from backend.logger import logger
from backend.prediction import PredictionComparitor
from backend.regression import Regressor
from backend.types import Actual, Estimate
from backend.utils import print_rankings

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
    regressor.fit()
    # Get the prediced value of the end of the time range.
    prediction_dist = regressor.distribution_predict(actuals[-1].datetime)

    comparitor = PredictionComparitor(prediction_dist, 1000, estimates)

    probabilities_by_rank = comparitor.run_simulation()

    top_per_rank = {
        rank: next(iter(probs.items())) for rank, probs in probabilities_by_rank.items()
    }

    print_rankings(top_per_rank, n=22)

    return


if __name__ == "__main__":
    logger.debug("Starting Data Viz Demo Backend.")

    main()
