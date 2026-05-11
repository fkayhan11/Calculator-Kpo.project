from operations import Operation

class OperationDecorator(Operation):
    def __init__(self, operation):
        self._operation = operation

    def execute(self, a, b):
        return self._operation.execute(a, b)