from dbm import error
import json
import random
import string
from cryptography.fernet import Fernet
import os


KEY_FILE = "secret.key"
ENC_FILE = "passwords.enc"


def load_or_create_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            key = f.read()

    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)

    return key

def show_menu(passwords):

    print("\n====== ŞİFRE YÖNETİCİSİ ======")

    while True:


        menu_text = '''
        1) Yeni şifre ekle 
        2) Şifreleri listele
        3) Şifre ara
        4) Şifre sil
        5) Şifre güncelle
        6) Çıkış '''
        print(menu_text)

        seçim = input("Lütfen seçiminizi giriniz: ").strip().lower()

        try:

            if seçim == "1":
                add_password(passwords)

            elif seçim == "2":
                list_passwords(passwords)

            elif seçim == "3":
                search_passwords(passwords)

            elif seçim == "4":
                delete_password(passwords)

            elif seçim == "5":
                update_passwords(passwords)

            elif seçim == "6":
                print("çıkış seçildi")
                break

            else:
                print("hatalı giriş yaptınız.")

        except Exception as error:
            print(error)

def add_password(passwords):
    print("Yeni şifre ekleme")
    site = input("Lütfen site adı giriniz: ").strip().lower()
    username = input("Lütfen kullanıcı adı giriniz: ").strip().lower()
    seçim = input("Şifreyi kendin mi girmek istersin yoksa otomatik güçlü şifre üretelim mi? y/n: ").strip().lower()
    if seçim == "y":
        password = input("Şifre giriniz: ").strip().lower()
    else:
        password = generate_strong_password()
        print("Oluşturulan güçlü şifre:", password)
    new_id = len(passwords) + 1
    yeni_kayıt = {"id": new_id, "site": site, "username": username, "password": password}
    passwords.append(yeni_kayıt)
    save_passwords(passwords)
    print("Şifre kaydı eklendi")


def generate_strong_password():
    string.ascii_lowercase
    string.ascii_uppercase
    string.digits
    string.punctuation
    string.ascii_letters
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))


def update_passwords(passwords):
    try:
        id = input("Lütfen kullanıcı ID'yi giriniz: ").strip()
        update_id = int(id)
    except ValueError:
        print("Geçersiz ID girdiniz.Lütfen sayı giriniz.")

        return

    found = False

    for index, password in enumerate(passwords):
        if password["id"] == update_id:
            found = True
            masked = "*" * len(password["password"])
            print("Mevcut kayıt:")
            print("ID:", password["id"])
            print("Site:", password["site"])
            print("Username:", password["username"])
            print("Şifre", masked)

            yeni_site = input("Yeni site adı(boş bırak): ").strip().lower()
            if yeni_site != "":
                password["site"] = yeni_site
            yeni_username = input("Yeni kullanıcı adı(boş bırak):").strip().lower()
            if yeni_username != "":
                password["username"] = yeni_username
            yeni_şifre = input("Şifreyi güncellemek ister misin? (e/h): ").strip().lower()
            if yeni_şifre == "e":
                secim = input("Şifreyi kendin mi girmek istersin yoksa otomatik güçlü şifre üretelim mi? y/n: ").strip().lower()
                if secim == "y":
                    password["password"] = input("Şifre giriniz: ").strip().lower()

                elif secim == "n":
                    password["password"] = generate_strong_password()
                    print("Oluşturulan güçlü şifre:", password["password"])
                else:
                    print("Geçersiz seçim, şifre değiştirilemedi.")

            save_passwords(passwords)
            print("kayıt güncellendi.")
            return

    if not found:
        print("Bu ID'ye ait kayıt bulunamadı.")





def list_passwords(passwords):
        if len(passwords) == 0:
            print("Kayıtlı şifre yok")
        for password in passwords:
            password["id"], password["site"], password["username"], password["password"]
            masked = "*" * len(password["password"])
            print("id", password["id"], password["site"], password["username"], masked)


def search_passwords(passwords):
    arama = input(" Aramak istediğiniz site veya kullanıcı adı: ").strip().lower()
    bulundu = False
    for password in passwords:
        site = password["site"].lower()
        username = password["username"].lower()
        if arama in site or arama in username:
            masked = "*" * len(password["password"])
            print("id", password["id"], password["site"], password["username"], masked)
            bulundu = True
    if not bulundu:
        print("Eşleşen kullanıcı adı veya site bulunamadı")


def delete_password(passwords):
    try:
        silmek = input("Silmek istediğiniz kaydın ID'sini giriniz: ").strip()
        record_id = int(silmek)
        save_passwords(passwords)
    except ValueError:
        print("Geçersiz bir sayı girdiniz. Lütfen tekrar deneyiniz.")
        return

    found = False

    for index, password in enumerate(passwords):
        if password["id"] == record_id:
            found = True
            print("id", password["id"], password["site"], password["username"], password["password"])
            onay = input("Bu kaydı silmek istiyor musun? (e/h): ").strip().lower()

            if onay == "e":
                passwords.pop(index)
                print("Kayıt silindi.")
            elif onay == "h":
                print("Silme işlemi iptal edildi.")
            else:
                print("Geçersiz seçim, silme işlemi iptal edildi.")

            return

    if not found:
        print("Bu ID'ye ait kayıt bulunamadı.")


def save_passwords(passwords):
    #python listesini json stringe çevirme
    data_str = json.dumps(passwords, ensure_ascii=False, indent=2)
    data_bytes = data_str.encode("utf-8")

    #anahtar yükleme-oluşturma
    key = load_or_create_key()
    f = Fernet(key)

    #json veri güncelleme
    encrypted = f.encrypt(data_bytes)

    #şifreli veriyi dosyaya yaz,binary şeklinde
    with open(ENC_FILE, "wb") as f_out:
        f_out.write(encrypted)


def load_passwords():
    #şifreli dosya yoksa: boş liste dön
    if not os.path.isfile(ENC_FILE):
        return []


    try:
        #şifreli veriyi okuma
        with open(ENC_FILE, "rb") as f_in:
            encrypted = f_in.read()

        #anahtar yükleme
        key = load_or_create_key()
        f = Fernet(key)

        #veri çözme
        decrypted = f.decrypt(encrypted)

        #json stringten python listesine dönüştürme
        data_str = decrypted.decode("utf-8")
        data = json.loads(data_str)
        return data

    except Exception as e:
        print("Şifreli dosya okunurken bir hata oluştu:", e)
        print("Boş liste ile başlatılıyor.")
        return []




if __name__ == '__main__':
    passwords = load_passwords()
    show_menu(passwords)


