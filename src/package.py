from pathlib import Path
import re
from enum import Enum
import dnf
import os

from rpmlint.filter import Filter

import logger

class Level(Enum):
    Information = "I"
    Warning = "W"
    Error = "E"

dnf = dnf.Base()
dnf.read_all_repos()
dnf.fill_sack()

from rpmlint.lint import Lint

class Specfile:
    def __init__(self,path : str | None) -> None:
        if path is None or not os.path.isfile(path):
            raise FileNotFoundError
        self.path: str = path
        self._linter: Lint = Lint(options={
            'rpmfile': [],
            # Has to be empty, otherwise it will exit, we want to use the output with validate_file
            'checks': "",
            'config': [],
            'explain': [],
            'ignore_unused_rpmlintrc': False,
            'installed': [],
            'permissive': False,
            'print_config': False,
            'profile': False,
            'rpmlintrc': [],
            'strict': False,
            'time_report': False,
            'verbose': False
        })
        self.lints: list[Linting] = []


    def lint(self) -> int:
        """Logs the lints the Specfile, returns the amount of fatal lints"""
        self._linter.validate_file(Path(self.path),True)
        self._parseLintOutput()
        self._printLintOutput()
        return self._linter.output.score
    # def installBuildDeps(self) -> None:
        # spec.
        # dnf.install_specs([""])
        # dnf.resolve()

    def _parseLintOutput(self):
        for result in self._linter.output.results:
            lintMessage = re.search("(?P<file>.+?\\.[^.]+?)(?:\\.(?P<arch>.+?))?:(?:(?P<line>\\d+):)? (?P<level>[IWE]): (?P<issue>.+)",result)
            if lintMessage is None:
                raise TypeError
            lint = lintMessage.groupdict()
            file = lint["file"]
            issue = lint["issue"]
            level = lint["level"]
            if not (isinstance(file,str) and isinstance(issue,str)):
                raise TypeError

            self.lints.append(Linting(
                file = file,
                arch = lint["arch"] if lint["arch"] else None,
                line = int(lint["line"]) if lint["line"] else None,
                level = Level(level),
                issue = issue,
            ))
    def _printLintOutput(self):
        for lint in self.lints:
            message: str
            title: str | None
            if lint.issue in self._linter.output.error_details:
                title = lint.issue
                message = self._linter.output.error_details[lint.issue]
            else:
                title = None
                message = lint.issue
            match lint.level:
                case Level.Error:
                    logger.Error(message=message,title=title,file=self.path,line=lint.line)
                case Level.Warning:
                    logger.Warning(message=message,title=title,file=self.path,line=lint.line)
                case Level.Information:
                    logger.Notice(message=message,title=title,file=self.path,line=lint.line)



class Linting:
    "Represents a lint message"
    def __init__(self,file,arch,line,level,issue):
        self.file = file
        self.arch = arch
        self.line = line
        self.level = level
        self.issue = issue

    file: str
    "File referred to by the lint message"

    arch: str | None
    "Architecture of the file"

    line: int | None
    "Line of the file containing the issue"

    level: Level

    issue: str
    "Rpmlint issue"

