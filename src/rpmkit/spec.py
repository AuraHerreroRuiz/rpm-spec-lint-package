import os

from action import MessageParameters, logger
from action.errors import ActionRuntimeError
from errors import PathInvalidError

from .builder import Builder
from .linter import Linter, Linting, LintLevel


class Specfile:
  def __init__(self, path: str, sources_dir: str | None) -> None:
    if not os.path.isfile(path):
      raise PathInvalidError(message="Specfile not found", path=path)
    self.path: str = path
    self.sources_dir: str | None = sources_dir
    self.lints: list[Linting] = []

  def lint(self) -> None:
    """
    Logs the lints the Specfile.
    Raises CriticalLintsError if there are critical lints.
    """
    linter = Linter(self.path)
    fatal_lint_count, self.lints = linter.lint()
    self.print_lints()
    if fatal_lint_count > 0:
      raise FatalLintsError(self.path)

  def print_lints(self):
    for lint in self.lints:
      message: str
      title: str | None
      if lint.details is None:
        title = None
        message = lint.issue
      else:
        title = lint.issue
        message = lint.details
      match lint.level:
        case LintLevel.Error:
          logger.error(
            message,
            MessageParameters(title=title, file=self.path, line=lint.line),
          )
        case LintLevel.Warning:
          logger.warning(
            message,
            MessageParameters(title=title, file=self.path, line=lint.line),
          )
        case LintLevel.Information:
          logger.notice(
            message,
            MessageParameters(title=title, file=self.path, line=lint.line),
          )

  def build(self):
    builder = Builder(self.path, self.sources_dir)
    builder.build()


class FatalLintsError(ActionRuntimeError):
  def __init__(self, file: str) -> None:
    super().__init__(
      "More than one critical lint was found.", 3, MessageParameters(file=file)
    )
