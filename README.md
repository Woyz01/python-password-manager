# Python Password Manager

Basit ama mantığı güçlü bir **şifre yöneticisi (Password Manager)**.  
Tamamen Python ile yazıldı ve şu özellikleri destekliyor:

- Komut satırı menü arayüzü (CLI)
- Şifre ekleme, listeleme, arama, silme, güncelleme (tam CRUD)
- Otomatik güçlü şifre üretici (random)
- Şifreleri ekranda **yıldızlı (maskeli)** gösterme
- Verileri düz JSON yerine **AES ile şifrelenmiş dosyada** saklama

Bu proje, hem *Python temellerini* hem de *mini bir gerçek uygulamanın mantığını* göstermek için geliştirilmiştir.

---

##  Özellikler

  - **CRUD İşlemleri**
  - Yeni şifre kaydı ekleme
  - Kayıtlı şifreleri listeleme
  - Site veya kullanıcı adına göre arama
  - ID’ye göre silme
  - ID’ye göre kayıt güncelleme

  - **Şifreleri Maskeli Gösterme**
  - Listeleme ve arama ekranlarında şifreler `*****` şeklinde gösterilir.
  - Gerçek şifreler sadece şifreli dosyada tutulur.

  - **AES ile Şifrelenmiş Kayıtlar**
  - Kullanıcı verileri düz `passwords.json` yerine `passwords.enc` isimli **şifreli dosyada** saklanır.
  - Şifreleme için [`cryptography`](https://pypi.org/project/cryptography/) kütüphanesi ve `Fernet` kullanılır.
  - Uygulama ilk çalıştığında bir `secret.key` oluşturur ve bu key ile tüm veriler şifrelenir/çözülür.

  - **Otomatik Güçlü Şifre Üretici**
  - Kullanıcı yeni kayıt eklerken:
    - İster kendi şifresini yazar
    - İster otomatik güçlü şifre üretilmesini seçer
  - Üretilen şifreler; harf + rakam kombinasyonundan oluşur.

---

##  Proje Yapısı

```text
python-password-manager/
├── src/
│   └── main.py          # Uygulamanın ana dosyası
├── data/                # (İsteğe bağlı) Şifreli dosyalar için klasör
│   ├── passwords.enc    # Şifrelenmiş şifre veritabanı
│   └── secret.key       # AES anahtarı (Fernet key)
├── .gitignore
├── requirements.txt
└── README.md


 Kurulum

git clone https://github.com/Woyz01/python-password-manager.git
cd python-password-manager

Sanal ortam kurmamız daha işimize yarayacaktır.Bunun içinde;

python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux / macOS:
source .venv/bin/activate


## Gereksinimleri yükleme;
pip install -r requirements.txt

## Çalıştırma
cd src
python main.py

Uygulama açıldığında menü göreceksiniz:
1) Yeni şifre ekle
2) Şifreleri listele
3) Şifre ara
4) Şifre sil
5) Çıkış
6) Şifre güncelle


Veri Yapısı ise şu şekildedir:
{
    "id": 1,                               ##python sözlüğü(dict) olarak tutulur.
    "site": "örnek.com",
    "username": "kullanici",
    "password": "gizli_sifre"
}


JSON + AES Şifreleme Akışı
- passwords listesi json.dumps ile JSON string'e çevrilir.
- JSON string utf-8 ile bytes haline getirilir.
- Fernet ile şifrelenir ve passwords.enc dosyasına yazılır.
- Uygulama açıldığında:
//secret.key yüklenir (yoksa oluşturulur)
//passwords.enc okunur, çözülür, JSON parse edilir ve tekrar passwords listesine aktarılır.
Bu sayede veriler düz metin olarak değil, şifrelenmiş biçimde saklanır.



Güvenlik Notları:
- Bu proje, öğrenme ve demo amaçlıdır.
- Gerçek dünyada:
secret.key dosyası çok iyi korunmalı, asla GitHub’a yüklenmemelidir.
Ek olarak “master password” mantığı ve daha güçlü şifre politikaları kullanılmalıdır.
- Ama bu haliyle bile:
Düz txt/JSON yerine şifreli depolama mantığını gösterir.


Gelecek Geliştirmeler
- Master password ile uygulama açılışı
- Şifre üreticide büyük/küçük harf + sembol desteğini genişletme
- Tkinter veya başka bir GUI ile masaüstü arayüz
- PyInstaller ile .exe haline getirme
- Testler (unittest veya pytest) ekleme




Katkı ve Lisans

Author: Cihan (Woyz01)





```bash
git add README.md
git commit -m "Add project README"
git push
