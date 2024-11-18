class Receipt:
    # {'transaction_number': '100000000002258297',
    # 'items': [3305320, 48687, 29582, 3210519, 202, 77100, 3449760, 3157875],
    # 'sum_total': 530.94,
    # 'date': '2024-11-15T00:44:24.673213',
    # 'card_number': '90432003421'}

    def __init__(self, initial_data):
        self.process(initial_data)

    def process(self, initial_data):
        data = initial_data
        self._data = {
            "date": data["date"],
            "transaction_number": data["transaction_number"],
            "sum": data["sum_total"],
            "items_count": len(data["items"]),
            "card_number": data["card_number"],
        }
