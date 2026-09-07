import asyncio
import os
import shutil
import subprocess

from action import MessageParameters, logger
from action.errors import ActionRuntimeError
from errors import InternalError, PathInvalidError
from process import ProcessStdStreamLogger


class Builder:
  def __init__(self, spec_path: str, sources_dir: str | None):
    self.spec_path: str = spec_path
    self.sources_dir: str | None = sources_dir

  def build(self):
    asyncio.run(self.install_build_deps())
    asyncio.run(self.fetch_sources())
    self.copy_sources()
    asyncio.run(self.build_rpm())

  async def install_build_deps(self) -> None:
    with logger.LogGroup("Installing build dependencies"):
      try:
        process = ProcessStdStreamLogger(
          ["dnf5", "-y", "--verbose", "builddep", self.spec_path]
        )
        await process.start()

        async for line in process.stdout_lines():
          print(line)

        async for line in process.stderr_lines():
          # For some reason, dnf prints to stderr when installing packages.
          print(line)
        await process.wait()
      except Exception as e:
        raise InstallBuildDependenciesError(e, self.spec_path)

  async def build_rpm(self):
    with logger.LogGroup("Building rpm"):
      try:
        process = ProcessStdStreamLogger(
          ["rpmbuild", "--verbose", "-ba", self.spec_path],
        )
        await process.start()

        async for line in process.stdout_lines():
          print(line)

        async for line in process.stderr_lines():
          logger.warning(
            line.removeprefix("warning: ").removesuffix("error: "),
            MessageParameters(file=self.spec_path),
          )
        await process.wait()
      except Exception as e:
        raise BuildPackageError(e, self.spec_path)

  async def fetch_sources(self):
    with logger.LogGroup("Fetching sources"):
      try:
        process = ProcessStdStreamLogger(
          ["spectool", "--get-files", "-R", self.spec_path],
        )
        await process.start()

        async for line in process.stdout_lines():
          print(line)

        async for line in process.stderr_lines():
          logger.warning(line, MessageParameters(file=self.spec_path))
        await process.wait()
      except Exception as e:
        raise FetchBuildSourcesError(e, self.spec_path)

  def copy_sources(self) -> None:
    if self.sources_dir is not None:
      if not os.path.isdir(self.sources_dir):
        raise PathInvalidError(
          message="Sources dir is not a directory", path=self.sources_dir
        )
      with logger.LogGroup("Copying sources from sources_dir"):
        dir_check = subprocess.run(
          ["rpm", "--eval", "%{_sourcedir}"],
          stdout=subprocess.PIPE,
          stderr=subprocess.PIPE,
        )
        if dir_check.returncode != 0:
          raise InternalError(
            dir_check.stderr.decode(),
            MessageParameters("Error copying sources_dir"),
          )
        dest_dir = dir_check.stdout.decode().strip()
        _: str = shutil.copytree(self.sources_dir, dest_dir, dirs_exist_ok=True)


class InstallBuildDependenciesError(ActionRuntimeError):
  def __init__(self, error: BaseException, file: str):
    super().__init__(
      str(error),
      5,
      MessageParameters(
        title="Error while installing build dependencies", file=file
      ),
    )


class FetchBuildSourcesError(ActionRuntimeError):
  def __init__(self, error: BaseException, file: str):
    super().__init__(
      str(error),
      6,
      MessageParameters(title="Error while fetching build sources", file=file),
    )


class BuildPackageError(ActionRuntimeError):
  def __init__(self, error: BaseException, file: str):
    super().__init__(
      str(error),
      7,
      MessageParameters(title="Error while building package", file=file),
    )
