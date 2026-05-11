from datetime import datetime
from operation_decorator import OperationDecorator


class FileLoggingDecorator(OperationDecorator):
    """
    Saves calculation history into a log file
    """

    def execute(self, a, b):
        result = self._operation.execute(a, b)

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_message = (
            f"{current_time} | "
            f"{a} and {b} = {result}\n"
        )

        with open("calculator_history.txt", "a") as file:
            file.write(log_message)

        return result