from abc import ABCMeta, abstractmethod

from action.message_parameters import MessageParameters


class ActionRuntimeError(Exception, metaclass=ABCMeta):
  @abstractmethod
  def __init__(
    self,
    message: str,
    exit_code: int,
    message_parameters: MessageParameters | None = None,
  ) -> None:
    super().__init__(message)
    self.message_parameters: MessageParameters | None = message_parameters
    self.exit_code: int = exit_code


class ActionEnvironmentInvalidError(ActionRuntimeError):
  def __init__(self, message: str) -> None:
    super().__init__(message, 1)


class UndefinedInputError(ActionRuntimeError):
  def __init__(self, input_key_name: str) -> None:
    self.input_key_name: str = input_key_name
    super().__init__(f"Required input {input_key_name} is not defined", 2)
