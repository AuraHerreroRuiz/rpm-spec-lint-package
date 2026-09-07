import asyncio
import subprocess

from errors import InternalError


class ProcessStdStreamLogger:
  """
  Runs a process and asynchronously logs standard streams.
  Use stdout_lines() and stderr_lines() to read them.
  Raises NotZeroReturnError if the process returns a non zero exit code.
  Raises UnexpectedProcessAccessError if start() is not used before reading std streams.
  """  # noqa: E501

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
      raise NotZeroReturnError(return_code, None, None)
    return


StdOut = str
StdErr = str


def run(command_args: list[str]) -> tuple[StdOut, StdErr]:
  """
  Runs a process and returns the standard streams.
  Raises UnexpectedProcessAccessError if start() is not used before reading std streams.
  """  # noqa: E501
  process = subprocess.run(
    command_args,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
  )
  if process.returncode != 0:
    raise NotZeroReturnError(
      return_code=process.returncode,
      stdout=process.stdout.decode(),
      stderr=process.stderr.decode(),
    )
  return process.stdout.decode(), process.stderr.decode()


class UnexpectedProcessAccessError(InternalError):
  def __init__(self):
    super().__init__(
      "Process status fetched while it has not started. "
      + "Make sure the implementation uses start() first."
    )


class NotZeroReturnError(Exception):
  def __init__(
    self, return_code: int, stderr: StdErr | None, stdout: StdOut | None
  ) -> None:
    self.return_code: int = return_code
    self.stdout: StdOut | None = stdout
    self.stderr: StdErr | None = stderr
    message = f"The process returned the code {return_code}"
    if stderr is not None:
      message += f"\n--- StdErr: ---\n {stderr}"
    if stdout is not None:
      message += f"\n--- StdOut: ---\n {stdout}"
    super().__init__(message)
