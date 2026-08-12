# Changelog

All notable changes to MBP's Video Downloader are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-08-12

### Added
- Initial release.
- Single-file tkinter GUI wrapping yt-dlp.
- Paste-a-URL input with dynamic download-folder default (Desktop) and a Browse picker.
- Best-quality downloads via `bestvideo+bestaudio/best`.
- Live progress bar with percentage, downloaded size, download speed, and ETA.
- Cancel support that aborts an in-flight download cleanly.
- ffmpeg merge step reported in the status bar when audio/video streams are combined.
- Auto-close on success after a short "Done! Closing..." delay; error dialog on failure.
- Centered, non-resizable window with a clean light theme.
