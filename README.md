# RPM Spec Lint & Package

This GitHub Action lints and builds an RPM package from a spec file.

It downloads sources as specified, and can also copy from an input directory.

## Package Distribution

Packages are built against "fedora:latest". This can be changed in the dockerfile.

There is currently no support for other versions, if there is a need feel free to open an issue.

## Usage

You can look at [.github/workflows/test.yaml] for example usage.

### Exit codes
|Code|Error Name|Cause|
|:----:|:----------:|:-----|
|1|ActionEnvironmentInvalidError|The expected action environment variable is invalid. Please check your workflow configuration and runner.
|2|UndefinedInputError|One of the action inputs is missing. Check your workflow configuration.|
|3|FatalLintsError|Your spec file has one or more fatal lints. Use rpmlint or read the logs to correct the issue.|
|4|PathInvalidError|One of the paths specified is nor valid.|
|5|InstallBuildDependenciesError|There was an error installing build dependencies. Check your spec file.
|6|FetchBuildSourcesError|There was an error installing build dependencies. Check your spec file.
|7|BuildPackageError|There was an error in the package build process. Check your spec file.
|8|Internal Error|An implementation error occurred, if possible report an issue.
|9|Unexpected Error|Some unknown error occurred, if possible report an issue.

## Credits

- [naveenrajm7/rpmbuild](https://github.com/naveenrajm7/rpmbuild): Inspiration for this project. Even though I ended up re-implementing the entire action in python, their action was an inspiration for this project.
