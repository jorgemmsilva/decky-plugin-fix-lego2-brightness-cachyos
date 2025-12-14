import os
import struct
import subprocess
import decky

BRIGHTNESS_ATOM = "GAMESCOPE_SDR_ON_HDR_CONTENT_BRIGHTNESS"
DISPLAY = ":0"

MAX_BRIGHTNESS_NITS: float = 500.0
MIN_BRIGHTNESS_NITS: float = 5.0


def int_bits_to_float(int_val: int) -> float:
    """Convert 32-bit integer (as stored by xprop) to float."""
    return struct.unpack('f', struct.pack('I', int_val))[0]


def float_to_int_bits(float_val: float) -> int:
    """Convert float to 32-bit integer representation for xprop."""
    return struct.unpack('I', struct.pack('f', float_val))[0]


class Plugin:
    async def get_brightness(self) -> int:
        result = subprocess.run(
            ["xprop", "-root", BRIGHTNESS_ATOM],
            capture_output=True,
            text=True,
            env={**os.environ, "DISPLAY": DISPLAY}
        )
        output = result.stdout.strip()
        if "=" in output:
            int_val = int(output.split("=")[-1].strip())
            nits = int_bits_to_float(int_val)
            percent = (nits - MIN_BRIGHTNESS_NITS) / (MAX_BRIGHTNESS_NITS - MIN_BRIGHTNESS_NITS) * 100
            return round(max(0, min(100, percent)))
        return 50

    async def set_brightness(self, percent: int) -> bool:
        percent = max(0, min(100, percent))
        nits = MIN_BRIGHTNESS_NITS + (percent / 100) * (MAX_BRIGHTNESS_NITS - MIN_BRIGHTNESS_NITS)
        int_val = float_to_int_bits(nits)
        result = subprocess.run(
            ["xprop", "-root", "-f", BRIGHTNESS_ATOM, "32c", "-set", BRIGHTNESS_ATOM, str(int_val)],
            capture_output=True,
            text=True,
            env={**os.environ, "DISPLAY": DISPLAY}
        )
        return result.returncode == 0

    async def _main(self):
        decky.logger.info(f"Legion Go 2 Brightness plugin loaded, range={MIN_BRIGHTNESS_NITS}-{MAX_BRIGHTNESS_NITS} nits")

    async def _unload(self):
        decky.logger.info("Legion Go 2 Brightness plugin unloaded")
