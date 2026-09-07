class MessageParameters:
  def __init__(
    self,
    title: str | None = None,
    file: str | None = None,
    column: int | None = None,
    end_column: int | None = None,
    line: int | None = None,
    end_line: int | None = None,
  ):
    self.title: str | None = title
    self.file: str | None = file
    self.column: int | None = column
    self.end_column: int | None = end_column
    self.line: int | None = line
    self.end_line: int | None = end_line

  PARAMETER_MAPPING: dict[str, str] = {
    "title": "title",
    "file": "file",
    "column": "col",
    "end_column": "endColumn",
    "line": "line",
    "end_line": "endLine",
  }
  def _serialise(self) -> str:
    # Class to github parameter names
    workflow_command_parameters = ""
    for parameter, value in vars(self).items():  # pyright: ignore[reportAny]
      if value is not None:
        workflow_command_parameters += (
          f"{self.PARAMETER_MAPPING[parameter]}={value},"
        )

    if len(workflow_command_parameters) != 0:
      # Add beginning space and removing trailing comma
      workflow_command_parameters = (
        " "
        + workflow_command_parameters[0 : len(workflow_command_parameters) - 1]
      )

    return workflow_command_parameters
