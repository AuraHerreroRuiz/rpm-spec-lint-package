class ActionSetupError(Exception):
  def __init__(self, message: str) -> None:
    super().__init__(message)


class UndefinedInputError(Exception):
  def __init__(self, message: str, input: str) -> None:
    super().__init__(message)
    self.input: str = input
