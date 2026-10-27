# YouTube RTMP Studio

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-1f6aa5)](https://customtkinter.tomschimansky.com/)
[![yt-dlp](https://img.shields.io/badge/Download-yt--dlp-8A2BE2)](https://github.com/yt-dlp/yt-dlp)
[![FFmpeg](https://img.shields.io/badge/Media-FFmpeg-007808?logo=ffmpeg&logoColor=white)](https://ffmpeg.org/)
[![License](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey)](#kurulum)

**YouTube RTMP Studio**, Python ile geliştirilmiş masaüstü arayüzü üzerinden, kullanıcının indirme ve yeniden yayınlama hakkına sahip olduğu bir YouTube videosunu indirip FFmpeg aracılığıyla RTMP/RTMPS hedefine göndermeyi amaçlayan bir yardımcı uygulamadır. Arayüz; kalite seçimi, isteğe bağlı döngü, ilerleme bilgisi, yayın süresi ve işlem günlüğü sunar.

> **Önemli:** Yalnızca size ait olan veya indirme ve yeniden yayınlama için açık izniniz bulunan içerikleri kullanın. YouTube, yayın platformu ve içerik sahibinin koşullarına uyun. Bu proje yayın anahtarı ya da yayın hedefi sağlamaz; hedef adresini yayın sağlayıcınızdan almanız gerekir.

## 🧰 Teknoloji kartları

| Teknoloji | Kullanım amacı |
|---|---|
| ![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white) | Uygulama mantığı ve iş parçacıkları |
| ![CustomTkinter](https://img.shields.io/badge/CustomTkinter-GUI-1f6aa5) | Koyu temalı masaüstü arayüzü |
| ![yt-dlp](https://img.shields.io/badge/yt--dlp-Downloader-8A2BE2) | Desteklenen YouTube bağlantısından video indirme |
| ![FFmpeg](https://img.shields.io/badge/FFmpeg-Transcode%20%2F%20RTMP-007808?logo=ffmpeg&logoColor=white) | Videoyu kodlama ve RTMP/RTMPS hedefine gönderme |
| ![threading](https://img.shields.io/badge/Python-threading-informational) | İndirme/yayın işini arayüzden ayrı yürütme |
| ![queue](https://img.shields.io/badge/Python-queue-informational) | İşçi iş parçacığından arayüze durum iletimi |

## ✨ Özellikler

- YouTube video URL'si için temel biçim kontrolü.
- RTMP ve RTMPS hedef adresi doğrulaması.
- 1080p, 720p ve 480p için üst çözünürlük seçimi.
- İndirme ilerlemesi ve indirilen veri miktarının gösterimi.
- MP4 kapsayıcısında birleştirme girişimi (yt-dlp/FFmpeg desteğine bağlıdır).
- İsteğe bağlı sürekli döngüyle yayın.
- Başlat/durdur kontrolleri, yayın süresi sayacı ve işlem günlüğü.
- RTMP adresinin günlüklerde maskelenmesi.
- FFmpeg'i uygulama klasöründe veya sistem PATH'inde arama.

## 📁 Proje yapısı

~~~text
youtube-rtmp-studio/
├── youtube_rtmp_studio.py   # Arayüz, indirme ve yayın akışı
├── requirements.txt         # Python paket bağımlılıkları
├── LICENSE                  # Apache License 2.0
└── README.md                # Proje dokümantasyonu
~~~

## 🚀 Kurulum

### Gereksinimler

- Python 3.10 veya üzeri önerilir.
- FFmpeg kurulu olmalı ve PATH üzerinden erişilebilmeli ya da çalıştırılabilir dosyası uygulama klasöründe bulunmalı.
- YouTube bağlantısına erişim ve geçerli bir RTMP/RTMPS yayın hedefi.
- Yayın için yeterli yükleme bant genişliği ve hedef platformda yayın yetkisi.

### 1. Depoyu indirin

~~~bash
git clone https://github.com/ebubekirbastama/youtube-rtmp-studio.git
cd youtube-rtmp-studio
~~~

### 2. Sanal ortam oluşturun (önerilir)

Windows:

~~~powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
~~~

Linux:

~~~bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
~~~

### 3. FFmpeg'i kurun

FFmpeg'i resmi [FFmpeg web sitesinden](https://ffmpeg.org/download.html) veya işletim sisteminizin güvenilir paket yöneticisinden kurun. Terminalde **ffmpeg -version** komutunun çalıştığını doğrulayın. Alternatif olarak Windows'ta **ffmpeg.exe** dosyasını **youtube_rtmp_studio.py** ile aynı klasöre koyabilirsiniz.

### 4. Uygulamayı başlatın

~~~bash
python youtube_rtmp_studio.py
~~~

Bağımlılıklar **requirements.txt** dosyasında listelenmiştir: **customtkinter** ve **yt-dlp**.

## ▶️ Kullanım

1. **YouTube bağlantısı** alanına desteklenen bir HTTPS video bağlantısı girin.
2. **RTMP / RTMPS yayın adresi** alanına yayın platformunuzun verdiği tam hedef adresi ve yayın anahtarını girin. Bu alan ekranda gizlenir.
3. İndirme klasörünü seçin. Varsayılan klasör **~/Downloads/YouTubeRTMP** konumudur.
4. Yayın için üst çözünürlük sınırını seçin: 1080p, 720p veya 480p.
5. Videonun bitince yeniden başlamasını istiyorsanız **Video bitince başa sar** seçeneğini açık bırakın.
6. **İndir ve Yayını Başlat** düğmesine basın.
7. Durum, sayaç ve işlem günlüğünü izleyin. Durdurmak için **Durdur** düğmesini kullanın.
8. Yayının hedef platformda gerçekten alındığını ayrıca o platformun yayın kontrol panelinden doğrulayın.

## 🔍 Çalışma akışı

1. Girdi alanları kontrol edilir; URL şeması ve RTMP/RTMPS adresi doğrulanır.
2. FFmpeg yerel uygulama klasöründe veya sistem PATH'inde aranır.
3. Arka plan iş parçacığı yt-dlp ile video bilgisini alır ve dosyayı seçilen klasöre indirir.
4. İndirme kancası ilerleme durumunu arayüze aktarır.
5. İndirilen dosya belirlenir; FFmpeg uygun görüntü boyutuna ölçekler, H.264 video ve AAC ses olarak kodlar.
6. FFmpeg, FLV taşıyıcısıyla RTMP/RTMPS hedefine yayın gönderir.
7. Günlükteki FFmpeg çıktısı ve işlem sonucu kullanıcıya aktarılır; durdurma veya hata durumunda alt süreç kapatılmaya çalışılır.

## ⚙️ Kodda kullanılan yayın varsayılanları

| Ayar | Mevcut uygulama |
|---|---|
| Video kodlayıcı | libx264, veryfast, zerolatency |
| Kare hızı | 30 FPS |
| Video bit hızı | 2500 kbit/s |
| GOP | 60 kare |
| Ses kodlayıcı | AAC, 128 kbit/s, 44.1 kHz |
| Piksel biçimi | yuv420p |
| Çıkış biçimi | FLV üzerinden RTMP/RTMPS |

Kalite menüsü kodlamanın üst çözünürlük sınırını belirler; bit hızı şu an menü seçimine göre otomatik değişmez.

## ⚠️ Teknik sınırlamalar

- Uygulama bir canlı YouTube akışını doğrudan aktarmak yerine önce videoyu yerel diske indirir, ardından dosyayı yayınlar. Büyük dosyalar için disk alanı ve indirme süresi gerekir.
- yt-dlp desteği, YouTube tarafındaki değişikliklere ve erişim koşullarına bağlıdır; bazı videolar indirilemeyebilir.
- Çözünürlük seçimi üst sınırdır; daha düşük çözünürlüklü kaynak büyütülmez. Video bit hızı sabit 2500 kbit/s olarak ayarlanmıştır.
- Sürekli döngü seçeneği aynı yerel dosyayı tekrar oynatır; oynatma listesi veya otomatik kaynak değiştirme sistemi değildir.
- Uygulama yayın sunucusunun yayını kabul ettiğini kesin olarak doğrulayamaz. Yayın platformunun kontrol paneli ayrıca incelenmelidir.
- Yayın durumu göstergesi FFmpeg sürecinin başlatılmasına dayanır; platformdaki yayının gerçekten izleyiciye açık olduğunun tek başına kanıtı değildir.
- FFmpeg çıktısı satır satır okunur; ayrıntılı yapılandırılmış loglama, otomatik yeniden bağlanma ve kapsamlı ağ hata kurtarma mekanizması bulunmaz.
- Arayüz iş parçacığı ile arka plan süreci arasındaki durum yönetimi basittir; uzun süreli yayınlarda farklı durdurma/çıkış senaryoları test edilmelidir.
- Bu README kaynak koddan çalıştırmayı açıklar; depoda hazır Windows EXE bulunduğu varsayılmamalıdır.

## 🔐 Güvenli ve sorumlu kullanım

- RTMP/RTMPS adresleri çoğunlukla yayın anahtarı içerir. Bu bilgiyi README, ekran görüntüsü, herkese açık günlük veya hata raporuna koymayın.
- Yayın anahtarını başkalarıyla paylaşmayın; ifşa edilirse yayın platformundan yenileyin.
- Uygulamayı yalnızca yeniden yayınlama izniniz bulunan içeriklerle kullanın.
- Kaynak kodu ve Python paketlerini güvenilir kaynaklardan edinin; bağımlılıkları güncel tutun.
- Bilinmeyen bir yayın hedefine veri göndermeden önce hedef alan adını doğrulayın.
- Bu araç bir yayın platformunun kurallarını, telif hakkını veya erişim kontrollerini aşmak için tasarlanmamalıdır.

## 🛠️ Modernizasyon önerileri

- Her çözünürlük için yapılandırılabilir video bit hızı, GOP ve ses ayarları eklemek.
- RTMP anahtarını giriş alanında gizli tutmanın yanında işletim sistemi kimlik bilgisi deposu veya güvenli yapılandırma desteği eklemek.
- FFmpeg çıkış kodunu, bağlantı zaman aşımını ve hedef sunucu hatalarını ayrı sınıflandırmak.
- Kontrollü yeniden bağlanma, yayın öncesi hedef testi ve yayın sağlığı göstergesi eklemek.
- İşlem durdurma ve pencere kapatma sırasında alt sürecin tamamen sonlandığını güvence altına alan süreç yönetimini geliştirmek.
- Bağımlılık sürümlerini kilitlemek ve Windows/Linux için otomatik testler eklemek.
- Uygulama sürümü, yapılandırılmış loglama ve kullanıcı dostu hata raporu desteği eklemek.
- Büyük indirmeler için disk alanı kontrolü ve indirme tamamlandıktan sonra dosyayı koruma/silme tercihi sunmak.

## 📜 Lisans

Bu proje depodaki [Apache License 2.0](LICENSE) lisansıyla dağıtılır. Üçüncü taraf bileşenler kendi lisans koşullarına tabidir.

## 👨‍💻 Geliştirici

**Ebubekir Bastama**  
GitHub: [@ebubekirbastama](https://github.com/ebubekirbastama)

---

[Hata bildirimi veya öneri](https://github.com/ebubekirbastama/youtube-rtmp-studio/issues) için GitHub Issues bölümünü kullanabilirsiniz.
