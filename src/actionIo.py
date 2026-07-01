## Inputs parsed from github action's env variables

import os
from typing import Final

import logger

import dnf

_ENV_INPUTS_PREFIX: Final[str] = "INPUT_"

class workflow:

    def __init__(self):
        workspace = os.getenv("GITHUB_WORKSPACE")
        if isinstance(workspace,str) :
            self.workspacePath: str = workspace
        else:
            logger.ErrorAndTerminate("Workspace environment variable is not defined",errorCode=128)

    def getInput(self, inputKey: str) -> str | None:
        return os.getenv(_ENV_INPUTS_PREFIX + inputKey.upper())
