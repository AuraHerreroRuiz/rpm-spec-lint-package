from typing import Any, Literal, TypedDict


class MessagesSeverity(TypedDict,total=True):
    I: int
    """
    Informative messages
    """
    W: int
    """
    Warning messages
    """
    E: int
    """
    Error messages
    """

class Filter:
    """
    Handle all printing/formatting/filtering of the rpmlint output.

    Nothing gets printed out until the end of all runs and all errors are
    sorted and formatted based on the rules specified by the user/config
    """

    score: int = 0
    """How many bad hits we already collected while collecting issues"""
    error_details: dict[Any, Any] = {}
    """Dictionary containing mapped values of descriptions for the errors."""
    printed_messages: MessagesSeverity = {'I': 0,'W':0,'E':0}
    """Counter of how many issues we encountered"""
    promoted_to_error: int
    """Number of promoted warnings and infos to errors"""
    filtered_out: int
    """Number of messaged that are filtered out"""
    results: list[str] = []
    """Messages"""

    def __init__(self, config) -> None:
        """
        Initialize options from configuration and load rpmlint descriptions.

        Args:
            config: Config object with parsed rpmlint configuration.
        """
        ...

    def add_info(self, level, package, rpmlint_issue, *details) -> None:
        """
        Format rpmlint issue output and add it to self.results.

        It creates formatted and colored output consisting of all information
        about rpmlint issue given by the arguments.

        Args:
            level: A string with level of the rpmlint issue ('E' - Error,
                   'W' - Warning, 'I' - Info
            package: Pkg object representing processed package
            rpmlint_issue: A string representing the name of the rpmlint
                           issue
            *details: Details of the rpmlint issue
        """
        ...

    def print_results(self, results, config=...) -> str:
        """
        Provide all the information about the specified package.

        If there is description to be provided it needs to be provided only
        once per rpmlint_issue.

        Args:
            results: A list with rpmlint messages.
            config: parsed configuration file that is used as a source for
                    new description strings

        Returns:
            A string with final rpmlint output.
        """
        ...

    def get_description(self, rpmlint_issue, config=...) -> str:
        """
        Get description for specified rpmlint issue (error, warning or info).

        Args:
            rpmlint_issue: A string with the rpmlint error/warning/info name
            config: parsed configuration file that is used as a source for
                    custom description strings ([Descriptions] table in toml
                    syntax)

        Returns:
            A string with description for specified rpmlint issue. Empty
            content does not cause an issue and we just return empty content
        """
        ...

    def validate_filters(self, pkg) -> None:
        ...



