from collections import deque
from datetime import datetime, timedelta

class TradeLimiter:
    def __init__(self, max_trades_per_minute=10):
        self.max_trades = max_trades_per_minute
        self.timestamps = deque()

    def can_trade(self):
        now = datetime.utcnow()
        while self.timestamps and self.timestamps[0] < now - timedelta(seconds=60):
            self.timestamps.popleft()
        return len(self.timestamps) < self.max_trades

    def record_trade(self):
        self.timestamps.append(datetime.utcnow())
