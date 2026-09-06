import sys
from types import TracebackType
from typing import Any


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


def notice(
  message: str,
  title: str | None = None,  # pyright: ignore[reportUnusedParameter]
  file: str | None = None,  # pyright: ignore[reportUnusedParameter]
  column: int | None = None,  # pyright: ignore[reportUnusedParameter]
  end_column: int | None = None,  # pyright: ignore[reportUnusedParameter]
  line: int | None = None,  # pyright: ignore[reportUnusedParameter]
  end_line: int | None = None,  # pyright: ignore[reportUnusedParameter]
):
  function_paramaters = locals()
  function_paramaters.pop(
    "message"
  )  # message is required, not an optional parameter.

  print(
    f"::notice{_parameters_to_workflow_parametres(function_paramaters)}::{message}",
    file=sys.stdout,
  )


def warning(
  message: str,
  title: str | None = None,  # pyright: ignore[reportUnusedParameter]
  file: str | None = None,  # pyright: ignore[reportUnusedParameter]
  column: int | None = None,  # pyright: ignore[reportUnusedParameter]
  end_column: int | None = None,  # pyright: ignore[reportUnusedParameter]
  line: int | None = None,  # pyright: ignore[reportUnusedParameter]
  end_line: int | None = None,  # pyright: ignore[reportUnusedParameter]
):
  function_paramaters = locals()
  function_paramaters.pop(
    "message"
  )  # message is required, not an optional parameter.

  print(
    f"::warning{_parameters_to_workflow_parametres(function_paramaters)}::{message}",
    file=sys.stdout,
  )


def error(
  message: str,
  title: str | None = None,  # pyright: ignore[reportUnusedParameter]
  file: str | None = None,  # pyright: ignore[reportUnusedParameter]
  column: int | None = None,  # pyright: ignore[reportUnusedParameter]
  end_column: int | None = None,  # pyright: ignore[reportUnusedParameter]
  line: int | None = None,  # pyright: ignore[reportUnusedParameter]
  end_line: int | None = None,  # pyright: ignore[reportUnusedParameter]
):
  function_paramaters = locals()
  function_paramaters.pop(
    "message"
  )  # message is required, not an optional parameter.

  print(
    f"::error{_parameters_to_workflow_parametres(function_paramaters)}::{message}",
    file=sys.stdout,
  )


# TODO remove
def error_and_terminate(
  message: str,
  title: str | None = None,
  file: str | None = None,
  column: int | None = None,
  end_column: int | None = None,
  line: int | None = None,
  end_line: int | None = None,
  error_code: int = 2,
):
  error(
    title=title,
    message=message,
    file=file,
    column=column,
    end_column=end_column,
    line=line,
    end_line=end_line,
  )
  if error_code <= 0:
    exit(2)
  else:
    exit(error_code)


def _parameters_to_workflow_parametres(parameters: dict[str, Any]) -> str:  # pyright: ignore[reportExplicitAny]
  workflow_command_parameters = ""
  for parameter in parameters:
    if parameters[parameter] is not None:
      workflow_command_parameters += f"{parameter}={parameters[parameter]},"

  if len(workflow_command_parameters) != 0:
    # Add beginning space and removing trailing comma
    workflow_command_parameters = (
      " "
      + workflow_command_parameters[0 : len(workflow_command_parameters) - 1]
    )

  return workflow_command_parameters
