from dataclasses import dataclass, field
from typing import List


# {
#     "transaction_number": "100000000002258297",
#     "items": [
#         3305320,
#         48687,
#         29582,
#         3210519,
#         202,
#         77100,
#         3449760,
#         3157875
#     ],
#     "sum_total": 530.94,
#     "date": "2024-11-15T00:44:24.673213",
#     "card_number": "90432003421"
# }


@dataclass
class Receipt:
    transaction_number: str
    items: List[int]
    sum_total: float
    date: str
    card_number: str

    # Derived fields
    items_count: int = field(init=False)

    def __post_init__(self):
        # Automatically compute derived fields
        self.items_count = len(self.items)
