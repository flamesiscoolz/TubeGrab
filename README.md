<p align="center">
  <img src="assets/tubegrab-wordmark.svg" width="360" alt="TubeGrab">
</p>

<p align="center">MP3 and MP4 downloads beside YouTube's Like button.</p>

TubeGrab is a browser extension with a local Python helper. It adds a native-looking `MP3 | MP4` control to YouTube. The helper handles downloads in the background and keeps a Quit option in the Windows system tray.

## Install

You need Windows and Python 3.10 or newer. The extension supports current versions of:

- Chrome
- Edge
- Brave
- Opera
- Vivaldi
- Firefox 121 or newer

1. Download or clone this repository.
2. Run:

   ```powershell
   powershell -ExecutionPolicy Bypass -File .\install.ps1
   ```

3. Load the extension using the instructions below.

The installer handles the Python packages, FFmpeg, local connection token, startup shortcut, and background helper.

## Load the extension

For Chromium browsers, open the matching extensions page, enable **Developer mode**, choose **Load unpacked**, and select the `extension` folder:

| Browser | Extensions page |
| --- | --- |
| Chrome | `chrome://extensions` |
| Edge | `edge://extensions` |
| Brave | `brave://extensions` |
| Opera | `opera://extensions` |
| Vivaldi | `vivaldi://extensions` |

For Firefox, open `about:debugging#/runtime/this-firefox`, choose **Load Temporary Add-on**, and select `extension/manifest.json`. A temporary Firefox installation must be loaded again after restarting Firefox. Publishing a signed Firefox package is the permanent-install route.

## Use

Open a YouTube video and use the buttons beside Like/Dislike. The first time TubeGrab appears, a short curved arrow points out the new controls.

- **MP3** downloads the best audio source and converts it to 320 kbps MP3.
- **MP4** downloads the best available video and audio.

Files are saved to your Windows Downloads folder. They will not appear in Edge's download panel because the local helper writes them directly to disk.

TubeGrab runs under **Show hidden icons** in the Windows taskbar. Right-click its icon and choose **Quit TubeGrab** to stop it.

## Update

Pull or replace the project files, run `install.ps1` again, then reload TubeGrab from your browser's extensions page.

## Remove

Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\uninstall.ps1
```

Then remove TubeGrab from your browser's extensions page.

Only download videos you own or have permission to save.
