## Inputs parsed from github action's env variables

import os
from collections.abc import Set
from pathlib import Path
from types import TracebackType

from action.errors import (
  ActionRuntimeError,
  UndefinedInputError,
  WorkspaceEnvironmentInvalidError,
)
from errors import UnexpectedError

from .logger import (
  _error_and_exit as log_error_and_exit,  # pyright: ignore[reportPrivateUsage]
)

Artifact = Path


class Action:
  _ENV_WORKSPACE: str = "GITHUB_WORKSPACE"
  _ENV_ARTIFACTS: str = "GITHUB_ARTIFACTS"

  def __init__(self):
    self.workspace: Path = self._get_workspace()
    self.inputs: "Action.Inputs" = self.Inputs(self)
    self.output_artifacts: Set[Artifact] = set()

  def __enter__(self):
    return (self.inputs, self.output_artifacts)

  def __exit__(
    self,
    exception_type: type[BaseException] | None,
    exception_value: BaseException | None,
    exception_traceback: TracebackType | None,
  ) -> bool | None:
    if exception_type is None or exception_value is None:
      self._set_output_artifacts(*self.output_artifacts)
    elif issubclass(exception_type,ActionRuntimeError) and isinstance(
      exception_value, ActionRuntimeError
    ):
      log_error_and_exit(exception_value)
    else:
      log_error_and_exit(UnexpectedError(exception_value))

  def _set_output_artifacts(self, *artifacts: Artifact):
    for artifact in artifacts:
      os.environ[self._ENV_ARTIFACTS] = os.getenv(self._ENV_ARTIFACTS, "").join(
        [str(artifact.relative_to(self.workspace, walk_up=True)), "\n"]
      )

  def _get_workspace(self) -> Path:
    workspace = os.getenv(self._ENV_WORKSPACE)
    if isinstance(workspace, str):
      return Path(workspace)
    else:
      log_error_and_exit(
        WorkspaceEnvironmentInvalidError(
          "Workspace environment variable is not defined"
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
