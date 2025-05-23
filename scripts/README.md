# Automation Scripts

This directory contains automation scripts for maintaining Claude Desktop Linux packages.

## check-upstream-version.py

Automated version checker that monitors Claude Desktop updates for both amd64 and arm64 architectures.

### Features

- **Multi-architecture Support**: Monitors both x64 and ARM64 installers
- **Smart Version Detection**: Extracts version numbers directly from installer files using multiple pattern matching strategies
- **Change Detection**: Tracks file metadata (ETag, size, last-modified) and version changes
- **Efficient Monitoring**: Only downloads 2MB chunks to extract version info
- **Robust Error Handling**: Graceful fallbacks and detailed error reporting

### Usage

```bash
# Check for updates manually
python3 scripts/check-upstream-version.py

# Exit codes:
# 0 = No changes detected
# 1 = Changes detected (triggers builds)
# 2 = Error occurred
```

### Metadata File

The script maintains a `.claude-version-metadata` file that tracks:

```json
{
  "check_time": "2024-01-15T12:00:00.000000",
  "architectures": {
    "amd64": {
      "etag": "abc123...",
      "size": "123456789",
      "last_modified": "2024-01-15T10:30:00+00:00",
      "url": "https://storage.googleapis.com/.../Claude-Setup-x64.exe",
      "version": "0.9.3"
    },
    "arm64": {
      "etag": "def456...",
      "size": "123456789", 
      "last_modified": "2024-01-15T10:30:00+00:00",
      "url": "https://storage.googleapis.com/.../Claude-Setup-arm64.exe",
      "version": "0.9.3"
    }
  }
}
```

### Integration

This script is designed to work with the existing sophisticated build system:

1. **GitHub Actions**: Triggered daily via `.github/workflows/check-for-updates.yml`
2. **Build Triggering**: Automatically starts `build.yml` workflow when changes detected
3. **Issue Creation**: Creates GitHub issues to announce new versions
4. **Metadata Tracking**: Commits updated metadata to repository

### Version Detection Strategy

The script uses multiple regex patterns to extract version numbers:

- Standard version patterns (`\d+\.\d+\.\d+`)
- Windows PE resource patterns (`ProductVersion`, `FileVersion`)
- NSIS installer patterns
- Unicode and binary format patterns
- Smart filtering to avoid false positives

This approach is more reliable than filename-based detection since it reads the actual version embedded in the installer files.

## Workflow Integration

The automation system integrates seamlessly with the inherited professional build system:

1. **Daily Checks**: Runs at 12:00 UTC to be a "good citizen"
2. **Change Detection**: Monitors both file changes and version updates
3. **Automatic Builds**: Triggers the existing multi-architecture build system
4. **Release Management**: Works with existing release automation
5. **Notification**: Creates issues and commits for transparency

This preserves all the sophisticated build capabilities (multi-arch, multi-format) while adding the automation that was missing. 