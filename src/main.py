from actions import action_io, logger
from errors import PathInvalidError
from rpmkit.spec import Specfile

if __name__ == "__main__":
  workflow: action_io.Workflow = action_io.Workflow()
  spec_file_name = workflow.get_input_or_error("spec_file")
  sources_dir = workflow.get_input("sources_dir")
  try:
    spec = Specfile(spec_file_name, sources_dir)

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
