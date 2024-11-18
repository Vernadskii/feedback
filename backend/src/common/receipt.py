class Receipt:
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

    def __init__(self, initial_data):
        self._data = {
            "date": initial_data["date"],
            "transaction_number": initial_data["transaction_number"],
            "sum": initial_data["sum_total"],
            "items_count": len(initial_data["items"]),
            "card_number": initial_data["card_number"],
        }

