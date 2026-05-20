from datetime import datetime
from operation_decorator import OperationDecorator
from history_manager import HistoryManager
from typing import Optional


class FileLoggingDecorator(OperationDecorator):
    """
    Saves calculation history into a log file
    """

    def __init__(self, operation, symbol: str, history_manager: Optional[HistoryManager] = None):
        super().__init__(operation)
        self._symbol = symbol
        self._history = history_manager or HistoryManager()

    def execute(self, a, b):
        result = self._operation.execute(a, b)

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_message = (
            f"{current_time} | "
            f"{a} {self._symbol} {b} = {result}\n"
        )

        self._history.append_line(log_message)

        return result
