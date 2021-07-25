import time

from web3._utils.filters import LogFilter


class AskEvent:
    """
    Representation of relevant information from ShroomMarket ask event
    """

    def __init__(self, event):
        self.customer_public_key = event['args']['customer_pubk']
        self.customer_address = event['args']['customer']
        self.seller_address = event['args']['seller']
        self.total = event['args']['total']

    def __str__(self):
        return f"customer: {self.customer_address}, seller: {self.seller_address}, total: {self.total}"

    @classmethod
    def from_values(cls, customer_public_key: str, customer_address: str, seller_address: str, total: int):
        return cls({
            "args":
                {
                    "customer_pubk": customer_public_key,
                    "customer": customer_address,
                    "seller": seller_address,
                    "total": total
                }
        })


class EventListener:

    def __init__(self, event_filter: LogFilter, event_handler, poll_interval: int):
        self.event_filter = event_filter
        self.event_handler = event_handler
        self.poll_interval = poll_interval

    def start(self):
        while True:
            for event in self.event_filter.get_new_entries():
                self.event_handler(event)
            time.sleep(self.poll_interval)
