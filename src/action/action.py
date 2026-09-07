import os
from pathlib import Path
from types import TracebackType

from action.errors import (
  ActionEnvironmentInvalidError,
  ActionRuntimeError,
  UndefinedInputError,
)
from errors import UnexpectedError

from .logger import (
  _error_and_exit as log_error_and_exit,  # pyright: ignore[reportPrivateUsage]
)


class Action:
  _ENV_WORKSPACE: str = "GITHUB_WORKSPACE"
  _ENV_OUTPUT_FILE_PATH: str = "GITHUB_OUTPUT"

  def __init__(self):
    try:
      self.workspace: Path = self._get_workspace()
      self.inputs: "Action.Inputs" = self.Inputs(self)
      self.outputs: "Action.Outputs" = self.Outputs()
    except Exception as e:
      _handle_action_errors(e)

  def __enter__(self) -> tuple[Path,"Inputs", "Outputs"]:
    return (self.workspace, self.inputs, self.outputs)

  def __exit__(
    self,
    exception_type: type[BaseException] | None,
    exception_value: BaseException | None,
    exception_traceback: TracebackType | None,
  ) -> bool | None:
    if exception_type is None or exception_value is None:
      try:
        self._set_outputs(self.outputs)
      except Exception as e:
        _handle_action_errors(e)
    else:
      _handle_action_errors(exception_value)

  def _set_outputs(self, outputs: "Outputs"):
    with open(self._get_outputs_file(), "a") as list:
      for key, path in outputs.serialise().items():
        _ = list.write(
          f"{key}={str(path.relative_to(self.workspace, walk_up=False))}\n"
        )

  def _get_action_path(self, environment_variable: str):
    path = os.getenv(environment_variable)
    if isinstance(path, str):
      return Path(path)
    else:
      log_error_and_exit(
        ActionEnvironmentInvalidError(
          f"{environment_variable} variable is not defined"
        )
      )

  def _get_workspace(self) -> Path:
    workspace = self._get_action_path(self._ENV_WORKSPACE)
    if workspace.is_dir():
      return workspace
    else:
      log_error_and_exit(
        ActionEnvironmentInvalidError(
          "Workspace environment variable "
          + f"{self._ENV_WORKSPACE}={os.getenv(self._ENV_WORKSPACE)} "
          + "does not point to a directory."
        )
      )

  def _get_outputs_file(self) -> Path:
    artifact_list = self._get_action_path(self._ENV_OUTPUT_FILE_PATH)
    if artifact_list.is_file():
      return artifact_list
    else:
      log_error_and_exit(
        ActionEnvironmentInvalidError(
          "Output environment variable "
          + f"{self._ENV_OUTPUT_FILE_PATH}"
          + f"={os.getenv(self._ENV_OUTPUT_FILE_PATH)} "
          + "does not point to a file."
        )
      )

  class Inputs:
    _ENV_INPUTS_PREFIX: str = "INPUT_"

    def __init__(self, action: "Action"):
      self.SPEC_FILE: str = self._get_input_or_error("spec_file")
      self.SOURCES_DIR: str | None = self._get_input("sources_dir")

    def _get_input(self, input_key: str) -> str | None:
      input = os.getenv(self._ENV_INPUTS_PREFIX + input_key.upper())
      if input == "":
        return None
      else:
        return input

    def _get_input_or_error(self, input_key: str) -> str:
      input = self._get_input(input_key)
      if input is None:
        log_error_and_exit(UndefinedInputError(input_key))
      return input

  class Outputs:
    def __init__(self):
      self.rpm_directory: Path
      self.source_rpm_directory: Path

    def serialise(self) -> dict[str, Path]:
      return {
        "rpm_directory_path": self.rpm_directory,
        "source_rpm_directory_path": self.source_rpm_directory,
      }


def _handle_action_errors(e: BaseException):
  if issubclass(type(e), ActionRuntimeError) and isinstance(
    e, ActionRuntimeError
  ):
    log_error_and_exit(e)
  else:
    log_error_and_exit(UnexpectedError(e))
