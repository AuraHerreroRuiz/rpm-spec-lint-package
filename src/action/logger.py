import sys
from types import TracebackType
from typing import Never

from action.errors import ActionRuntimeError
from action.message_parameters import MessageParameters


class LogGroup:
  def __init__(self, title: str):
    self.title: str = title

  def __enter__(self) -> None:
    print(f"::group::{self.title}", file=sys.stdout)

  def __exit__(
    self,
    exc_type: type[BaseException] | None,
    exc_val: BaseException | None,
    exc_tb: TracebackType | None,
  ) -> bool | None:
    print("::endgroup::", file=sys.stdout)


def masked_message(message: str):
  print(f"::add-mask::{message}", file=sys.stdout)


def notice(message: str, parameters: MessageParameters | None = None):
  _print_workflow_message("notice", message, parameters)


def warning(message: str, parameters: MessageParameters | None = None):
  _print_workflow_message("warning", message, parameters)


def error(message: str, parameters: MessageParameters | None = None):
  _print_workflow_message("error", message, parameters)


def _print_workflow_message(
  log_type: str,
  message: str,
  parameters: MessageParameters | None,
):
  function_paramaters = locals()
  function_paramaters.pop(
    "message"
  )  # message is required, not an optional parameter.
  serialised_parameters = ""
  if parameters is not None:
    serialised_parameters = parameters._serialise()  # pyright: ignore[reportPrivateUsage]
  print(
    f"::{log_type}{serialised_parameters}::{message}",
    file=sys.stdout,
  )

def _error_and_exit(e: ActionRuntimeError) -> Never:  # pyright: ignore[reportUnusedFunction]
  error(str(e), e.message_parameters)
  exit(e.exit_code)
