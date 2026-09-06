## Inputs parsed from github action's env variables

import os
from typing import Final

from . import logger

_ENV_INPUTS_PREFIX: Final[str] = "INPUT_"


class Workflow:
  def __init__(self):
    workspace = os.getenv("GITHUB_WORKSPACE")
    if isinstance(workspace, str):
      self.workspace_path: str = workspace
    else:
      logger.error_and_terminate(
        "Workspace environment variable is not defined", error_code=128
      )

  def get_input(self, input_key: str) -> str | None:
    input = os.getenv(_ENV_INPUTS_PREFIX + input_key.upper())
    if input == "":
      return None
    else:
      return input

  def get_input_or_error(self, input_key: str) -> str:
    input = self.get_input(input_key)
    if input is None:
      logger.error_and_terminate(
        f"Required input {input_key} is not defined", error_code=256
      )
    return input  # pyright: ignore[reportReturnType]
