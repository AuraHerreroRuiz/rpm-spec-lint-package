import asyncio
import os
import shutil
from pathlib import Path
from typing import Any, TypeAlias

import process
from action import MessageParameters, logger
from action.errors import ActionRuntimeError
from errors import InternalError, PathInvalidError
from process import ProcessStdStreamLogger


class Builder:
  SourceRPMSPath: TypeAlias = Path
  RPMSPath: TypeAlias = Path

  def __init__(
    self, spec: Path, build_output_dir: Path, sources_dir: Path | None
  ):
    self.spec: Path = spec
    self.build_output_dir: Path = build_output_dir
    self.sources_dir: Path | None = sources_dir
    self.rpms_dir: "Builder.RPMSPath" = build_output_dir.joinpath("RPMS")
    self.rpms_dir.mkdir(exist_ok=True)
    self.source_rpms_dir: "Builder.SourceRPMSPath" = build_output_dir.joinpath(
      "SRPMS"
    )
    self.source_rpms_dir.mkdir(exist_ok=True)
    self._rpm_build_command_macro_definitions: list[str] = [
      "--define",
      f"_rpmdir {self.rpms_dir}",
      "--define",
      f"_srcrpmdir {self.source_rpms_dir}",
    ]

  def build(self) -> tuple[RPMSPath, SourceRPMSPath]:
    asyncio.run(self._install_build_deps())
    asyncio.run(self._fetch_sources())
    self._copy_sources()
    asyncio.run(self._build_rpm())
    return self.rpms_dir, self.source_rpms_dir

  async def _install_build_deps(self) -> None:
    with logger.LogGroup("Installing build dependencies"):
      try:
        process = ProcessStdStreamLogger(
          ["dnf5", "-y", "builddep", str(self.spec)]
        )
        await process.start()

        async for line in process.stdout_lines():
          print(line)

        async for line in process.stderr_lines():
          # For some reason, dnf prints to stderr when installing packages.
          print(line)
        await process.wait()
      except Exception as e:
        raise InstallBuildDependenciesError(e, str(self.spec))

  async def _build_rpm(self):
    with logger.LogGroup("Building rpm"):
      try:
        process = ProcessStdStreamLogger(
          ["rpmbuild"]
          + self._rpm_build_command_macro_definitions
          + [
            "--quiet",
            "-ba",
            str(self.spec),
          ],
        )
        await process.start()

        async for line in process.stdout_lines():
          print(line)

        async for line in process.stderr_lines():
          logger.warning(
            line.removeprefix("warning: ").removesuffix("error: "),
            MessageParameters(file=str(self.spec)),
          )
        await process.wait()
      except Exception as e:
        raise BuildPackageError(e, str(self.spec))

  async def _fetch_sources(self):
    with logger.LogGroup("Fetching sources"):
      try:
        process = ProcessStdStreamLogger(
          ["spectool", "--get-files", "-R", str(self.spec)],
        )
        await process.start()

        async for line in process.stdout_lines():
          print(line)

        async for line in process.stderr_lines():
          logger.warning(line, MessageParameters(file=str(self.spec)))
        await process.wait()
      except Exception as e:
        raise FetchBuildSourcesError(e, str(self.spec))

  def _copy_sources(self) -> None:
    if self.sources_dir is not None:
      if not self.sources_dir.is_dir():
        raise PathInvalidError(
          message="Sources dir is not a directory", path=str(self.sources_dir)
        )
      with logger.LogGroup("Copying sources from sources_dir"):
        try:
          dir_check, _ = process.run(["rpmbuild", "--eval", "%{_sourcedir}"])
          dest_dir = dir_check.strip()
          _: str = shutil.copytree(
            self.sources_dir, dest_dir, dirs_exist_ok=True
          )
        except Exception as e:
          raise InternalError(
            str(e),
            parameters=MessageParameters("Error copying sources_dir"),
          )

  # def _get_build_output_paths(self) -> tuple[RPMSPath, SourceRPMSPath]:
  #   try:
  #     rpms_dir_macro, _ = process.run(
  #       [
  #         "rpmbuild",
  #         "--define",
  #         f"'_topdir {self.build_output_dir}'",
  #         "--eval",
  #         "%{_rpmdir}",
  #       ]
  #     )
  #     source_rpms_dir_macro, _ = process.run(
  #       [
  #         "rpmbuild",
  #         "--define",
  #         f"'_topdir {self.build_output_dir}'",
  #         "--eval",
  #         "%{_srcrpmdir}",
  #       ]
  #     )

  #     rpms_dir = Path(rpms_dir_macro.strip()).expanduser().resolve()
  #     source_rpms_dir = (
  #       Path(source_rpms_dir_macro.strip()).expanduser().resolve()
  #     )

  #     return rpms_dir, source_rpms_dir
  #   except Exception as e:
  #     raise InternalError(
  #       str(e),
  #       parameters=MessageParameters("Error compiling artifacts list"),
  #     )


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
