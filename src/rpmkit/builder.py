import asyncio
import os
import shutil
import subprocess

from action import logger
from errors import NotZeroReturnError, PathInvalidError
from process import ProcessRunner


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
      process = ProcessRunner(
        ["dnf5", "-y", "--quiet", "builddep", self.spec_path]
      )
      await process.start()

      async for line in process.stdout_lines():
        print(line)

      async for line in process.stderr_lines():
        # For some reason, dnf prints to sterr when installing packages.
        print(line)
      return_code = await process.wait()
      if return_code != 0:
        raise NotZeroReturnError(return_code)

  async def build_rpm(self):
    with logger.LogGroup("Building rpm"):
      process = ProcessRunner(
        ["rpmbuild", "--quiet", "-ba", self.spec_path],
      )
      await process.start()

      async for line in process.stdout_lines():
        print(line)

      async for line in process.stderr_lines():
        logger.warning(line.removeprefix("warning: ").removesuffix("error: "))

      return_code = await process.wait()
      if return_code != 0:
        raise NotZeroReturnError(return_code)

  async def fetch_sources(self):
    with logger.LogGroup("Fetching sources"):
      process = ProcessRunner(
        ["spectool", "--get-files", "-R", self.spec_path],
        # stderr=logger.LoggerIO(logger.error),
      )
      await process.start()

      async for line in process.stdout_lines():
        print(line)

      async for line in process.stderr_lines():
        logger.warning(line)

      return_code = await process.wait()
      if return_code != 0:
        raise NotZeroReturnError(return_code)

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
          logger.error(dir_check.stderr.decode(), "Error copying sources_dir")
          raise NotZeroReturnError(dir_check.returncode)
        dest_dir = dir_check.stdout.decode().strip()
        _: str = shutil.copytree(self.sources_dir, dest_dir, dirs_exist_ok=True)
