from typing import Any, List

import numpy as np

from backend.types import Estimate


class PredictionComparitor:

    dist: Any
    num_experiments: int
    actuals: List[Estimate]

    def __init__(self, dist, num_experiments, estimates) -> None:

        self.dist = dist
        self.num_experiments = num_experiments
        self.estimates = estimates

    def run_simulation(self) -> None:

        samples = self.dist.rvs(size=self.num_experiments)
        estimated_values = np.array([e.estimate for e in self.estimates])
        names = [e.name for e in self.estimates]

        # Diffs between estimates and sample values, converted into rank order.
        diffs = np.abs(estimated_values[np.newaxis, :] - samples[:, np.newaxis])
        # In each sample, in which position was the closest, second closest etc.
        # Example: "rank_indices[500, 0]" which position was the closet in experiment 500.
        rank_indices = np.argsort(diffs, axis=1)
        # For each position, what was their rank in each experiment.
        # Example: "actual_ranks[500, 0]" what rank was the first position (name) in the 500th experiment.
        actual_ranks = np.argsort(rank_indices, axis=1)

        # Placeholders to get ready to find
        n = len(self.estimates)
        ranks_per_name = {}

        for name_index in range(n):
            # Distribution of where the estimates with a given name were ranked in each experiment.
            name_indices = actual_ranks[:, name_index]
            ranks_per_name[names[name_index]] = name_indices

        # For a given name, the probability of it being first, second third etc.
        probabilities: dict[str, np.ndarray] = {
            name: np.bincount(ranks, minlength=n) / self.num_experiments
            for name, ranks in ranks_per_name.items()
        }

        probabilities_by_rank: dict[int, dict[str, float]] = {
            rank: dict(
                sorted(
                    {name: float(probabilities[name][rank]) for name in names}.items(),
                    key=lambda item: item[1],
                    reverse=True,
                )
            )
            for rank in range(n)
        }

        return
