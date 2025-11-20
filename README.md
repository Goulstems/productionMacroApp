# AIROBO - AI & Robotics Academy App Publisher

A comprehensive CLI tool for building, publishing, and deploying mobile applications for the AI & Robotics Academy. Automates the entire workflow from source code to Google Play Store.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Building & Publishing](#building--publishing)
- [Development](#development)
- [Troubleshooting](#troubleshooting)

---

## Features

✨ **Automated Android App Building**
- Builds signed Android App Bundles (.aab)
- Handles Capacitor app preparation and syncing
- Automatic icon and splash screen processing
- PNG to SVG conversion for optimal quality

🚀 **Google Play Auto-Publishing**
- Direct upload to Google Play Console via API
- Support for all release tracks (internal, alpha, beta, production)
- Automatic authentication with service accounts

🎨 **Asset Management**
- Icon and splash screen processing
- Multi-resolution asset generation
- Vector conversion for scalability

📦 **Package Management**
- Automated version incrementing
- PyPI publishing integration
- One-command deployment

---

## Installation

### Prerequisites

- Python 3.7 or higher
- Node.js and npm (for Capacitor)
- Java JDK 21 (for Android builds)
- Android SDK
- Git

### Install from PyPI

```bash
pip install -U airobo
```

### Install from Source (Development)

```bash
git clone https://github.com/Goulstems/productionMacroApp.git
cd productionMacroApp
pip install -e .
```

---

## Configuration

### 1. Required Directory: `airoboConfigs`

The `airoboConfigs` directory contains all necessary configuration files and assets for your app builds.

**📍 Location:** `C:\airoboConfigs` (Windows) or `~/airoboConfigs` (Mac/Linux)

**📁 Required Files:**

```
C:\airoboConfigs\
├── appIcon.png          # App launcher icon (512x512 recommended)
├── splash.png           # Splash screen image (2732x2732 recommended)
├── airoboEnv           # Environment variables file
└── airoboEnv.env       # Alternative env file name
```

#### Creating the Config Directory

**Windows:**
```powershell
mkdir C:\airoboConfigs
```

**Mac/Linux:**
```bash
mkdir ~/airoboConfigs
```

### 2. Environment Configuration

Create `C:\airoboConfigs\airoboEnv` with the following content:

```bash
# Git Repository Configuration
gitURL=https://github.com/YourOrg/your-app-repo/tree/main

# Google Play Publishing (Optional - for auto-publish)
GOOGLE_PLAY_SERVICE_ACCOUNT_JSON=C:\path\to\service-account.json
GOOGLE_PLAY_PACKAGE_NAME=com.yourcompany.yourapp
GOOGLE_PLAY_TRACK=internal

# Android Signing Configuration
AIROBO_SIGN_KEYSTORE=C:\path\to\your-release.keystore
AIROBO_SIGN_STORE_PASSWORD=your_store_password
AIROBO_SIGN_KEY_ALIAS=your_key_alias
AIROBO_SIGN_KEY_PASSWORD=your_key_password

# Enable Auto-Publishing
AIROBO_AUTO_PUBLISH=true
```

### 3. App Assets

#### App Icon (`appIcon.png`)
- **Recommended Size:** 512x512 pixels or higher
- **Format:** PNG with transparency
- **Purpose:** Used to generate all launcher icons for Android

#### Splash Screen (`splash.png`)
- **Recommended Size:** 2732x2732 pixels
- **Format:** PNG
- **Purpose:** Displayed when app launches

---

## Usage

### Basic Commands

```bash
# Build and publish Android app
airobo publish android

# Build Android app only (no upload)
# Set AIROBO_AUTO_PUBLISH=false in config
airobo publish android
```

### What Happens During a Build

1. **Source Preparation**
   - Clones/pulls the latest code from your Git repository
   - Prepares Capacitor app structure
   - Syncs with Android platform

2. **Asset Processing**
   - Converts PNG icons to SVG for better quality
   - Generates multi-resolution launcher icons
   - Processes splash screens for all densities

3. **Building**
   - Cleans previous builds
   - Configures signing if credentials provided
   - Builds release AAB using Gradle
   - Creates versioned output file

4. **Publishing** (if enabled)
   - Authenticates with Google Play API
   - Uploads AAB to specified track
   - Commits the release

### Build Output

Built files are saved to:
```
C:\Users\<YourUser>\AppData\Local\airobo\app-cache\air-app-builds\android\
```

Example output file: `app-release-v1.0.0.aab`

---

## Building & Publishing

### Step-by-Step: Complete Workflow

#### 1. Initial Setup (One-Time)

```bash
# Install airobo
pip install -U airobo

# Create config directory
mkdir C:\airoboConfigs

# Add your app icon and splash screen
# Copy appIcon.png and splash.png to C:\airoboConfigs\

# Create environment configuration
# Create C:\airoboConfigs\airoboEnv with your settings
```

#### 2. Android Signing Setup (One-Time)

Generate a release keystore:
```bash
keytool -genkey -v -keystore my-release-key.keystore -alias my-key-alias -keyalg RSA -keysize 2048 -validity 10000
```

Add keystore details to `C:\airoboConfigs\airoboEnv`:
```bash
AIROBO_SIGN_KEYSTORE=C:\path\to\my-release-key.keystore
AIROBO_SIGN_STORE_PASSWORD=your_password
AIROBO_SIGN_KEY_ALIAS=my-key-alias
AIROBO_SIGN_KEY_PASSWORD=your_password
```

#### 3. Google Play Setup (Optional - For Auto-Publishing)

See [GOOGLE_PLAY_SETUP.md](./GOOGLE_PLAY_SETUP.md) for detailed instructions.

Quick setup:
1. Create service account in Google Cloud Console
2. Enable Play Developer API
3. Download JSON credentials
4. Grant permissions in Play Console
5. Add credentials to config file

#### 4. Build and Publish

```bash
# Navigate to any directory (config is auto-detected)
cd C:\Users\Josh\Desktop

# Run the publisher
airobo publish android
```

#### 5. Monitor the Build

Watch the console output for:
- ✅ Source pulled from repository
- ✅ Capacitor sync completed
- ✅ Icons and splash screens processed
- ✅ Gradle build successful
- ✅ AAB file created
- ✅ Uploaded to Google Play (if enabled)

---

## Development

### Project Structure

```
productionMacroApp/
├── airobo/
│   ├── __init__.py
│   ├── api.py              # PyPI API interactions
│   ├── cli.py              # Main CLI entry point
│   ├── modules/
│   │   ├── android/
│   │   │   └── buildAndroid.py    # Android build logic
│   │   ├── capacitorMacro.py      # Capacitor helpers
│   │   ├── getLatestAppSource.py  # Git operations
│   │   ├── imageConverter.py      # PNG to SVG conversion
│   │   └── utils/
│   │       └── env.py             # Environment config
├── pyproject.toml          # Package configuration
├── publish.py              # PyPI publishing script
├── .env                    # Local secrets (NOT committed)
├── .gitignore
└── README.md
```

### Installing Development Version

```bash
# Clone the repository
git clone https://github.com/Goulstems/productionMacroApp.git
cd productionMacroApp

# Install in editable mode
pip install -e .

# Test CLI
airobo --help
```

### Publishing Updates to PyPI

```bash
# Update version and publish
python publish.py
```

The script automatically:
1. Increments the version number
2. Cleans old builds
3. Builds the package
4. Uploads to PyPI
5. Updates local installation

### Adding Dependencies

Edit `pyproject.toml`:

```toml
dependencies = [
    "google-api-python-client>=2.0.0",
    "google-auth-httplib2>=0.1.0",
    "google-auth-oauthlib>=0.5.0",
    "Pillow>=9.0.0",
]
```

Then reinstall:
```bash
pip install -e .
```

---

## Troubleshooting

### Common Issues

#### "Config directory not found"
- Ensure `C:\airoboConfigs` exists
- Check that `airoboEnv` or `airoboEnv.env` file is present

#### "Git pull failed"
- Verify `gitURL` in config is correct
- Check you have access to the repository
- Ensure Git is installed and configured

#### "Gradle build failed"
- Verify JDK 21 is installed
- Check Android SDK is properly configured
- Review console output for specific errors

#### "No appIcon.png found"
- Place a PNG icon in `C:\airoboConfigs\appIcon.png`
- Recommended size: 512x512 or larger

#### "Google Play upload failed (403)"
- Check service account JSON path is correct
- Verify API is enabled in Google Cloud
- Ensure service account has permissions in Play Console
- Wait 48 hours after granting permissions

#### "Module not found: googleapiclient"
- Install/reinstall airobo: `pip install -U airobo`
- Or manually: `pip install google-api-python-client`

### Getting Help

1. Check the console output for error details
2. Review [GOOGLE_PLAY_SETUP.md](./GOOGLE_PLAY_SETUP.md) for publishing issues
3. Verify all environment variables are set correctly
4. Ensure all prerequisites are installed

### Debug Mode

For more detailed output, you can:
1. Check build logs in the Android directory
2. Run Gradle commands manually for debugging
3. Use `--verbose` flag with twine for upload issues

---

## Requirements Summary

### System Requirements
- **OS:** Windows 10/11, macOS 10.15+, or Linux
- **Python:** 3.7 or higher
- **Node.js:** 16.x or higher
- **Java:** JDK 21
- **Memory:** 4GB RAM minimum (8GB recommended)
- **Disk Space:** 10GB free space

### Software Requirements
- Git
- Android SDK
- Gradle (installed via Android SDK)
- Python pip

### Configuration Requirements
- `C:\airoboConfigs` directory
- `airoboEnv` file with repository URL
- `appIcon.png` (512x512+)
- `splash.png` (2732x2732+)
- Android signing keystore (for release builds)
- Google Play service account (for auto-publishing)

---

## License

Copyright © 2025 AI & Robotics Academy

---

## Support

For issues, questions, or contributions:
- **Repository:** https://github.com/Goulstems/productionMacroApp
- **Author:** Joshua Morvant (joshua@aiarobo.com)

---

**Happy Publishing! 🚀**
