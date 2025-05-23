# Claude Desktop for Linux 🐧

***Unofficial Claude Desktop packages for Debian/Ubuntu systems with automated builds!***

This project provides automated .deb and AppImage packages for Claude Desktop on Linux, with daily monitoring for upstream updates and automatic builds when new versions are released.

> **⚠️ Important:** This is an unofficial build. If you encounter issues with this build script, please report them here - don't contact Anthropic support about unofficial packages.

## 🤖 Automated Builds

This repository features **automated version detection and building**:

- **Daily Monitoring**: Automatically checks for new Claude Desktop versions every day at 12:00 UTC
- **Automatic Builds**: Triggers builds for both amd64 and arm64 architectures when updates are detected  
- **Multi-Format Packages**: Produces both .deb packages and AppImage files
- **GitHub Releases**: Automatically creates releases with downloadable packages
- **Issue Notifications**: Creates GitHub issues to announce new version availability

**Latest Version Tracked**: `0.9.3` (both amd64 and arm64)

Check the [Releases page](https://github.com/rlmattax/claude-desktop-debian/releases) for the latest automated builds, or [Actions](https://github.com/rlmattax/claude-desktop-debian/actions) to see builds in progress.

## 📦 Quick Installation

### Option 1: Download Pre-built Packages (Recommended)
Visit our [Releases page](https://github.com/rlmattax/claude-desktop-debian/releases) and download:
- `claude-desktop_VERSION_amd64.deb` for Debian/Ubuntu systems
- `claude-desktop-VERSION-amd64.AppImage` for universal Linux compatibility

### Option 2: Build Yourself
```bash
git clone https://github.com/rlmattax/claude-desktop-debian.git
cd claude-desktop-debian
./build.sh  # Creates .deb package by default
```

## 🚀 Features

**Arch Linux users:** For the PKGBUILD and Arch-specific instructions: [https://github.com/aaddrick/claude-desktop-arch](https://github.com/aaddrick/claude-desktop-arch)

**✅ Full Feature Support:**
- 🔧 **MCP (Model Context Protocol)** - Configuration at `~/.config/Claude/claude_desktop_config.json`
- ⌨️ **Global Hotkey** - Ctrl+Alt+Space popup window
- 🔔 **System Tray** - Minimize to tray functionality
- 🖥️ **Native Integration** - Proper Linux desktop integration

![Claude Desktop on Linux](https://github.com/user-attachments/assets/93080028-6f71-48bd-8e59-5149d148cd45)

**Ctrl+Alt+Space Popup:**
![Global Hotkey](https://github.com/user-attachments/assets/1deb4604-4c06-4e4b-b63f-7f6ef9ef28c1)

**System Tray Integration (KDE):**
![System Tray](https://github.com/user-attachments/assets/ba209824-8afb-437c-a944-b53fd9ecd559)

## 🛠️ Building & Installation

For Debian-based distributions (Debian, Ubuntu, Linux Mint, Pop!_OS, etc.), you can build Claude Desktop using our automated build script. The script supports multiple output formats and architectures.

```bash
# Clone this repository
git clone https://github.com/rlmattax/claude-desktop-debian.git
cd claude-desktop-debian

# Build the package (Defaults to .deb and cleans build files)
./build.sh

# Example: Build an AppImage and keep intermediate files
./build.sh --build appimage --clean no

# Example: Build a .deb (explicitly) and clean intermediate files (default)
./build.sh --build deb --clean yes
```

The script will automatically:
 - Check for and install required dependencies
 - Download and extract resources from the Windows version
 - Create a proper Debian package or AppImage
 - Perform the build steps based on selected flags

## 📋 After Building

### If you chose Debian Package (.deb):

The script will output the path to the generated `.deb` file (e.g., `claude-desktop_0.9.3_amd64.deb`). Install it using `dpkg`:

```bash
# Replace VERSION and ARCHITECTURE with the actual values from the filename
sudo dpkg -i ./claude-desktop_VERSION_ARCHITECTURE.deb 

# If you encounter dependency issues, run:
sudo apt --fix-broken install 
```

### If you chose AppImage (.AppImage):

The script will output the path to the generated `.AppImage` file (e.g., `claude-desktop-0.9.3-amd64.AppImage`) and a corresponding `.desktop` file (`claude-desktop-appimage.desktop`).

**AppImage login will not work unless you setup the .desktop file correctly or use a tool like AppImageLauncher to manage it for you.**

1.  **Make the AppImage executable:**
    ```bash
    # Replace FILENAME with the actual AppImage filename
    chmod +x ./FILENAME.AppImage 
    ```
2.  **Run the AppImage:**
    ```bash
    ./FILENAME.AppImage
    ```
3.  **(Optional) Integrate with your system:**
    -   Tools like [AppImageLauncher](https://github.com/TheAssassin/AppImageLauncher) can automatically integrate AppImages (moving them to a central location and adding them to your application menu) using the bundled `.desktop` file.
    -   Alternatively, you can manually move the `.AppImage` file to a preferred location (e.g., `~/Applications` or `/opt`) and copy the generated `claude-desktop-appimage.desktop` file to `~/.local/share/applications/` (you might need to edit the `Exec=` line in the `.desktop` file to point to the new location of the AppImage).

#### --no-sandbox

The AppImage script runs with electron's --no-sandbox flag. AppImage's don't have their own sandbox. chome-sandbox, which is used by electron, needs to escalate root privileges briefly in order to setup the sandbox. When you pack an AppImage, chrome-sandbox loses any assigned ownership and executes with user permissions. There's also an issue with [unprivileged namespaces](https://www.reddit.com/r/debian/comments/hkyeft/comment/fww5xb1) being set differently on different distributions.

**Alternatives to --no-sandbox**
 - Run claude-desktop as root
   - Doesn't feel warm and fuzzy.
 - Install chrome-sandbox outside of the AppImage(or leverage an existing install), set it with the right permissions, and reference it.
   - Counter-intuitive to the "batteries included" mindset of AppImages
 - Run it with --no-sandbox, but then wrap the whole thing inside another sandbox like bubblewrap
   - Not "batteries included", and configuring in such a way that it runs everywhere is beyond my immediate capabilities.

I'd love a better suggestion. Feel free to submit a PR or start a discussion if I missed something obvious.

## 🗑️ Uninstallation

### Debian Package (.deb)

If you installed the `.deb` package, you can uninstall it using `dpkg`:

```bash
sudo dpkg -r claude-desktop
```

If you also want to remove configuration files (including MCP settings), use `purge`:

```bash
sudo dpkg -P claude-desktop
```

### AppImage (.AppImage)

If you used the AppImage:
1.  Delete the `.AppImage` file.
2.  Delete the associated `.desktop` file (e.g., `claude-desktop-appimage.desktop` from where you placed it, like `~/.local/share/applications/`).
3.  If you used AppImageLauncher, it might offer an option to un-integrate the AppImage.

### Configuration Files (Both Formats)

To remove user-specific configuration files (including MCP settings), regardless of installation method:

```bash
rm -rf ~/.config/Claude
```

## 🔧 Troubleshooting

Aside from the install logs, runtime logs can be found in (`$HOME/claude-desktop-launcher.log`).

If your window isn't scaling correctly the first time or two you open the application, right click on the claude-desktop panel (taskbar) icon and quit. When doing a safe shutdown like this, the application saves some states to the .config/claude folder which will resolve the issue moving forward. Force quitting the application will not trigger the updates. 

## ⚙️ How it works (Debian/Ubuntu Build)

Claude Desktop is an Electron application packaged as a Windows executable. Our build script performs several key operations to make it work on Linux:

1.  Downloads and extracts the Windows installer
2.  Unpacks the `app.asar` archive containing the application code
3.  Replaces the Windows-specific native module with a Linux-compatible stub implementation
4.  Repackages everything into the user's chosen format:
    *   **Debian Package (.deb):** Creates a standard Debian package installable via `dpkg`.
    *   **AppImage (.AppImage):** Creates a self-contained executable using `appimagetool`.

The process works because Claude Desktop is largely cross-platform, with only one platform-specific component that needs replacement.

### Build Process Details

The main build script (`build.sh`) orchestrates the process:

1. Checks for a Debian-based system and required dependencies
2. Parses command-line flags (`--build`, `--clean`) to determine output format and cleanup behavior.
3. Downloads the official Windows installer
4. Extracts the application resources
5. Processes icons for Linux desktop integration
6. Unpacks and modifies the app.asar:
   - Replaces the native mapping module with our Linux version
   - Preserves all other functionality
7. Calls the appropriate packaging script (`scripts/build-deb-package.sh` or `scripts/build-appimage.sh`) to create the final output:
   *   **For .deb:** Creates a package with desktop entry, icons, dependencies, and post-install steps.
   *   **For .AppImage:** Creates an AppDir, bundles Electron, generates an `AppRun` script and `.desktop` file, and uses `appimagetool` to create the final `.AppImage`.

### Automated Version Detection

The repository includes an automated system (`scripts/check-upstream-version.py`) that:

- Monitors both amd64 and arm64 Claude Desktop installers daily
- Downloads only small chunks (2MB) to efficiently extract version information
- Uses multiple regex patterns to detect version numbers in binary data
- Tracks file metadata (ETag, size, last-modified) for reliable change detection
- Automatically triggers builds when new versions are detected
- Creates GitHub issues and releases to notify users of updates

See [`AUTOMATION.md`](AUTOMATION.md) for detailed information about the automation system.

## 📖 Attribution & History

This project was originally inspired by [k3d3's claude-desktop-linux-flake](https://github.com/k3d3/claude-desktop-linux-flake) and their [Reddit post](https://www.reddit.com/r/ClaudeAI/comments/1hgsmpq/i_successfully_ran_claude_desktop_natively_on/) about running Claude Desktop natively on Linux. The sophisticated build system was later developed by [aaddrick](https://github.com/aaddrick).

**Current Maintainer**: Bob Mattax ([rlmattax](https://github.com/rlmattax))

**Original Authors**:
- [k3d3](https://github.com/k3d3) - Original NixOS implementation and proof of concept
- [aaddrick](https://github.com/aaddrick) - Debian/Ubuntu build system and multi-format packaging

**Related Projects**:
- **NixOS Users**: [k3d3's claude-desktop-linux-flake](https://github.com/k3d3/claude-desktop-linux-flake) 
- **Alternative Implementation**: [Emsi's claude-desktop](https://github.com/emsi/claude-desktop) (includes additional refinements and the title bar fix)

## 📄 License

The build scripts in this repository are dual-licensed under the terms of the MIT license and the Apache License (Version 2.0).

See [LICENSE-MIT](LICENSE-MIT) and [LICENSE-APACHE](LICENSE-APACHE) for details.

The Claude Desktop application, not included in this repository, is covered by [Anthropic's Consumer Terms](https://www.anthropic.com/legal/consumer-terms).

## 🤝 Contribution

Unless you explicitly state otherwise, any contribution intentionally submitted for inclusion in the work by you, as defined in the Apache-2.0 license, shall be dual licensed as above, without any additional terms or conditions.

**Contributing Guidelines:**
- Bug reports and feature requests are welcome via GitHub Issues
- Pull requests should maintain the automated build system compatibility
- Test changes with both .deb and AppImage formats when possible
- Check that automation scripts continue to work after modifications
