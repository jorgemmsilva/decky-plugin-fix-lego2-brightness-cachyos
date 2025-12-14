import os
import decky

BACKLIGHT_PATH = "/sys/class/backlight/amdgpu_bl1"
BRIGHTNESS_FILE = os.path.join(BACKLIGHT_PATH, "brightness")
MAX_BRIGHTNESS_FILE = os.path.join(BACKLIGHT_PATH, "max_brightness")


class Plugin:
    max_brightness: int = None

    async def get_brightness(self) -> int:
        """Get current brightness as percentage (0-100)"""
        try:
            decky.logger.info(f"Reading brightness from {BRIGHTNESS_FILE}")
            with open(BRIGHTNESS_FILE, "r") as f:
                current = int(f.read().strip())
            result = round((current / self.max_brightness) * 100)
            decky.logger.info(f"Current brightness: {result}%")
            return result
        except Exception as e:
            decky.logger.error(f"Failed to get brightness: {e}")
            return -1

    async def set_brightness(self, percent: int) -> bool:
        """Set brightness from percentage (0-100)"""
        try:
            # Clamp to valid range
            percent = max(1, min(100, percent))
            # Ensure at least 1 to prevent black screen (1% of max could round to 0)
            value = max(1, round((percent / 100) * self.max_brightness))
            decky.logger.info(f"Setting brightness to {percent}% (raw value: {value})")

            # Use low-level OS calls to write directly to sysfs
            fd = os.open(BRIGHTNESS_FILE, os.O_WRONLY)
            try:
                written = os.write(fd, f"{value}\n".encode())
                decky.logger.info(f"Wrote {written} bytes to {BRIGHTNESS_FILE}")
            finally:
                os.close(fd)

            return True
        except Exception as e:
            decky.logger.error(f"Failed to set brightness: {e}")
            return False

    async def _main(self):
        decky.logger.info("Legion Go 2 Brightness plugin starting...")
        try:
            with open(MAX_BRIGHTNESS_FILE, "r") as f:
                self.max_brightness = int(f.read().strip())
            decky.logger.info(f"Max brightness: {self.max_brightness}")
        except Exception as e:
            decky.logger.error(f"Failed to read max brightness: {e}")

    async def _unload(self):
        decky.logger.info("Legion Go 2 Brightness plugin unloading...")
