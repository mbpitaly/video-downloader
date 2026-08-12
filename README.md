<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->
[![Python][python-shield]](https://www.python.org/downloads/release/python-3119/)
[![Platform][platform-shield]](#)
[![License][license-shield]][license-url]
[![Version][version-shield]](#)

<br />
<div align="center">
  <h1 align="center">MBP's Video Downloader</h1>
  <p align="center">
    A simple yt-dlp GUI for downloading videos at the best available quality — a single-file tkinter tool.
    <br />
    <a href="#getting-started"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="#usage">View Usage</a>
    ·
    <a href="https://github.com/mbpitaly/video-downloader/issues/new?labels=bug&template=bug_report.md">Report Bug</a>
    ·
    <a href="https://github.com/mbpitaly/video-downloader/issues/new?labels=enhancement&template=feature_request.md">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#features">Features</a></li>
    <li><a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#building-from-source">Building From Source</a></li>
    <li><a href="#project-layout">Project Layout</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

MBP's Video Downloader is a single-file tkinter GUI that wraps [yt-dlp](https://github.com/yt-dlp/yt-dlp) behind a clean, minimal interface. Paste a link, pick where to save, and download — no command line required.

It was built by Matteo Barni (2026) to make downloading videos at the best available quality fast and effortless.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- FEATURES -->
## Features

- **Paste a URL** — the only thing you need to get started
- **Choose a download folder** — defaults to your Desktop
- **Best available quality** — `bestvideo+bestaudio/best` grabs the highest-quality streams
- **Live progress** — percentage with download speed and ETA
- **Cancel support** — abort an in-flight download cleanly
- **ffmpeg merge step** — clearly shown in the status bar while audio/video are merged
- **Auto-closes on success** — a brief "Done! Closing..." then the window exits
- **Error dialog on failure** — a message box reports what went wrong

### Built With

- [Python 3.11](https://www.python.org/) + [tkinter/ttk](https://docs.python.org/3/library/tkinter.html)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — the download engine
- [ffmpeg](https://ffmpeg.org/) — merging separate audio/video streams
- [PyInstaller](https://pyinstaller.org/) — standalone exe packaging

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

- **Windows 10/11** (tkinter comes with the official Python installer; the packaged exe needs nothing)
- **ffmpeg** on `PATH` when running from source — required to merge separate audio/video streams
- **Python 3.11** when running from source

### Installation

**Option A — installer (Windows)**

Download `MBPs_Video_Downloader_Setup.exe` from the [Releases](https://github.com/mbpitaly/video-downloader/releases) page and run it. The installer bundles **ffmpeg**, so best-quality downloads (video + audio merge) work out of the box.

**Option B — from source**

```sh
# 1. Clone
git clone https://github.com/mbpitaly/video-downloader.git
cd video-downloader

# 2. Install the only runtime dependency
python -m pip install yt-dlp

# 3. Run
python downloader.pyw
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE -->
## Usage

1. Launch `MBPs_Video_Downloader.exe` — the window opens centered.
2. Paste the **video URL** into the top field.
3. Choose a **download folder** (defaults to your Desktop) — or leave it as is.
4. Hit **Start Download**.
5. Watch the live progress bar (percentage, speed, ETA); the status bar shows the ffmpeg merge step when audio and video are combined.

The window auto-closes on success. Hit **Cancel** to abort an in-flight download.

> **Note**: when the URL yields separate video and audio streams, ffmpeg merges them — make sure it's available (bundled in the exe via yt-dlp; on PATH when running from source).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- BUILDING -->
## Building From Source

```sh
# Python 3.11
python -m pip install yt-dlp pyinstaller

# Build the standalone exe
python -m PyInstaller --onefile --windowed \
  --collect-all yt_dlp \
  --icon icon.ico \
  --name MBPs_Video_Downloader \
  downloader.pyw
```

Notes:

- **`--collect-all yt_dlp` is REQUIRED** — without it the exe is missing modules and crashes at runtime. yt-dlp ships lazily-imported plugin/data modules that PyInstaller's static analysis does not find on its own.
- `--windowed` suppresses the console window — the app is a pure GUI.
- The icon must always be passed via `--icon`, or PyInstaller silently embeds its generic icon.
- Worker threads never touch tkinter directly; all UI traffic goes through `root.after(0, ...)` on the main thread.

A CI workflow (`.github/workflows/build.yml`) builds the exe automatically on version tags.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LAYOUT -->
## Project Layout

```
video-downloader/
├── MBPs_Video_Downloader.exe   # prebuilt Windows binary (PyInstaller onefile)
├── downloader.pyw              # full source (single file)
├── icon.ico                    # app icon
├── .github/
│   ├── ISSUE_TEMPLATE/         # bug report + feature request templates
│   └── workflows/build.yml     # Windows exe build on tag
├── CHANGELOG.md
├── SECURITY.md
├── LICENSE                     # MIT
└── README.md
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open-source community such an amazing place. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please use the [issue templates](https://github.com/mbpitaly/video-downloader/issues/new/choose) for bugs and feature requests, and check [CHANGELOG.md](CHANGELOG.md) before opening PRs.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — the download engine
- [ffmpeg](https://ffmpeg.org/) — audio/video merging
- [PyInstaller](https://pyinstaller.org/) — standalone exe packaging
- [Best-README-Template](https://github.com/othneildrew/Best-README-Template) — README structure
- [Img Shields](https://shields.io/) — badges

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS -->
[python-shield]: https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white
[platform-shield]: https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white
[license-shield]: https://img.shields.io/badge/License-MIT-green?style=for-the-badge
[license-url]: LICENSE
[version-shield]: https://img.shields.io/badge/Release-v1.0.0-purple?style=for-the-badge
