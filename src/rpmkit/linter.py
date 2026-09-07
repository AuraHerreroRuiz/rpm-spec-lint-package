
import re
from enum import Enum
from pathlib import Path

from rpmlint.lint import Lint

from action.errors import ActionRuntimeError
from action.message_parameters import MessageParameters


class FatalLintsError(ActionRuntimeError):
  def __init__(
    self,
    file: str
  ) -> None:
    super().__init__(
      "More than one critical lint was found.",
      3,
      MessageParameters(
        file=file
      ))



class LintLevel(Enum):
  Information = "I"
  Warning = "W"
  Error = "E"


class Linting:
  "Represents a lint message"

  def __init__(
    self,
    file: str,
    arch: str | None,
    line: int | None,
    level: LintLevel,
    issue: str,
    details: str | None,
  ):
    self.file = file
    self.arch = arch
    self.line = line
    self.level = level
    self.issue = issue
    self.details = details

  file: str
  "File referred to by the lint message"

  arch: str | None
  "Architecture of the file"

  line: int | None
  "Line of the file containing the issue"

  level: LintLevel

  issue: str
  "Rpmlint issue title"

  details: str | None
  "Lint error details"

class Linter:
  def __init__(self,rpm_file_path: str) -> None:
    self.path: str = rpm_file_path

  def lint(self) -> tuple[int, list[Linting]]:
    "Returns the amount of fatal lints, and a list of all the lintings."
    lints: list[Linting] = []
    linter: Lint = Lint(
      options={
        "rpmfile": [],
        # Need to be empty, otherwise it will exit
        "checks": "",
        "config": [],
        "explain": [],
        "ignore_unused_rpmlintrc": False,
        "installed": [],
        "permissive": False,
        "print_config": False,
        "profile": False,
        "rpmlintrc": [],
        "strict": False,
        "time_report": False,
        "verbose": False,
      }
    )
    linter.validate_file(Path(self.path), True)

    for result in linter.output.results:
      lint_message = re.search(
        "(?P<file>.+?\\.[^.]+?)(?:\\.(?P<arch>.+?))?:(?:(?P<line>\\d+):)? (?P<level>[IWE]): (?P<issue>.+)",  # noqa: E501
        result,
      )
      if lint_message is None:
        raise TypeError
      lint = lint_message.groupdict()
      file = lint["file"]
      issue = lint["issue"]
      level = lint["level"]
      if not (isinstance(file, str) and isinstance(issue, str)):
        raise TypeError
      details: str | None = None
      if issue in linter.output.error_details:
        details = linter.output.error_details[issue]

      lints.append(
        Linting(
          file=file,
          arch=lint["arch"] if lint["arch"] else None,
          line=int(lint["line"]) if lint["line"] else None,
          level=LintLevel(level),
          issue=issue,
          details=details
        )
      )
    return linter.output.score, lints
