# Security Policy

## Data handling

MBP's Video Downloader is a fully local tool. It:

- stores **no credentials** — no API keys, tokens, or passwords are used or saved anywhere
- touches **only local files** — it writes the downloaded video to the folder you choose and reads nothing else
- never sends your URL, your file paths, or any other data to any server
- downloads are performed directly by [yt-dlp](https://github.com/yt-dlp/yt-dlp), the same engine used by many public download tools

Nothing in this application phones home or persists anything beyond the files it downloads for you.

## Reporting a vulnerability

This is a personal project. To report a security issue, open a private discussion or contact the maintainer directly. Do **not** open a public issue that includes URLs, file paths, or any personal data.

## Supported versions

Only the latest release is supported.
