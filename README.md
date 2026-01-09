# Legion Go 2 Brightness

Decky Loader plugin that fixes brightness control for Legion Go 2 in Steam Game Mode.

## Installation

### From Git URL (Recommended)

1. Open the Quick Access Menu (QAM) → Decky → Settings (gear icon)
2. Go to "Developer" section
3. Enable "Developer Mode" if not already enabled
4. Click "Install Plugin from URL"
5. Enter: `https://github.com/jorgemmsilva/decky-plugin-fix-lego2-brightness-cachyos`
6. Click "Install"

### From GitHub Release

1. Download the latest release zip
2. Extract to `~/homebrew/plugins/`
3. Restart Decky Loader (QAM → Decky → Settings → Reload)

### Manual Build

```bash
git clone https://github.com/jorgemmsilva/decky-plugin-fix-lego2-brightness-cachyos.git
cd decky-plugin-fix-lego2-brightness-cachyos
pnpm install
pnpm build
```

Copy `plugin.json`, `main.py`, and `dist/` to `~/homebrew/plugins/legion-go2-brightness/`

## Usage

Open the Quick Access Menu (QAM) and find "LGO2 Brightness" with the sun icon. Use the slider to adjust brightness.

## Technical Details

- Reads max brightness from `/sys/class/backlight/amdgpu_bl1/max_brightness`
- Writes percentage-scaled value to `/sys/class/backlight/amdgpu_bl1/brightness`
- Requires root flag in Decky (automatically handled)

## License

MIT
