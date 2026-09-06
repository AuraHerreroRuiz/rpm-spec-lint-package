import os

from action import logger
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

  def lint(self) -> int:
    """Logs the lints the Specfile, returns the amount of fatal lints"""
    linter = Linter(self.path)
    fatals, self.lints = linter.lint()
    self.print_lints()
    return fatals

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
            message=message, title=title, file=self.path, line=lint.line
          )
        case LintLevel.Warning:
          logger.warning(
            message=message, title=title, file=self.path, line=lint.line
          )
        case LintLevel.Information:
          logger.notice(
            message=message, title=title, file=self.path, line=lint.line
          )

  def build(self):
    builder = Builder(self.path, self.sources_dir)
    builder.build()
