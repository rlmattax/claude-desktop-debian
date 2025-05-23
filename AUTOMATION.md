# Claude Desktop Linux - Automation System

This document describes the automated update detection and build system added to maintain Claude Desktop packages for Linux.

## Overview

The automation system monitors upstream Claude Desktop releases and automatically triggers builds when new versions are detected, combining the sophisticated multi-architecture build system with intelligent version monitoring.

## Architecture

### Version Detection (`scripts/check-upstream-version.py`)

**Purpose**: Monitor Claude Desktop installers for both amd64 and arm64 architectures

**Key Features**:
- Downloads only 2MB chunks for efficient version extraction
- Uses multiple regex patterns to find version numbers in binary data
- Tracks file metadata (ETag, size, last-modified) for change detection
- Supports both 3-part (1.2.3) and 4-part (1.2.3.4) version formats
- Robust error handling with clear exit codes

**Exit Codes**:
- `0`: No changes detected
- `1`: Changes detected (triggers automation)
- `2`: Error occurred

### Daily Monitoring (`.github/workflows/check-for-updates.yml`)

**Schedule**: Daily at 12:00 UTC (good citizen timing)

**Process**:
1. **Check Updates**: Run version detection script
2. **Commit Metadata**: Save tracking information if changes found
3. **Trigger Builds**: Automatically start the sophisticated CI/CD pipeline
4. **Create Issues**: Notify about new versions with detailed information

### Integration with Existing Build System

The automation seamlessly integrates with the inherited professional build system:

- **Multi-Architecture**: Monitors both x64 and ARM64 installers
- **Multi-Format**: Triggers builds for both .deb and AppImage packages
- **Reusable Workflows**: Uses existing `ci.yml` workflow
- **Release Management**: Works with existing tag-based releases
- **Quality Control**: Includes shellcheck, codespell, and flag testing

## Metadata Tracking

The system maintains `.claude-version-metadata` with:

```json
{
  "check_time": "2024-01-15T12:00:00.000000",
  "architectures": {
    "amd64": {
      "etag": "file-hash...",
      "size": "123456789",
      "last_modified": "2024-01-15T10:30:00+00:00",
      "url": "https://storage.googleapis.com/.../Claude-Setup-x64.exe",
      "version": "0.9.3"
    },
    "arm64": {
      "etag": "file-hash...", 
      "size": "123456789",
      "last_modified": "2024-01-15T10:30:00+00:00",
      "url": "https://storage.googleapis.com/.../Claude-Setup-arm64.exe",
      "version": "0.9.3"
    }
  }
}
```

This file is committed to the repository to maintain a history of version changes.

## Manual Usage

```bash
# Check for updates manually
python3 scripts/check-upstream-version.py

# Test workflow locally
act workflow_dispatch -W .github/workflows/check-for-updates.yml

# Force a build manually
gh workflow run ci.yml
```

## Benefits

1. **Automated Maintenance**: No manual monitoring required
2. **Fast Response**: New versions detected within 24 hours
3. **Professional Quality**: Maintains all sophisticated build features
4. **Transparency**: Clear logging and issue creation
5. **Reliable Detection**: Multiple fallback patterns for version extraction
6. **Efficient**: Minimal bandwidth usage with chunk downloading

## Version Detection Strategy

The system uses a multi-layered approach:

1. **File Metadata**: ETag and modification time changes
2. **Binary Analysis**: Extract version from Windows PE resources
3. **Pattern Matching**: Multiple regex patterns for different formats
4. **Version Comparison**: Semantic version comparison
5. **Validation**: Filter out false positives with reasonable bounds

## What Happens When New Version Detected

1. **Detection**: Script identifies new version(s)
2. **Metadata**: Updated tracking file is committed
3. **Build Trigger**: `ci.yml` workflow started automatically
4. **Package Creation**: Multi-arch .deb and AppImage packages built
5. **Quality Assurance**: All tests and checks run
6. **Notification**: GitHub issue created with details
7. **Availability**: Packages available in Actions artifacts

For tagged releases, packages are automatically attached to GitHub releases.

## Contributing

The automation system is designed to be maintainable and extensible:

- **Clear Documentation**: Well-commented code and comprehensive README
- **Modular Design**: Separate concerns for detection vs. building
- **Error Handling**: Graceful failures with informative messages
- **Testing Support**: Can be run manually and tested locally

## Future Enhancements

Potential improvements:
- Slack/Discord notifications
- Version comparison in issues
- Automatic release notes generation
- Beta/RC version support
- Custom notification channels

---

*This automation system was built to combine the best of both worlds: sophisticated professional build capabilities with intelligent automatic version monitoring.* 