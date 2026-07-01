import sys
from typing import Any

def startLinesGroup(title: str):
  print(f"::group::{title}",file=sys.stdout)

def endLinesGroup():
  print("::endgroup::")

def MaskedMessage(maskedMessage: str):
  print(f"::add-mask::{maskedMessage}",file=sys.stdout)

def Notice(
  message: str,
  title: str | None = None,
  file: str | None = None,
  column: int | None = None,
  endColumn: int | None = None,
  line: int | None = None,
  endLine: int | None = None,
  ):
  functionParamaters = locals()
  functionParamaters.pop("message") # message is required, not an optional parameter.

  print(f"::notice{_parametersToWorkflowParameters(functionParamaters)}::{message}",file=sys.stdout)

def Warning(
  message: str,
  title: str | None = None,
  file: str | None = None,
  column: int | None = None,
  endColumn: int | None = None,
  line: int | None = None,
  endLine: int | None = None,
  ):
  functionParamaters = locals()
  functionParamaters.pop("message") # message is required, not an optional parameter.

  print(f"::warning{_parametersToWorkflowParameters(functionParamaters)}::{message}",file=sys.stdout)

def Error(
  message: str,
  title: str | None = None,
  file: str | None = None,
  column: int | None = None,
  endColumn: int | None = None,
  line: int | None = None,
  endLine: int | None = None,
  ):
  functionParamaters = locals()
  functionParamaters.pop("message") # message is required, not an optional parameter.

  print(f"::error{_parametersToWorkflowParameters(functionParamaters)}::{message}",file=sys.stdout)

def ErrorAndTerminate(
  message: str,
  title: str | None = None,
  file: str | None = None,
  column: int | None = None,
  endColumn: int | None = None,
  line: int | None = None,
  endLine: int | None = None,
  errorCode=2,
  ):
  Error(title=title,message=message,file=file,column=column,endColumn=endColumn,line=line,endLine=endLine)
  if errorCode <= 0:
    exit(2)
  else:
    exit(errorCode)


def _parametersToWorkflowParameters(functionParamaters: dict[str, Any]) -> str:  # pyright: ignore[reportExplicitAny]
  workflowCommandParameters = ""
  for parameter in functionParamaters:
    if functionParamaters[parameter] is not None:
      workflowCommandParameters += f"{parameter}={functionParamaters[parameter]},"

  if len(workflowCommandParameters) != 0:
    # Add beginning space and removing trailing comma
    workflowCommandParameters = " " + workflowCommandParameters[0:len(workflowCommandParameters)-1]

  return workflowCommandParameters
