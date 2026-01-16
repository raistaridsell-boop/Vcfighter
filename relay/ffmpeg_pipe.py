import subprocess
from relay import state

def start_ffmpeg():
    """
    stdin  <- control VC audio (raw)
    stdout -> target VC audio (raw) with volume filter
    """
    cmd = [
        "ffmpeg",
        "-loglevel", "quiet",
        "-f", "s16le",
        "-ar", "48000",
        "-ac", "2",
        "-i", "pipe:0",
        "-filter:a", f"volume={state.volume}",
        "-f", "s16le",
        "pipe:1"
    ]
    return subprocess.Popen(
        cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE
    )
