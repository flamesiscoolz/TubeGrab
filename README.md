<p align="center">
  <img src="assets/tubegrab-wordmark.svg" width="360" alt="TubeGrab">
</p>

<p align="center">MP3 and MP4 downloads beside YouTube's Like button.</p>

TubeGrab is a small Edge extension with a local Python helper. The extension adds a native-looking `MP3 | MP4` control to YouTube. The helper handles downloads in the background and keeps a Quit option in the Windows system tray.

## Install

You need Windows, Microsoft Edge, and Python 3.10 or newer.

1. Download or clone this repository.
2. Run:

   ```powershell
   powershell -ExecutionPolicy Bypass -File .\install.ps1
   ```

3. Open `edge://extensions`.
4. Turn on **Developer mode**.
5. Choose **Load unpacked** and select the `extension` folder.

The installer handles the Python packages, FFmpeg, local connection token, startup shortcut, and background helper.

## Use

Open a YouTube video and use the buttons beside Like/Dislike:

- **MP3** downloads the best audio source and converts it to 320 kbps MP3.
- **MP4** downloads the best available video and audio.

Files are saved to your Windows Downloads folder. They will not appear in Edge's download panel because the local helper writes them directly to disk.

TubeGrab runs under **Show hidden icons** in the Windows taskbar. Right-click its icon and choose **Quit TubeGrab** to stop it.

## Update

Pull or replace the project files, run `install.ps1` again, then click **Reload** for TubeGrab on `edge://extensions`.

## Remove

Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\uninstall.ps1
```

Then remove TubeGrab from `edge://extensions`.

Only download videos you own or have permission to save.
