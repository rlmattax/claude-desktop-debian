# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository automates the creation of .deb packages and AppImages for Claude Desktop on Linux systems. It's an unofficial build system that:

- Downloads the official Windows Claude Desktop installer
- Extracts and adapts the Electron application for Linux
- Creates both Debian packages (.deb) and AppImage formats
- Supports both amd64 and arm64 architectures
- Features automated version detection and daily builds

## Development Commands

### Main Build Script
```bash
# Build .deb package (default)
./build.sh

# Build AppImage
./build.sh --build appimage

# Build without cleaning intermediate files
./build.sh --clean no

# Test flag parsing without building
./build.sh --test-flags
```

### Version Checking
```bash
# Check for upstream Claude Desktop updates
python3 scripts/check-upstream-version.py

# Install Python dependencies
pip install -r requirements.txt
```

### CI/CD Testing
```bash
# Test individual build workflows locally with act
act workflow_dispatch -W .github/workflows/ci.yml
act workflow_dispatch -W .github/workflows/check-for-updates.yml

# Run shellcheck on scripts
shellcheck build.sh scripts/*.sh

# Run codespell on text files
codespell
```

## Architecture

### Build Process Flow
1. **Architecture Detection**: Automatically detects host system (amd64/arm64)
2. **Dependency Installation**: Installs required system packages via apt
3. **Resource Download**: Downloads Windows installer from Google Cloud Storage
4. **Extraction**: Uses 7zip to extract installer and nupkg contents
5. **Icon Processing**: Extracts icons using wrestool/icotool for Linux desktop integration
6. **App Processing**: Unpacks app.asar, replaces Windows-specific native module with Linux stub
7. **Electron Bundling**: Downloads and bundles local Electron installation
8. **Packaging**: Calls format-specific scripts (Debian or AppImage)

### Key Scripts
- `build.sh`: Main orchestration script with architecture detection and dependency management
- `scripts/build-deb-package.sh`: Creates Debian packages with proper desktop integration
- `scripts/build-appimage.sh`: Creates portable AppImage files with bundled dependencies
- `scripts/check-upstream-version.py`: Automated version monitoring with binary analysis

### Automation System
- **Daily Monitoring**: `.github/workflows/check-for-updates.yml` runs at 12:00 UTC
- **Version Detection**: Downloads 2MB chunks to extract version info from installers
- **Metadata Tracking**: Maintains `.claude-version-metadata` with ETag/size/version data
- **Automatic Builds**: Triggers CI pipeline when changes detected
- **Automatic Releases**: Downloads build artifacts and creates GitHub releases with all packages
- **Complete Workflow**: Detection → Build → Release, fully automated end-to-end

### Native Module Replacement
The build process replaces Windows-specific `claude-native` module with a Linux stub implementation providing:
- Keyboard key mappings for global hotkeys
- Window management functions (maximize, flash, etc.)
- System integration stubs (notifications, progress bar, etc.)

### Title Bar Fix
The build script modifies the main renderer JavaScript to enable the native title bar on Linux by removing the Windows-only check pattern `if(!isWindows && isMainWindow)`.

## Build Dependencies

**System packages** (installed automatically):
- `p7zip-full`: Archive extraction
- `wget`: File downloading
- `icoutils`: Icon extraction and conversion
- `imagemagick`: Image processing
- `nodejs`, `npm`: JavaScript runtime
- `dpkg-dev`: Debian package tools (for .deb builds)

**Node.js packages** (installed locally during build):
- `electron`: Runtime bundled with packages
- `@electron/asar`: Archive manipulation

## Output Formats

### Debian Package (.deb)
- Standard Linux package format
- Includes desktop entry, icons, dependencies
- Creates launcher script with Wayland detection
- Sets up chrome-sandbox permissions in postinst
- Installs to `/usr/lib/claude-desktop/`

### AppImage
- Self-contained portable executable
- Bundles all dependencies including Electron
- Includes AppRun script with `--no-sandbox` flag
- Requires AppImageLauncher for proper desktop integration
- Supports URI scheme handling when integrated

## Version Metadata

The `.claude-version-metadata` file tracks:
```json
{
  "check_time": "2025-06-30T12:13:20.451595",
  "architectures": {
    "amd64": {
      "etag": "6d47febaf3beb7efb454e13f4815d871",
      "size": null,
      "last_modified": "2025-06-29T22:37:53",
      "url": "https://storage.googleapis.com/.../Claude-Setup-x64.exe",
      "version": "0.11.6"
    },
    "arm64": { ... }
  }
}
```

This file is committed to track version changes and trigger builds.

## Common Troubleshooting

### Build Issues
- **Missing dependencies**: The script auto-installs via `apt` but may need `sudo` access
- **Electron download failures**: Check network connectivity and npm configuration
- **Architecture mismatch**: Script auto-detects but verify with `dpkg --print-architecture`

### Runtime Issues
- **Scaling problems**: Right-click taskbar icon and quit cleanly to save window state
- **Wayland compatibility**: Launcher script auto-detects and adds appropriate flags
- **Sandbox errors**: AppImage uses `--no-sandbox`; .deb sets chrome-sandbox permissions

### Automation Issues
- **Version detection failures**: Check `scripts/check-upstream-version.py` exit codes (0=no changes, 1=changes, 2=error)
- **Build trigger failures**: Verify GitHub Actions workflows and secrets
- **Metadata corruption**: Regenerate `.claude-version-metadata` by deleting and re-running check script

## Testing Locally

```bash
# Test build without cleanup to inspect intermediate files
./build.sh --clean no

# Test version checker
python3 scripts/check-upstream-version.py

# Test AppImage
./claude-desktop-*.AppImage

# Test .deb installation
sudo dpkg -i claude-desktop_*.deb
```

The automation system maintains professional build quality while adding intelligent upstream monitoring, making this a self-maintaining package repository.