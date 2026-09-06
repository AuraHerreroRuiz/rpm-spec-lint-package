from action import action, logger
from errors import PathInvalidError
from rpmkit.spec import Specfile

if __name__ == "__main__":
  with action.Action() as (inputs, artifcats):

    try:
      spec = Specfile(inputs.SPEC_FILE,inputs.SOURCES_DIR)

      with logger.LogGroup("Linting spec file"):
        error_number = spec.lint()
        if error_number > 0:
          logger.error_and_terminate("More than one critical lint")

      with logger.LogGroup("Building rpm"):
        spec.build()

    except PathInvalidError as e:
      logger.error_and_terminate(str(e), file=str(e.path), error_code=1)
    except Exception as e:
      logger.error_and_terminate(repr(e), title="Unknown exception")
