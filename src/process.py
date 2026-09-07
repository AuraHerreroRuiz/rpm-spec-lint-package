import asyncio

from errors import InternalError


class ProcessStdStreamLogger:
  def __init__(self, command_args: list[str]):
    self.command_args: list[str] = command_args
    self._process: asyncio.subprocess.Process | None = None

  async def start(self):
    self._process = await asyncio.create_subprocess_exec(
      *self.command_args,
      stdout=asyncio.subprocess.PIPE,
      stderr=asyncio.subprocess.PIPE,
    )

  def stdout_lines(self):
    return self._output_lines(stream=self._get_running_process().stdout)

  def stderr_lines(self):
    return self._output_lines(stream=self._get_running_process().stderr)

  async def _output_lines(self, stream: asyncio.StreamReader | None):
    if stream is None:
      raise UnexpectedProcessAccessError()
    while True:
      line_bytes: bytes = await stream.readline()
      if not line_bytes:
        break
      line = line_bytes.decode()
      if line.isspace():
        continue
      yield line

  def _get_running_process(self):
    if self._process is None:
      raise UnexpectedProcessAccessError()
    return self._process

  async def wait(self) -> None:
    if self._process is None:
      raise UnexpectedProcessAccessError()
    return_code = await self._process.wait()
    if return_code != 0:
      raise NotZeroReturnError(return_code)
    return


class UnexpectedProcessAccessError(InternalError):
  def __init__(self):
    super().__init__(
      "Process status fetched while it has not started. "
      + "Make sure the implementation uses start() first."
    )


class NotZeroReturnError(Exception):
  def __init__(self, return_code: int) -> None:
    self.return_code: int = return_code
    super().__init__(f"The process returned the code {return_code}")
