from action import action, logger
from rpmkit.spec import Specfile

if __name__ == "__main__":
  with action.Action() as (inputs, artifcats):
    spec = Specfile(inputs.SPEC_FILE, inputs.SOURCES_DIR)

    with logger.LogGroup("Linting spec file"):
      spec.lint()

    with logger.LogGroup("Building rpm"):
      spec.build()
