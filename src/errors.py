from action.errors import ActionRuntimeError
from action.message_parameters import MessageParameters


class PathInvalidError(ActionRuntimeError):
  def __init__(self, message: str, path: str) -> None:
    self.path: str = path
    super().__init__(
      message, 4, MessageParameters(f"The path ${path} cannot be found")
    )


class InternalError(ActionRuntimeError):
  def __init__(self, message: str, parameters: MessageParameters | None = None):
    super().__init__(message, 8, parameters)


class UnexpectedError(ActionRuntimeError):
  def __init__(self, e: BaseException):
    super().__init__(
      str(e), 9, MessageParameters("Unexpected Error has occurred")
    )
