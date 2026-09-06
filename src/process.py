import asyncio


class ProcessRunner:
  def __init__(self, command_args: list[str]):
    self.command_args: list[str] = command_args
    self._process: asyncio.subprocess.Process | None = None

  async def start(self):
    self._process = await asyncio.create_subprocess_exec(
      *self.command_args,
      stdout=asyncio.subprocess.PIPE,
      stderr=asyncio.subprocess.PIPE
    )

  def stdout_lines(self):
    return self._output_lines(stream=self._get_running_process().stdout)

  def stderr_lines(self):
    return self._output_lines(stream=self._get_running_process().stderr)


  async def _output_lines(self,stream: asyncio.StreamReader | None):
    if stream is None:
      raise RuntimeError("Not started")
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
      raise RuntimeError("Not started")
    return self._process

  async def wait(self) -> int:
    if self._process is None:
      raise RuntimeError("Not started")
    return await self._process.wait()
