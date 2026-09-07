from pathlib import Path

from action import action, logger
from rpmkit.spec import Specfile

if __name__ == "__main__":
  with action.Action() as (workspace, inputs, outputs):
    sources_dir: Path | None = None
    if inputs.SOURCES_DIR is not None:
      sources_dir = Path(inputs.SOURCES_DIR)
    build_dir = Path(workspace).joinpath("build")
    build_dir.mkdir(exist_ok=True)
    spec = Specfile(
      spec=Path(inputs.SPEC_FILE),
      build_output_dir=build_dir,
      sources_dir=sources_dir,
    )

    with logger.LogGroup("Linting spec file"):
      spec.lint()

    with logger.LogGroup("Building rpm"):
      outputs.rpm_directory, outputs.source_rpm_directory = spec.build()
