"""YouTube -> RTMP Studio. Yalnızca yayınlama hakkınız olan içeriklerde kullanın."""
import os
import queue
import shutil
import subprocess
import threading
import time
from pathlib import Path
from urllib.parse import urlparse

import customtkinter as ctk
from tkinter import filedialog, messagebox
from yt_dlp import YoutubeDL

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue')

HOME = Path.home() / 'Downloads' / 'YouTubeRTMP'
FONTS = ('Segoe UI', 13)

class Cancelled(Exception):
    pass

class Studio(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('YouTube → RTMP | Broadcast Studio')
        self.geometry('960x740')
        self.minsize(800, 660)
        self.configure(fg_color='#0b1020')
        self.messages = queue.Queue()
        self.stop_flag = threading.Event()
        self.process = None
        self.running = False
        self.broadcast_since = None
        self.download_file = None
        self._build()
        self.after(150, self._poll)
        self.protocol('WM_DELETE_WINDOW', self._close)

    def _build(self):
        root = ctk.CTkFrame(self, fg_color='transparent')
        root.pack(fill='both', expand=True, padx=30, pady=24)
        ctk.CTkLabel(root, text='◉  BROADCAST STUDIO', font=('Segoe UI', 27, 'bold'), text_color='#f8fafc').pack(anchor='w')
        ctk.CTkLabel(root, text='YouTube videosunu indir • RTMP / RTMPS adresine gerçek zamanlı gönder',
                     text_color='#a2aec2', font=FONTS).pack(anchor='w', pady=(2, 18))

        panel = ctk.CTkFrame(root, fg_color='#151d30', corner_radius=17)
        panel.pack(fill='x', pady=(0, 12))
        ctk.CTkLabel(panel, text='YAYIN AYARLARI', font=('Segoe UI', 15, 'bold'), text_color='#d8e6ff').pack(anchor='w', padx=22, pady=(18, 9))
        self.url = self._field(panel, 'YouTube bağlantısı', 'https://www.youtube.com/watch?v=...')
        self.rtmp = self._field(panel, 'RTMP / RTMPS yayın adresi (yayın anahtarı dahil)', 'rtmps://sunucu/app/yayin-anahtari', secret=True)
        dirrow = ctk.CTkFrame(panel, fg_color='transparent')
        dirrow.pack(fill='x', padx=22, pady=(4, 10))
        ctk.CTkLabel(dirrow, text='İndirme klasörü', text_color='#cbd5e1', font=FONTS).pack(anchor='w', pady=(0, 5))
        chooser = ctk.CTkFrame(dirrow, fg_color='transparent')
        chooser.pack(fill='x')
        self.folder = ctk.CTkEntry(chooser, height=38, corner_radius=9, fg_color='#0b1325', border_color='#293854')
        self.folder.insert(0, str(HOME))
        self.folder.pack(side='left', fill='x', expand=True)
        ctk.CTkButton(chooser, text='Gözat', width=90, height=38, command=self._choose_folder).pack(side='left', padx=(9, 0))

        toggles = ctk.CTkFrame(panel, fg_color='transparent')
        toggles.pack(fill='x', padx=22, pady=(2, 18))
        self.loop = ctk.CTkSwitch(toggles, text='Video bitince başa sar (sürekli yayın)', font=('Segoe UI', 12))
        self.loop.pack(side='left')
        self.loop.select()
        self.quality = ctk.CTkOptionMenu(toggles, values=['1080p', '720p', '480p'], width=110)
        self.quality.set('720p')
        self.quality.pack(side='right')
        ctk.CTkLabel(toggles, text='Yayın çözünürlüğü', text_color='#a2aec2').pack(side='right', padx=10)

        controls = ctk.CTkFrame(root, fg_color='transparent')
        controls.pack(fill='x', pady=(5, 12))
        self.start_btn = ctk.CTkButton(controls, text='▶   İNDİR VE YAYINI BAŞLAT', height=49,
                                       fg_color='#2563eb', hover_color='#1d4ed8', font=('Segoe UI', 14, 'bold'),
                                       command=self._start)
        self.start_btn.pack(side='left', fill='x', expand=True)
        self.stop_btn = ctk.CTkButton(controls, text='■   DURDUR', height=49, width=165,
                                      fg_color='#992c42', hover_color='#7f1d1d', font=('Segoe UI', 13, 'bold'),
                                      command=self._stop, state='disabled')
        self.stop_btn.pack(side='left', padx=(10, 0))

        statuspanel = ctk.CTkFrame(root, fg_color='#151d30', corner_radius=17)
        statuspanel.pack(fill='x', pady=(0, 12))
        top = ctk.CTkFrame(statuspanel, fg_color='transparent')
        top.pack(fill='x', padx=21, pady=(17, 7))
        self.status = ctk.CTkLabel(top, text='●  Hazır', text_color='#94a3b8', font=('Segoe UI', 16, 'bold'))
        self.status.pack(side='left')
        self.clock = ctk.CTkLabel(top, text='00:00:00', text_color='#e2e8f0', font=('Consolas', 16))
        self.clock.pack(side='right')
        self.progress = ctk.CTkProgressBar(statuspanel, height=13, progress_color='#3b82f6')
        self.progress.pack(fill='x', padx=21, pady=(9, 10))
        self.progress.set(0)
        self.detail = ctk.CTkLabel(statuspanel, text='Bağlantı ve yayın adresini girerek başlayın.', text_color='#9aa9c0')
        self.detail.pack(anchor='w', padx=21, pady=(0, 18))

        loghead = ctk.CTkFrame(root, fg_color='transparent')
        loghead.pack(fill='x', pady=(3, 7))
        ctk.CTkLabel(loghead, text='İŞLEM GÜNLÜĞÜ', font=('Segoe UI', 14, 'bold'), text_color='#d8e6ff').pack(side='left')
        ctk.CTkButton(loghead, text='Temizle', width=74, height=29, fg_color='#334155', command=self._clear_log).pack(side='right')
        self.logs = ctk.CTkTextbox(root, fg_color='#0d1425', border_width=1, border_color='#26344c',
                                   font=('Consolas', 12), text_color='#d3e0f3', corner_radius=13, wrap='word')
        self.logs.pack(fill='both', expand=True)
        self.logs.configure(state='disabled')
        self._log('Uygulama hazır. FFmpeg sistemde veya uygulama klasöründe olmalı.')

    def _field(self, parent, label, placeholder, secret=False):
        ctk.CTkLabel(parent, text=label, text_color='#cbd5e1', font=FONTS).pack(anchor='w', padx=22, pady=(5, 5))
        entry = ctk.CTkEntry(parent, height=42, placeholder_text=placeholder, corner_radius=9,
                             fg_color='#0b1325', border_color='#293854', show='•' if secret else '')
        entry.pack(fill='x', padx=22, pady=(0, 11))
        return entry

    def _choose_folder(self):
        selected = filedialog.askdirectory(initialdir=str(Path.home()))
        if selected:
            self.folder.delete(0, 'end')
            self.folder.insert(0, selected)

    def _clear_log(self):
        self.logs.configure(state='normal')
        self.logs.delete('1.0', 'end')
        self.logs.configure(state='disabled')

    def _log(self, message):
        self.logs.configure(state='normal')
        self.logs.insert('end', f'[{time.strftime("%H:%M:%S")}] {message}\n')
        self.logs.see('end')
        self.logs.configure(state='disabled')

    def _emit(self, kind, data=None):
        self.messages.put((kind, data))

    def _poll(self):
        try:
            while True:
                kind, data = self.messages.get_nowait()
                if kind == 'log':
                    self._log(data)
                elif kind == 'status':
                    self.status.configure(text=data[0], text_color=data[1])
                elif kind == 'detail':
                    self.detail.configure(text=data)
                elif kind == 'progress':
                    self.progress.set(max(0, min(1, data)))
                elif kind == 'live':
                    self.broadcast_since = time.monotonic()
                elif kind == 'done':
                    self.running = False
                    self.process = None
                    self.start_btn.configure(state='normal')
                    self.stop_btn.configure(state='disabled')
                    self.broadcast_since = None
        except queue.Empty:
            pass
        if self.broadcast_since:
            seconds = int(time.monotonic() - self.broadcast_since)
            self.clock.configure(text=f'{seconds // 3600:02}:{seconds // 60 % 60:02}:{seconds % 60:02}')
        self.after(150, self._poll)

    def _start(self):
        if self.running:
            return
        url = self.url.get().strip()
        dest = self.rtmp.get().strip()
        folder = Path(self.folder.get().strip()).expanduser()
        if not (url.startswith('https://www.youtube.com/') or url.startswith('https://youtu.be/') or
                url.startswith('https://m.youtube.com/') or url.startswith('https://music.youtube.com/')):
            messagebox.showerror('Geçersiz bağlantı', 'Geçerli bir HTTPS YouTube video bağlantısı girin.')
            return
        parsed = urlparse(dest)
        if parsed.scheme not in ('rtmp', 'rtmps') or not parsed.netloc or not parsed.path.strip('/'):
            messagebox.showerror('Geçersiz RTMP', 'rtmp:// veya rtmps:// ile başlayan tam yayın adresini girin.')
            return
        ffmpeg = self._find_ffmpeg()
        if not ffmpeg:
            messagebox.showerror('FFmpeg bulunamadı', 'FFmpeg kurun ve PATH içine ekleyin veya ffmpeg.exe dosyasını bu uygulamanın yanına koyun.')
            return
        try:
            folder.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            messagebox.showerror('Klasör hatası', str(exc))
            return
        self.stop_flag.clear()
        self.running = True
        self.broadcast_since = None
        self.clock.configure(text='00:00:00')
        self.start_btn.configure(state='disabled')
        self.stop_btn.configure(state='normal')
        self.progress.set(0)
        opts = (url, dest, folder, ffmpeg, int(self.quality.get().replace('p', '')), bool(self.loop.get()))
        threading.Thread(target=self._worker, args=opts, daemon=True).start()

    @staticmethod
    def _find_ffmpeg():
        local = Path(__file__).resolve().parent / ('ffmpeg.exe' if os.name == 'nt' else 'ffmpeg')
        return str(local) if local.is_file() else shutil.which('ffmpeg')

    def _stop(self):
        self.stop_flag.set()
        self._emit('status', ('●  Durduruluyor...', '#fbbf24'))
        self._emit('log', 'Durdurma istendi.')
        proc = self.process
        if proc and proc.poll() is None:
            try:
                proc.terminate()
            except OSError:
                pass

    def _worker(self, url, dest, folder, ffmpeg, height, loop):
        try:
            self._emit('status', ('●  İndiriliyor', '#60a5fa'))
            self._emit('log', 'Video bilgisi alınıyor ve indirme başlatılıyor...')
            saved = {'value': None}
            last_pct = {'value': -1}

            def hook(d):
                if self.stop_flag.is_set():
                    raise Cancelled()
                if d.get('status') == 'downloading':
                    total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
                    got = d.get('downloaded_bytes') or 0
                    if total:
                        pct = int(got * 100 / total)
                        if pct != last_pct['value']:
                            last_pct['value'] = pct
                            self._emit('progress', got / total)
                            self._emit('detail', f'İndirme: %{pct} • {got / 1048576:.1f} MB / {total / 1048576:.1f} MB')
                elif d.get('status') == 'finished':
                    saved['value'] = d.get('filename')
                    self._emit('detail', 'İndirme tamamlandı; ses/video birleştiriliyor...')

            options = {
                'format': f'bestvideo[height<={height}]+bestaudio/best[height<={height}]/best',
                'merge_output_format': 'mp4',
                'outtmpl': str(folder / '%(title).160B [%(id)s].%(ext)s'),
                'noplaylist': True,
                'ffmpeg_location': str(Path(ffmpeg).parent),
                'progress_hooks': [hook],
                'quiet': True,
                'no_warnings': True,
                'overwrites': True,
            }
            with YoutubeDL(options) as ydl:
                info = ydl.extract_info(url, download=True)
                video_id = info.get('id')
                if not video_id:
                    raise RuntimeError('İndirilen videonun kimliği alınamadı.')
                matching = [p for p in folder.iterdir() if f'[{video_id}]' in p.name and p.suffix.lower() in ('.mp4', '.mkv', '.webm', '.mov')]
                if not matching:
                    # yt-dlp can finalize a file under a different extension/template
                    source = saved['value']
                    if source:
                        base = Path(source)
                        matching = [p for p in (base.with_suffix('.mp4'), base.with_suffix('.mkv'), base) if p.is_file()]
                if not matching:
                    raise RuntimeError('İndirilen video dosyası bulunamadı.')
                video = max(matching, key=lambda p: p.stat().st_mtime)
            if self.stop_flag.is_set():
                raise Cancelled()
            self.download_file = video
            self._emit('progress', 1)
            self._emit('log', f'İndirildi: {video.name}')
            self._emit('status', ('●  RTMP bağlantısı kuruluyor', '#fbbf24'))
            self._emit('detail', 'FFmpeg yayına hazırlanıyor...')

            # Her video boyutuna uyumlu (çift piksel), 30 fps, stereo AAC.
            vf = f'scale=w=trunc(iw*min({height}/ih\\,1)/2)*2:h=trunc(ih*min({height}/ih\\,1)/2)*2,format=yuv420p'
            cmd = [ffmpeg, '-hide_banner', '-nostdin', '-loglevel', 'error',
                   '-stream_loop', '-1' if loop else '0', '-re', '-i', str(video),
                   '-map', '0:v:0', '-map', '0:a:0?', '-vf', vf,
                   '-c:v', 'libx264', '-preset', 'veryfast', '-tune', 'zerolatency',
                   '-r', '30', '-pix_fmt', 'yuv420p', '-g', '60',
                   '-b:v', '2500k', '-maxrate', '2500k', '-bufsize', '5000k',
                   '-c:a', 'aac', '-b:a', '128k', '-ar', '44100',
                   '-f', 'flv', dest]
            flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            self.process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
                                            text=True, encoding='utf-8', errors='replace',
                                            creationflags=flags)
            self._emit('live', None)
            self._emit('status', ('●  YAYIN AKTİF', '#4ade80'))
            self._emit('detail', f'Yayın dosyası: {video.name}')
            self._emit('log', 'FFmpeg başlatıldı. Sunucunun yayını kabul ettiğini kendi panelinizden doğrulayın.')
            errors = []
            for line in self.process.stderr:
                if self.stop_flag.is_set():
                    break
                # Yayın anahtarının günlükte görünmesini önle.
                clean = line.strip().replace(dest, '[RTMP ADRESİ GİZLENDİ]')
                if clean:
                    errors.append(clean)
                    self._emit('log', clean[:300])
            if self.stop_flag.is_set():
                self._stop_process()
                raise Cancelled()
            code = self.process.wait()
            if code != 0:
                raise RuntimeError(f'FFmpeg hata kodu {code}. ' + (errors[-1] if errors else 'RTMP bağlantısını kontrol edin.'))
            self._emit('status', ('●  Yayın tamamlandı', '#4ade80'))
            self._emit('detail', 'Video sonuna ulaşıldı.')
            self._emit('log', 'Yayın normal şekilde tamamlandı.')
        except Cancelled:
            self._emit('status', ('●  Durduruldu', '#94a3b8'))
            self._emit('detail', 'İşlem kullanıcı tarafından durduruldu.')
            self._emit('log', 'İşlem durduruldu.')
        except Exception as exc:
            self._emit('status', ('●  Hata', '#fb7185'))
            self._emit('detail', 'Ayrıntılar işlem günlüğünde.')
            self._emit('log', 'HATA: ' + str(exc).replace(dest, '[RTMP ADRESİ GİZLENDİ]')[:800])
        finally:
            self._stop_process()
            self._emit('done')

    def _stop_process(self):
        proc = self.process
        if proc and proc.poll() is None:
            try:
                proc.terminate()
                proc.wait(timeout=3)
            except (subprocess.TimeoutExpired, OSError):
                proc.kill()
                proc.wait()

    def _close(self):
        if self.running:
            if not messagebox.askyesno('Çıkış', 'Yayın/indirme sürüyor. Durdurup çıkılsın mı?'):
                return
            self._stop()
        self.destroy()

if __name__ == '__main__':
    Studio().mainloop()
