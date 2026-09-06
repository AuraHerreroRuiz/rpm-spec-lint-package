class PathInvalidError(Exception):
  def __init__(self, message: str, path: str) -> None:
    super().__init__(message)
    self.path: str = path


class NotZeroReturnError(Exception):
  def __init__(self, return_code: int, message: str | None = None) -> None:
    self.return_code: int = return_code
    if message is None:
      super().__init__(f"The task returned the code {return_code}")
    else:
      super().__init__(message)
