#!/usr/bin/env python3
"""
Claude Desktop Version Checker

This script checks for new versions of Claude Desktop by monitoring both
amd64 and arm64 installers. It integrates with the existing build system
by checking the actual installer files rather than maintaining a separate
VERSION file.
"""

import os
import sys
import json
import requests
import re
from datetime import datetime
from typing import Optional, Dict, Tuple

# URLs for both architectures
CLAUDE_URLS = {
    "amd64": "https://storage.googleapis.com/osprey-downloads-c02f6a0d-347c-492b-a752-3e0651722e97/nest-win-x64/Claude-Setup-x64.exe",
    "arm64": "https://storage.googleapis.com/osprey-downloads-c02f6a0d-347c-492b-a752-3e0651722e97/nest-win-arm64/Claude-Setup-arm64.exe"
}

METADATA_FILE = ".claude-version-metadata"

def get_file_metadata(url: str, arch: str) -> Tuple[str, str, Optional[datetime], Optional[str]]:
    """Get metadata about a Claude installer file from GCS."""
    print(f"Checking {arch} installer...")
    response = requests.head(url, timeout=30)
    response.raise_for_status()
    
    etag = response.headers.get('ETag', '').strip('"')
    last_modified = response.headers.get('Last-Modified')
    content_length = response.headers.get('Content-Length')
    
    # Parse the Last-Modified date
    last_modified_date = None
    if last_modified:
        try:
            last_modified_date = datetime.strptime(last_modified, '%a, %d %b %Y %H:%M:%S %Z')
        except ValueError as e:
            print(f"Warning: Could not parse last-modified date: {e}")
    
    # Try to extract version from the installer
    version = extract_version_from_installer(url)
    
    return etag, content_length, last_modified_date, version

def extract_version_from_installer(url: str) -> Optional[str]:
    """
    Download a small chunk of the installer and try to extract version information.
    Uses the same approach as the main build script but optimized for checking.
    """
    try:
        # Download first 2MB which should contain version info
        headers = {'Range': 'bytes=0-2097152'}
        response = requests.get(url, headers=headers, stream=True, timeout=60)
        response.raise_for_status()
        
        chunk = response.content
        
        # Look for version patterns in the binary data
        version_patterns = [
            # Standard version patterns
            rb'(\d+\.\d+\.\d+\.\d+)',
            rb'(\d+\.\d+\.\d+)',
            # Specific Windows version resource patterns  
            rb'ProductVersion["\x00]*(\d+\.\d+\.\d+)',
            rb'FileVersion["\x00]*(\d+\.\d+\.\d+)',
            rb'Version["\x00]*(\d+\.\d+\.\d+)',
            # NSIS installer patterns
            rb'AnthropicClaude[^\d]*(\d+\.\d+\.\d+)',
            rb'Claude[^\d]*(\d+\.\d+\.\d+)',
            # General patterns
            rb'v(\d+\.\d+\.\d+)',
            rb'V(\d+\.\d+\.\d+)',
            # Unicode patterns
            rb'(\d+\.\d+\.\d+)[\x00\x20-\x7F]{0,50}[Cc]laude',
            rb'[Cc]laude[\x00\x20-\x7F]{0,50}(\d+\.\d+\.\d+)',
        ]
        
        found_versions = []
        for pattern in version_patterns:
            matches = re.findall(pattern, chunk)
            for match in matches:
                version = match.decode('utf-8') if isinstance(match, bytes) else match
                if version not in found_versions:
                    found_versions.append(version)
        
        # Filter out invalid versions
        valid_versions = []
        for version in found_versions:
            parts = version.split('.')
            if len(parts) >= 3:
                try:
                    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
                    # Reasonable bounds for Claude versions
                    if major <= 10 and minor <= 100 and patch <= 100:
                        valid_versions.append(version)
                except ValueError:
                    continue
        
        if valid_versions:
            # Return the most reasonable version (prefer 3-part versions)
            valid_versions.sort(key=lambda v: (len(v.split('.')), v))
            return valid_versions[0]
        
        return None
    except Exception as e:
        print(f"Warning: Failed to extract version from installer: {e}")
        return None

def load_previous_metadata() -> Optional[Dict]:
    """Load the previously saved metadata."""
    if os.path.exists(METADATA_FILE):
        try:
            with open(METADATA_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load previous metadata: {e}")
    return None

def save_current_metadata(metadata: Dict):
    """Save the current metadata to file."""
    try:
        with open(METADATA_FILE, 'w') as f:
            json.dump(metadata, f, indent=2, default=str)
    except IOError as e:
        print(f"Error: Could not save metadata: {e}")

def compare_versions(v1: str, v2: str) -> int:
    """Compare two version strings. Returns -1 if v1 < v2, 0 if equal, 1 if v1 > v2."""
    def normalize(v):
        return [int(x) for x in v.split('.')]
    
    try:
        v1_parts = normalize(v1)
        v2_parts = normalize(v2)
        
        for i in range(max(len(v1_parts), len(v2_parts))):
            v1_part = v1_parts[i] if i < len(v1_parts) else 0
            v2_part = v2_parts[i] if i < len(v2_parts) else 0
            if v1_part < v2_part:
                return -1
            elif v1_part > v2_part:
                return 1
        return 0
    except (ValueError, TypeError):
        # Fallback to string comparison if parsing fails
        if v1 < v2:
            return -1
        elif v1 > v2:
            return 1
        return 0

def main():
    """Main function to check for upstream changes."""
    try:
        print("🔍 Checking for Claude Desktop updates...")
        
        # Get current metadata for both architectures
        current_metadata = {
            'check_time': datetime.now().isoformat(),
            'architectures': {}
        }
        
        for arch, url in CLAUDE_URLS.items():
            etag, size, last_modified, version = get_file_metadata(url, arch)
            current_metadata['architectures'][arch] = {
                'etag': etag,
                'size': size,
                'last_modified': last_modified.isoformat() if last_modified else None,
                'url': url,
                'version': version
            }
        
        # Load previous metadata
        previous_metadata = load_previous_metadata()
        
        # Check for changes
        changes = []
        
        if previous_metadata and 'architectures' in previous_metadata:
            for arch in CLAUDE_URLS.keys():
                current = current_metadata['architectures'][arch]
                previous = previous_metadata['architectures'].get(arch, {})
                
                # Check file metadata changes
                if previous.get('etag') != current['etag']:
                    changes.append(f'{arch}: ETag changed')
                if previous.get('size') != current['size']:
                    changes.append(f'{arch}: File size changed')
                if previous.get('last_modified') != current['last_modified']:
                    changes.append(f'{arch}: Last modified date changed')
                
                # Check version changes
                current_version = current.get('version')
                previous_version = previous.get('version')
                
                if current_version and previous_version:
                    if compare_versions(previous_version, current_version) < 0:
                        changes.append(f'{arch}: Version updated from {previous_version} to {current_version}')
                elif current_version and not previous_version:
                    changes.append(f'{arch}: Version detected: {current_version}')
        else:
            # First run - treat as changes to initialize the system
            print("🆕 First run detected - initializing version tracking")
            for arch, data in current_metadata['architectures'].items():
                version = data.get('version', 'unknown')
                changes.append(f'{arch}: Initial version detected: {version}')
        
        # Report results
        if changes:
            print("✨ Changes detected:")
            for change in changes:
                print(f"  • {change}")
            
            # Show version summary
            print("\n📋 Current versions:")
            for arch, data in current_metadata['architectures'].items():
                version = data.get('version', 'unknown')
                print(f"  • {arch}: {version}")
            
            save_current_metadata(current_metadata)
            sys.exit(1)  # Exit with status 1 to indicate changes
        else:
            print("✅ No changes detected")
            
            # Show current versions
            versions = []
            for arch, data in current_metadata['architectures'].items():
                version = data.get('version', 'unknown')
                versions.append(f"{arch}: {version}")
            print(f"📋 Current versions: {', '.join(versions)}")
            
            save_current_metadata(current_metadata)
            sys.exit(0)
            
    except Exception as e:
        print(f"❌ Error checking for updates: {e}")
        sys.exit(2)

if __name__ == '__main__':
    main() 