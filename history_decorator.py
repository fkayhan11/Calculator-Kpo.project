from operation_decorator import OperationDecorator

class HistoryDecorator(OperationDecorator):

    history = []

    def execute(self, a, b):
        result = self._operation.execute(a, b)

        HistoryDecorator.history.append(
            f"{a} and {b} = {result}"
        )

        return result