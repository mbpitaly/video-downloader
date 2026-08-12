import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import yt_dlp
import time

class VideoDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MBP's Video Downloader")
        
        self.window_width = 500
        self.window_height = 280
        self.center_window()
        
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.is_downloading = False
        
        self.setup_style()
        self.setup_ui()

    def center_window(self):
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width / 2) - (self.window_width / 2))
        y = int((screen_height / 2) - (self.window_height / 2))
        self.root.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")

    def setup_style(self):
        style = ttk.Style()
        style.theme_use('clam')
        self.bg_color = "#f0f0f0"
        self.root.configure(bg=self.bg_color)

        style.configure("TLabel", background=self.bg_color, font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 10, "bold"), background=self.bg_color)
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=5)
        style.configure("TEntry", fieldbackground="white", font=("Segoe UI", 11))
        style.configure("Horizontal.TProgressbar", thickness=15, background="#0078D7")

    def setup_ui(self):
        self.main_frame = tk.Frame(self.root, bg=self.bg_color, padx=25, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # URL Input
        ttk.Label(self.main_frame, text="Video URL:", style="Header.TLabel").pack(anchor="w")
        self.url_entry = ttk.Entry(self.main_frame)
        self.url_entry.pack(fill=tk.X, pady=(2, 15))

        # Output Folder
        ttk.Label(self.main_frame, text="Download Location:", style="Header.TLabel").pack(anchor="w")
        out_row = tk.Frame(self.main_frame, bg=self.bg_color)
        out_row.pack(fill=tk.X, pady=(2, 15))
        
        # Defaulting to the user's Desktop dynamically
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        self.out_var = tk.StringVar(value=desktop_path)
        self.out_entry = ttk.Entry(out_row, textvariable=self.out_var, font=("Segoe UI", 10))
        self.out_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.btn_out = ttk.Button(out_row, text="Browse", command=self.browse_output, width=8)
        self.btn_out.pack(side=tk.RIGHT)

        # Action Buttons
        action_row = tk.Frame(self.main_frame, bg=self.bg_color)
        action_row.pack(fill=tk.X, pady=(5, 15))

        self.btn_start = ttk.Button(action_row, text="Start Download", command=self.start_download)
        self.btn_start.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        self.btn_cancel = ttk.Button(action_row, text="Cancel", command=self.cancel_download, state=tk.DISABLED)
        self.btn_cancel.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))

        # Progress
        self.progress_bar = ttk.Progressbar(self.main_frame, orient="horizontal", mode="determinate", style="Horizontal.TProgressbar")
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))

        self.stats_label = ttk.Label(self.main_frame, text="Ready.", foreground="#333333", anchor="center", font=("Segoe UI", 10, "bold"))
        self.stats_label.pack(fill=tk.X)

    def browse_output(self):
        folder = filedialog.askdirectory(title="Select Download Directory")
        if folder:
            self.out_var.set(os.path.normpath(folder))

    def cancel_download(self):
        if not self.is_downloading: return
        self.is_downloading = False
        self.stats_label.config(text="Aborting download... Please wait.")
        self.btn_cancel.config(state=tk.DISABLED)

    def progress_hook(self, d):
        if not self.is_downloading:
            raise Exception("User Cancelled")

        if d['status'] == 'downloading':
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            
            if total > 0:
                percent = (downloaded / total) * 100
                mb_downloaded = downloaded / (1024 * 1024)
                mb_total = total / (1024 * 1024)
                
                speed = d.get('speed', 0)
                if speed is not None and speed > 0:
                    rate_str = f"{speed / (1024 * 1024):.1f} MB/s"
                else:
                    rate_str = "0.0 MB/s"
                
                eta = d.get('eta', 0)
                if eta is not None:
                    mins, secs = divmod(int(eta), 60)
                    eta_str = f"{mins:02d}:{secs:02d}"
                else:
                    eta_str = "Calculating..."

                status_text = f"{percent:.1f}% | {mb_downloaded:.1f} / {mb_total:.1f} MB | {rate_str} | ETA: {eta_str}"
                
                self.root.after(0, self.update_gui_progress, percent, status_text)
                
        elif d['status'] == 'finished':
            self.root.after(0, lambda: self.stats_label.config(text="100.0% | Merging Audio/Video with FFmpeg..."))

    def update_gui_progress(self, percent, text):
        self.progress_bar['value'] = percent
        self.stats_label.config(text=text)

    def start_download(self):
        url = self.url_entry.get().strip()
        out_dir = self.out_var.get().strip()

        if not url:
            messagebox.showerror("Error", "Please enter a video URL.")
            return

        try:
            os.makedirs(out_dir, exist_ok=True)
        except Exception:
            messagebox.showerror("Error", "Cannot access or create the output directory.")
            return

        self.is_downloading = True
        self.btn_start.config(state=tk.DISABLED)
        self.url_entry.config(state=tk.DISABLED)
        self.btn_out.config(state=tk.DISABLED)
        self.out_entry.config(state=tk.DISABLED)
        self.btn_cancel.config(state=tk.NORMAL)

        self.progress_bar['value'] = 0
        self.stats_label.config(text="Extracting video info...")

        thread = threading.Thread(target=self.download_thread, args=(url, out_dir))
        thread.daemon = True
        thread.start()

    def download_thread(self, url, out_dir):
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best', # Grabs the absolute highest quality streams
            'outtmpl': os.path.join(out_dir, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'updatetime': False,
            'progress_hooks': [self.progress_hook],
            'nocheckcertificate': False
        }
        # If ffmpeg sits next to the app (installer build), point yt-dlp at it.
        bundled_dir = os.path.dirname(sys.executable)
        if os.path.exists(os.path.join(bundled_dir, 'ffmpeg.exe')):
            ydl_opts['ffmpeg_location'] = bundled_dir

        error_msg = None
        was_cancelled = False

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            if "User Cancelled" in str(e):
                was_cancelled = True
            else:
                error_msg = str(e)

        self.is_downloading = False
        self.root.after(0, self.finish_download, error_msg, was_cancelled)

    def finish_download(self, error_msg, was_cancelled):
        self.btn_start.config(state=tk.NORMAL)
        self.url_entry.config(state=tk.NORMAL)
        self.btn_out.config(state=tk.NORMAL)
        self.out_entry.config(state=tk.NORMAL)
        self.btn_cancel.config(state=tk.DISABLED)

        if was_cancelled:
            self.stats_label.config(text="Download cancelled.")
            self.progress_bar['value'] = 0
        elif error_msg:
            self.stats_label.config(text="Error occurred. Check console or URL.")
            messagebox.showerror("Download Error", f"An error occurred:\n{error_msg}")
        else:
            self.progress_bar['value'] = 100
            self.stats_label.config(text="100.0% | Done! Closing...")
            
        # 1-second delay before auto-closing on success
        if not error_msg and not was_cancelled:
            self.root.after(1000, self.root.destroy)

    def on_closing(self):
        self.is_downloading = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoDownloaderApp(root)
    root.mainloop()