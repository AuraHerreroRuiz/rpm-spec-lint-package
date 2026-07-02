import actionIo
import logger
import package


if __name__ == "__main__":
    workflow = actionIo.workflow()
    specFileName = workflow.getInput("spec_file")
    # specRepoPath = f"SPECS/{specFileName}"

    logger.Notice("Packaging rpm from spec file",file=specFileName)
    try:
        logger.startLinesGroup("Linting")
        spec = package.Specfile(specFileName)
        errorNumber = spec.lint()
        logger.endLinesGroup()
        if errorNumber > 0:
            logger.ErrorAndTerminate("More than one critical lint")
    except FileNotFoundError:
        logger.ErrorAndTerminate(f"Specfile {specFileName} does not exist",file=specFileName,errorCode=1)
    except Exception as e:
        logger.ErrorAndTerminate(repr(e),title="Unknown exception")
