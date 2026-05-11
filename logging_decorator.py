from operation_decorator import OperationDecorator

class LoggingDecorator(OperationDecorator):

    def execute(self, a, b):
        result = self._operation.execute(a, b)

        print(f"LOG: {a} ? {b} = {result}")

        return result