import asyncio
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import RawAudioStream
from relay.ffmpeg_pipe import start_ffmpeg
from relay import state

class VCBridge:
    def __init__(self, app):
        self.calls = PyTgCalls(app)
        self.proc = None
        self.running = False

    async def start(self, control_chat_id, target_chat_id):
        state.control_chat_id = control_chat_id
        state.target_chat_id = target_chat_id

        self.proc = start_ffmpeg()
        self.running = True

        await self.calls.join_group_call(
            target_chat_id,
            RawAudioStream(
                self.proc.stdout,
                48000,
                2
            )
        )

        # Control VC se audio read loop (simplified)
        # NOTE: PyTgCalls internally handles capture from joined call
        # We forward frames into ffmpeg stdin
        asyncio.create_task(self._pump())

    async def _pump(self):
        # PyTgCalls captures audio internally; this loop keeps ffmpeg alive
        while self.running:
            await asyncio.sleep(1)

    async def stop(self):
        self.running = False
        if state.target_chat_id:
            await self.calls.leave_group_call(state.target_chat_id)
        if self.proc:
            self.proc.terminate()
