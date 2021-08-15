#!/usr/bin/python3
#######################################
#   TODOS OS DIREITOS RESERVADOS Á    #
#  GABRIEL CAMARGO É CAMARGO SCRIPTS  #
#          COPIA NÃO COMEDIA          #
#######################################


import os
import sys
import json
import time
import shutil
import requests
import webbrowser
import shutil
import psutil
import pygetwindow
import urllib.request
from zipfile import ZipFile
import tkinter.font as tkFont
from winregistry import WinRegistry as Reg
from tkinter import *
from PIL import ImageTk, Image
from playsound import playsound
from threading import Thread
from mta.monitoring import Server
import win32com.shell.shell as shell
import subprocess

#Config
NomeDoServidor = "Brasil São Paulo RP"
idLauncher = "4467646486768"
Version = "1.2"

#Verificar se Existe outra processo
pid = os.getpid()
for proc in psutil.process_iter(['pid', 'name']):
    inf = json.dumps(proc.info)
    inf2 = json.loads(inf)
    if(inf2['name'] == NomeDoServidor+'.exe' and inf2['pid'] != pid):
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess.call('taskkill /F /PID '+str(inf2['pid']), startupinfo=si)

#Info Dir Path
dir_path = os.path.dirname(os.path.realpath(__file__))

#API Launcher
dados = {'api': idLauncher}
x = requests.post("http://54.39.68.176/", data=dados)
inf = json.loads(x.text)

#Registro RegeDit verificar se existe o MTA
reg = Reg()
path = r'HKLM\SOFTWARE\WOW6432Node\Multi Theft Auto: San Andreas All\Common'

#AutoUpdate
dadosUpdate = {'api': idLauncher, 'version': Version}
xUpdate = requests.post("http://54.39.68.176/", data=dadosUpdate)
jsonUpdate = json.loads(xUpdate.text)
try:
    if jsonUpdate["success"]:
        pass
except:
    TelaDownload = Tk()
    TelaDownload.title(NomeDoServidor + ' - Auto Update')
    TelaDownload["borderwidth"] = 0
    TelaDownload.resizable(0, 0)
    TelaDownload.overrideredirect(True)
    TelaDownload.wm_attributes("-transparentcolor", "gray")
    TelaDownload.bind("<Escape>", lambda e: e.widget.quit())
    TelaDownload.focus_set()
    ws = TelaDownload.winfo_screenwidth()
    hs = TelaDownload.winfo_screenheight()
    wid = ws / 1.824
    hei = hs / 1.706
    #TelaDownload.wm_attributes("-topmost", True)
    TelaDownload.config(bg=None)
    x = (ws / 2) - (wid / 2)
    y = (hs / 2) - (hei / 2)
    TelaDownload.geometry('%dx%d+%d+%d' % (wid, hei, x, y))

    can = Canvas(TelaDownload, width=wid, height=hei, bg='gray', bd=0, highlightthickness=0, relief='ridge')
    can.grid()

    image1 = ImageTk.PhotoImage(Image.open(dir_path + "\\media\\1bg.png").resize((ws, hs), Image.ANTIALIAS))
    can.create_image(x, y, image=image1)


    def ClosePrograma(event):
        pid = os.getpid()
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess.call('taskkill /F /PID ' + str(pid), startupinfo=si)


    def check_hand_enter():
        can.config(cursor="hand2")


    def check_hand_leave():
        can.config(cursor="")

    CloseX = int(ws / 34.2)
    CloseY = int(hs / 19.2)
    Close = ImageTk.PhotoImage(
        Image.open(dir_path + "\\media\\close.png").resize((CloseX, CloseY), Image.ANTIALIAS))
    CloseBtn = can.create_image(ws / 1.9, hs / 30, image=Close, tags="CloseBtn")
    can.tag_bind(CloseBtn, "<Enter>", lambda event: check_hand_enter())
    can.tag_bind(CloseBtn, "<Leave>", lambda event: check_hand_leave())
    can.tag_bind(CloseBtn, "<Button-1>", ClosePrograma)
    can.tag_bind(CloseBtn, "<Key>", ClosePrograma)

    ImgLogoX = int(ws / 5.464)
    ImgLogoY = int(hs / 3.072)
    img = Image.open(dir_path + '\\media\\logo.png')
    img = img.resize((ImgLogoX, ImgLogoY), Image.ANTIALIAS)
    Imgimage = ImageTk.PhotoImage(img)
    can.create_image(ws / 3.7, hs / 5, image=Imgimage)

    fill_line = can.create_rectangle(0, hs/1.5, 0, hs/2, width=0, fill="white", tags="ProgressBar")

    def StartDownload():
        while True:
            try:
                can.delete('ProgressBar')
                fill_line = can.create_rectangle(0, hs / 1.5, 0, hs / 2, width=0, fill="white", tags="ProgressBar")
                can.coords(fill_line, (0, hs/1.5, 0, hs/2))
                xa = int(ws * 2.5)
                na = 20/xa
                for t in range(xa):
                    na = na + 300/ws
                    can.coords(fill_line, (0, hs/1.5, na, hs/2))
                    TelaDownload.update()
                    time.sleep(0.1)
            except:
                break


    download = Thread(target=StartDownload)
    download.start()

    LetraX = int(ws / 3.7)
    LetraY = int(hs / 2.5)
    TamanhoLetra = int(ws / 113.8)
    mensagemDownload = "Estamos fazendo o download da atualização!"
    can.create_text(LetraX, LetraY, text=mensagemDownload,
                        font=('Arial', TamanhoLetra, 'bold'), fill="white")

    def DownloadItem(TelaDownload):
        ASADMIN = 'asadmin'
        #try:
        if sys.argv[-1] != ASADMIN:
            script = os.path.abspath(sys.argv[0])
            params = ' '.join([script] + sys.argv[1:] + [ASADMIN])
            try:
                shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)
                pid = os.getpid()
                si = subprocess.STARTUPINFO()
                si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                subprocess.call('taskkill /F /PID ' + str(pid), startupinfo=si)
            except:
                pid = os.getpid()
                si = subprocess.STARTUPINFO()
                si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                subprocess.call('taskkill /F /PID ' + str(pid), startupinfo=si)
        try:
            os.mkdir(dir_path + "\\update\\")
        except:
            pass
        time.sleep(3)
        urllib.request.urlretrieve("http://54.39.68.176/"+jsonUpdate["ArquivoName"], dir_path + "\\update\\"+jsonUpdate["ArquivoName"])
        subprocess.Popen(dir_path + "\\update\\"+jsonUpdate["ArquivoName"], shell=True)
        pid = os.getpid()
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess.call('taskkill /F /PID ' + str(pid), startupinfo=si)


    down = Thread(target=DownloadItem, args=(TelaDownload,))
    down.start()

    TelaDownload.mainloop()

#Download Circular
class CircularProgressbar(object):
    def __init__(self, canvas, x0, y0, x1, y1, width=2, start_ang=0, full_extent=360):
        self.cur_extent = 0
        self.custom_font = tkFont.Font(family="Helvetica", size=12, weight='bold')
        self.canvas = canvas
        self.x0, self.y0, self.x1, self.y1 = x0+width, y0+width, x1-width, y1-width
        self.tx, self.ty = (x1-x0) / 2, (y1-y0) / 2
        self.width = width
        self.start_ang, self.full_extent = start_ang, full_extent
        # draw static bar outline
        w2 = width / 2
        self.oval_id1 = self.canvas.create_oval(self.x0-w2, self.y0-w2,
                                                self.x1+w2, self.y1+w2)
        self.oval_id2 = self.canvas.create_oval(self.x0+w2, self.y0+w2,
                                                self.x1-w2, self.y1-w2)
        self.running = False

    def start(self, interval=100):
        self.interval = interval
        self.increment = self.full_extent / interval
        self.extent = 0
        self.arc_id = self.canvas.create_arc(self.x0, self.y0, self.x1, self.y1,
                                             start=self.start_ang, extent=self.extent,
                                             width=self.width, style='arc')
        percent = '0%'
        self.label_id = self.canvas.create_text(self.tx, self.ty, text=percent,
                                                font=self.custom_font)
        self.running = True
        self.canvas.after(interval, self.step, self.increment)

    def step(self, delta):
        if self.running:
            self.cur_extent = (self.cur_extent + delta) % 360
            self.canvas.itemconfigure(self.arc_id, extent=self.cur_extent)
            percent = '{:.0f}%'.format(round(float(self.cur_extent) / self.full_extent * 100))
            self.canvas.itemconfigure(self.label_id, text=percent)

        self.after_id = self.canvas.after(self.interval, self.step, delta)

    def toggle_pause(self):
        self.running = not self.running

try:
    ASADMIN = 'asadmin'
    if sys.argv[-1] != ASADMIN:
        script = os.path.abspath(sys.argv[0])
        params = ' '.join([script] + sys.argv[1:] + [ASADMIN])
        try:
            shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)
            pid = os.getpid()
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.call('taskkill /F /PID ' + str(pid), startupinfo=si)
        except:
            pid = os.getpid()
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.call('taskkill /F /PID ' + str(pid), startupinfo=si)
    regValueInstall = reg.read_value(path, 'File Cache Path')
    if regValueInstall["data"]:

        def SaveImageCopy():
            try:
                shutil.copyfile(dir_path+"\\media\\background.png", regValueInstall["data"]+"\\..\\..\\MTA\\cgui\\images\\background.png")
                shutil.copyfile(dir_path + "\\media\\background_logo.png", regValueInstall["data"] + "\\..\\..\\MTA\\cgui\\images\\background_logo.png")
                shutil.copyfile(dir_path + "\\media\\latest_news.png", regValueInstall["data"] + "\\..\\..\\MTA\\cgui\\images\\latest_news.png")
            except:
                pass

        ThdSaveImage = Thread(target=SaveImageCopy)
        ThdSaveImage.start()

        TelaPrincipal = Tk()
        TelaPrincipal.title(NomeDoServidor)
        TelaPrincipal["borderwidth"] = 0
        TelaPrincipal.resizable(0, 0)
        TelaPrincipal.iconbitmap(dir_path+"\\media\\logo.ico")
        TelaPrincipal.overrideredirect(True)
        TelaPrincipal.wm_attributes("-transparentcolor", "gray")
        TelaPrincipal.bind("<Escape>", lambda e: e.widget.quit())
        TelaPrincipal.focus_set()
        ws = TelaPrincipal.winfo_screenwidth()
        hs = TelaPrincipal.winfo_screenheight()
        wid = ws/1.824
        hei = hs/1.706
        TelaPrincipal.wm_attributes("-topmost", True)
        TelaPrincipal.config(bg=None)
        x = (ws/2) - (wid/2)
        y = (hs/2) - (hei/2)
        TelaPrincipal.geometry('%dx%d+%d+%d' % (wid, hei, x, y))


        """def ManimizeJanelaThread(TelaPrincipal, NomeDoServidor):
            AntesisMaximized = None
            AntesisMinimized = None
            while True:
                window = pygetwindow.getWindowsWithTitle(NomeDoServidor)[0]
                try:
                    if (AntesisMinimized != window.isMinimized):
                        if window.isMinimized == True:
                            AntesisMinimized = window.isMinimized
                            TelaPrincipal.overrideredirect(False)
                            TelaPrincipal.wm_attributes("-topmost", False)
                    if (AntesisMaximized != window.isMaximized):
                        if window.isMaximized == False:
                            AntesisMaximized = window.isMaximized
                            TelaPrincipal.overrideredirect(True)
                            TelaPrincipal.wm_attributes("-topmost", True)
                except:
                    pass
                time.sleep(0.1)


        JanelaThread = Thread(target=ManimizeJanelaThread, args=(TelaPrincipal, NomeDoServidor,))
        JanelaThread.start()"""

        def Iniciar_Music():
            playsound(dir_path + '\\media\\music.mp3')

        startMusic = Thread(target=Iniciar_Music)
        startMusic.start()

        def ClosePrograma(event):
            pid = os.getpid()
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.call('taskkill /F /PID '+str(pid), startupinfo=si)

        def Abrir_Discord(event):
            webbrowser.open(inf["discord"])

        def Abrir_Instagram(event):
            webbrowser.open(inf["instagram"])

        def Abrir_Servidor(event):
            webbrowser.open("mtasa://"+inf["ip_mtasa"]+":"+inf["porta_mtasa"])
            pid = os.getpid()
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.call('taskkill /F /PID '+str(pid), startupinfo=si)

        def BTNMaximized(event):
            window = pygetwindow.getWindowsWithTitle(NomeDoServidor)[0]
            window.minimize()


        can = Canvas(TelaPrincipal, width=wid, height=hei, bg='gray', bd=0, highlightthickness=0, relief='ridge')
        can.grid()

        def check_hand_enter():
            can.config(cursor="hand2")

        def check_hand_leave():
            can.config(cursor="")

        def OpenConfig(event):
            Config = Tk()
            Config.title(NomeDoServidor + ' - Servidor de MTA')
            Config["borderwidth"] = 0
            Config.resizable(0, 0)
            Config.overrideredirect(True)
            Config.wm_attributes("-transparentcolor", "gray")
            Config.bind("<Escape>", lambda e: e.widget.quit())
            Config.focus_set()
            ws2 = Config.winfo_screenwidth()
            hs2 = Config.winfo_screenheight()
            wid2 = ws / 4.824
            hei2 = hs / 6
            Config.wm_attributes("-topmost", True)
            Config.config(bg=None)
            x2 = (ws2 / 2) - (wid2 / 2)
            y2 = (hs2 / 2) - (hei2 / 2)
            Config.geometry('%dx%d+%d+%d' % (wid2, hei2, x2, y2))
            canConfig = Canvas(Config, width=wid2, height=hei2, bg='#2d2d2d', bd=0, highlightthickness=0, relief='ridge')
            canConfig.grid()

            def check_hand_enter():
                canConfig.config(cursor="hand2")

            def check_hand_leave():
                canConfig.config(cursor="")

            def CloseConfig(event):
                Config.destroy()

            def Limpar_cache(event):
                reg = Reg()
                path = r'HKLM\SOFTWARE\WOW6432Node\Multi Theft Auto: San Andreas All\Common'
                regValueInstall = reg.read_value(path, 'File Cache Path')
                path = regValueInstall["data"]+"\\resources"
                path = regValueInstall["data"]+"\\resources"
                shutil.rmtree(path)
                os.mkdir(path)
                try:
                    from win10toast import ToastNotifier
                    toaster = ToastNotifier()
                    toaster.show_toast(NomeDoServidor + " - Sucesso", "Cachê limpo com sucesso!", icon_path=dir_path + '\\media\\logo.ico')

                except:
                    a = False
                pid = os.getpid()
                si = subprocess.STARTUPINFO()
                si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                subprocess.call(dir_path + '\\Brasil Sao Paulo RP.exe', startupinfo=si)
                subprocess.call('taskkill /F /PID ' + str(pid), startupinfo=si)

            CloseX2 = int(ws2 / 45.5)
            CloseY2 = int(hs2 / 25.6)
            Close2 = ImageTk.PhotoImage(
                Image.open(dir_path + "\\media\\close.png").resize((CloseX2, CloseY2), Image.ANTIALIAS), master=Config)
            CloseBtn2 = canConfig.create_image(ws2 / 5.3, hs2 /28, image=Close2, tags="CloseBtn2")
            canConfig.tag_bind(CloseBtn2, "<Enter>", lambda event: check_hand_enter())
            canConfig.tag_bind(CloseBtn2, "<Leave>", lambda event: check_hand_leave())
            canConfig.tag_bind(CloseBtn2, "<Button-1>", CloseConfig)
            canConfig.tag_bind(CloseBtn2, "<Key>", CloseConfig)

            ImgLimparCacheX = int(ws2 / 6.83)
            ImgLimparCacheY = int(hs2 / 12.8)

            ImgLimparCache = ImageTk.PhotoImage(
                Image.open(dir_path + '\\media\\ButtonLimparCache.png').resize((ImgLimparCacheX, ImgLimparCacheY), Image.ANTIALIAS), master=Config)
            ButtonLimparCache = canConfig.create_image(ws /9.7, hs / 10.5, image=ImgLimparCache, tags="ButtonLimparCache")
            canConfig.tag_bind(ButtonLimparCache, "<Enter>", lambda event: check_hand_enter())
            canConfig.tag_bind(ButtonLimparCache, "<Leave>", lambda event: check_hand_leave())
            canConfig.tag_bind(ButtonLimparCache, "<Button-1>", Limpar_cache)
            canConfig.tag_bind(ButtonLimparCache, "<Key>", Limpar_cache)


            Config.mainloop()




        image1 = ImageTk.PhotoImage(Image.open(dir_path+"\\media\\1bg.png").resize((ws, hs), Image.ANTIALIAS))
        can.create_image(x, y, image=image1)

        CloseX = int(ws/34.2)
        CloseY = int(hs/19.2)
        Close = ImageTk.PhotoImage(Image.open(dir_path+"\\media\\close.png").resize((CloseX, CloseY), Image.ANTIALIAS))
        CloseBtn = can.create_image(ws/1.9, hs/30, image=Close, tags="CloseBtn")
        can.tag_bind(CloseBtn, "<Enter>", lambda event: check_hand_enter())
        can.tag_bind(CloseBtn, "<Leave>", lambda event: check_hand_leave())
        can.tag_bind(CloseBtn, "<Button-1>", ClosePrograma)
        can.tag_bind(CloseBtn, "<Key>", ClosePrograma)

        engrenagemX = int(ws / 36.2)
        engrenagemY = int(hs / 21.2)
        engrenagem = ImageTk.PhotoImage(
            Image.open(dir_path + "\\media\\engrenagem.png").resize((engrenagemX, engrenagemY), Image.ANTIALIAS))
        engrenagemBtn = can.create_image(ws / 2.03, hs / 30.5, image=engrenagem, tags="engrenagemBtn")
        can.tag_bind(engrenagemBtn, "<Enter>", lambda event: check_hand_enter())
        can.tag_bind(engrenagemBtn, "<Leave>", lambda event: check_hand_leave())
        can.tag_bind(engrenagemBtn, "<Button-1>", OpenConfig)
        can.tag_bind(engrenagemBtn, "<Key>", OpenConfig)

        """minimizedX = int(ws / 36.2)
        minimizedY = int(hs / 21.2)
        minimized = ImageTk.PhotoImage(
            Image.open(dir_path + "\\media\\Minimize.png").resize((minimizedX, minimizedY), Image.ANTIALIAS))
        minimizedBtn = can.create_image(ws / 2.18, hs / 30.5, image=minimized, tags="minimizedBtn")
        can.tag_bind(minimizedBtn, "<Enter>", lambda event: check_hand_enter())
        can.tag_bind(minimizedBtn, "<Leave>", lambda event: check_hand_leave())
        can.tag_bind(minimizedBtn, "<Button-1>", BTNMaximized)
        can.tag_bind(minimizedBtn, "<Key>", BTNMaximized)"""


        ImgLogoX = int(ws/5.464)
        ImgLogoY = int(hs/3.072)
        img = Image.open(dir_path + '\\media\\logo.png')
        img = img.resize((ImgLogoX, ImgLogoY), Image.ANTIALIAS)
        Imgimage = ImageTk.PhotoImage(img)
        can.create_image(ws/3.7, hs/5, image=Imgimage)


        ImgButtonX = int(ws/6.83)
        ImgButtonY = int(hs/12.8)

        ImgButtonInstagram = ImageTk.PhotoImage(Image.open(dir_path + '\\media\\AbrirInstagram.png').resize((ImgButtonX, ImgButtonY), Image.ANTIALIAS))
        ButtonInstagram = can.create_image(ws/9.3, hs/1.9, image=ImgButtonInstagram, tags="ButtonInstagram")
        can.tag_bind(ButtonInstagram, "<Enter>", lambda event: check_hand_enter())
        can.tag_bind(ButtonInstagram, "<Leave>", lambda event: check_hand_leave())
        can.tag_bind(ButtonInstagram, "<Button-1>", Abrir_Instagram)
        can.tag_bind(ButtonInstagram, "<Key>", Abrir_Instagram)

        ImgButton = ImageTk.PhotoImage(Image.open(dir_path + '\\media\\jogarAgr.png').resize((ImgButtonX, ImgButtonY), Image.ANTIALIAS))
        Button = can.create_image(ws/3.70, hs/1.9, image=ImgButton, tags="Button")
        can.tag_bind(Button, "<Enter>", lambda event: check_hand_enter())
        can.tag_bind(Button, "<Leave>", lambda event: check_hand_leave())
        can.tag_bind(Button, "<Button-1>", Abrir_Servidor)
        can.tag_bind(Button, "<Key>", Abrir_Servidor)

        ImgButtonDiscord = ImageTk.PhotoImage(Image.open(dir_path + '\\media\\AbrirDiscord.png').resize((ImgButtonX, ImgButtonY), Image.ANTIALIAS))
        ButtonDiscord = can.create_image(ws/2.3, hs/1.9, image=ImgButtonDiscord, tags="ButtonDiscord")
        can.tag_bind(ButtonDiscord, "<Enter>", lambda event: check_hand_enter())
        can.tag_bind(ButtonDiscord, "<Leave>", lambda event: check_hand_leave())
        can.tag_bind(ButtonDiscord, "<Button-1>", Abrir_Discord)
        can.tag_bind(ButtonDiscord, "<Key>", Abrir_Discord)

        LetraX = int(ws/3.7)
        LetraY = int(hs/2.5)
        try:
            s = Server(inf["ip_mtasa"], int(inf["porta_mtasa"]))
            TamanhoLetra = int(ws/113.8)
            can.create_text(LetraX, LetraY, text=s.players+"/"+s.maxplayers+" Cidadãos Online (Agora)", font=('Arial', TamanhoLetra, 'bold'), fill="white")
        except:
            TamanhoLetra = int(ws/113.8)
            can.create_text(LetraX, LetraY, text="Não conseguimos pegar as informações!",
                            font=('Arial', TamanhoLetra, 'bold'), fill="white")
        TelaPrincipal.mainloop()

except:
    TelaDownload = Tk()
    TelaDownload.title(NomeDoServidor + ' - Download')
    TelaDownload["borderwidth"] = 0
    TelaDownload.resizable(0, 0)
    TelaDownload.overrideredirect(True)
    TelaDownload.wm_attributes("-transparentcolor", "gray")
    TelaDownload.bind("<Escape>", lambda e: e.widget.quit())
    TelaDownload.focus_set()
    ws = TelaDownload.winfo_screenwidth()
    hs = TelaDownload.winfo_screenheight()
    wid = ws / 1.824
    hei = hs / 1.706
    #TelaDownload.wm_attributes("-topmost", True)
    TelaDownload.config(bg=None)
    x = (ws / 2) - (wid / 2)
    y = (hs / 2) - (hei / 2)
    TelaDownload.geometry('%dx%d+%d+%d' % (wid, hei, x, y))

    can = Canvas(TelaDownload, width=wid, height=hei, bg='gray', bd=0, highlightthickness=0, relief='ridge')
    can.grid()

    image1 = ImageTk.PhotoImage(Image.open(dir_path + "\\media\\1bg.png").resize((ws, hs), Image.ANTIALIAS))
    can.create_image(x, y, image=image1)


    def ClosePrograma(event):
        pid = os.getpid()
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess.call('taskkill /F /PID ' + str(pid), startupinfo=si)


    def check_hand_enter():
        can.config(cursor="hand2")


    def check_hand_leave():
        can.config(cursor="")

    CloseX = int(ws / 34.2)
    CloseY = int(hs / 19.2)
    Close = ImageTk.PhotoImage(
        Image.open(dir_path + "\\media\\close.png").resize((CloseX, CloseY), Image.ANTIALIAS))
    CloseBtn = can.create_image(ws / 1.9, hs / 30, image=Close, tags="CloseBtn")
    can.tag_bind(CloseBtn, "<Enter>", lambda event: check_hand_enter())
    can.tag_bind(CloseBtn, "<Leave>", lambda event: check_hand_leave())
    can.tag_bind(CloseBtn, "<Button-1>", ClosePrograma)
    can.tag_bind(CloseBtn, "<Key>", ClosePrograma)

    ImgLogoX = int(ws / 5.464)
    ImgLogoY = int(hs / 3.072)
    img = Image.open(dir_path + '\\media\\logo.png')
    img = img.resize((ImgLogoX, ImgLogoY), Image.ANTIALIAS)
    Imgimage = ImageTk.PhotoImage(img)
    can.create_image(ws / 3.7, hs / 5, image=Imgimage)

    fill_line = can.create_rectangle(0, hs/1.5, 0, hs/2, width=0, fill="white", tags="ProgressBar")

    def StartDownload():
        while True:
            try:
                can.delete('ProgressBar')
                fill_line = can.create_rectangle(0, hs / 1.5, 0, hs / 2, width=0, fill="white", tags="ProgressBar")
                can.coords(fill_line, (0, hs/1.5, 0, hs/2))
                xa = int(ws * 2.5)
                na = 20/xa
                for t in range(xa):
                    na = na + 300/ws
                    can.coords(fill_line, (0, hs/1.5, na, hs/2))
                    TelaDownload.update()
                    time.sleep(0.1)
            except:
                break


    download = Thread(target=StartDownload)
    download.start()

    LetraX = int(ws / 3.7)
    LetraY = int(hs / 2.5)
    TamanhoLetra = int(ws / 113.8)
    mensagemDownload = "Estamos fazendo o download dos modulos!"
    MensagemDownloadItem = can.create_text(LetraX, LetraY, text=mensagemDownload,
                        font=('Arial', TamanhoLetra, 'bold'), fill="white")

    def DownloadItem(Terminatedown, can, MensagemDownloadItem):
        ASADMIN = 'asadmin'
        #try:
        if sys.argv[-1] != ASADMIN:
            script = os.path.abspath(sys.argv[0])
            params = ' '.join([script] + sys.argv[1:] + [ASADMIN])
            try:
                shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)
                pid = os.getpid()
                si = subprocess.STARTUPINFO()
                si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                subprocess.call('taskkill /F /PID ' + str(pid), startupinfo=si)
            except:
                pid = os.getpid()
                si = subprocess.STARTUPINFO()
                si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                subprocess.call('taskkill /F /PID ' + str(pid), startupinfo=si)
        can.itemconfigure(MensagemDownloadItem, text="Fazendo download do Multi Theft Auto!")
        urllib.request.urlretrieve("http://54.39.68.176/mtaSystem.zip", dir_path + "\\mtaSystem\\mtaSystem.zip")
        can.itemconfigure(MensagemDownloadItem, text="Fazendo download do Grand Theft Auto!")
        urllib.request.urlretrieve("http://54.39.68.176/GTA.zip", dir_path + "\\GTA\\GTA.zip")
        Terminatedown = True
        if Terminatedown == True:
            can.itemconfigure(MensagemDownloadItem, text="Download Concluido, Estamos instalando as dependências!")
            try:
                zf = ZipFile(dir_path + '/mtaSystem/mtaSystem.zip', 'r')
                zf.extractall(dir_path + '/mtaSystem/')
                zf.close()
            except:
                a = False

            try:
                zf0 = ZipFile(dir_path + '/GTA/GTA.zip', 'r')
                zf0.extractall(dir_path + '/GTA/')
                zf0.close()
            except:
                a = False

            try:
                os.remove(dir_path+"\\mtaSystem\\mtaSystem.zip")
                os.remove(dir_path+"\\GTA\\GTA.zip")
            except:
                a = False
            try:
                reg.create_key("HKCR\\mtasa")
            except:
                a = False
            try:
                reg.create_key("HKCR\\mtasa\\DefaultIcon")
            except:
                a = False
            try:
                reg.create_key("HKCR\\mtasa\\shell")
            except:
                a = False
            try:
                reg.create_key("HKCR\\mtasa\\shell\\open")
            except:
                a = False
            try:
                reg.create_key("HKCR\\mtasa\\shell\\open\\command")
            except:
                a = False


            try:
                reg.create_key("HKCU\\SOFTWARE\\Classes\\mtasa")
            except:
                a = False
            try:
                reg.create_key("HKCU\\SOFTWARE\\Classes\\mtasa\\DefaultIcon")
            except:
                a = False
            try:
                reg.create_key("HKCU\\SOFTWARE\\Classes\\mtasa\\shell")
            except:
                a = False
            try:
                reg.create_key("HKCU\\SOFTWARE\\Classes\\mtasa\\shell\\open")
            except:
                a = False
            try:
                reg.create_key("HKCU\\SOFTWARE\\Classes\\mtasa\\shell\\open\\command")
            except:
                a = False



            try:
                reg.create_key('HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All')
            except:
                a = False
            try:
                reg.create_key('HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5')
            except:
                a = False
            try:
                
                reg.create_key('HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\Common')
            except:
                a = False
            try:
                reg.create_key('HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings')
            except:
                a = False
            try:
                reg.create_key('HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\diagnostics')
            except:
                a = False
            try:
                reg.create_key('HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\general')
            except:
                a = False

            try:
                reg.write_value("HKCR\\mtasa", 'URL:MTA San Andreas Protocol', '', 'REG_SZ')
            except:
                a = False

            try:
                reg.write_value("HKCR\\mtasa", 'URL Protocol', '', 'REG_SZ')
            except:
                a = False

            try:
                reg.write_value("HKCR\\mtasa\\DefaultIcon", '', dir_path + '\\mtaSystem\\Multi Theft Auto.exe, 0', 'REG_SZ')
            except:
                a = False

            try:
                reg.write_value("HKCR\\mtasa\\shell\\open\\command", '', '"' + dir_path + '\\mtaSystem\\Multi Theft Auto.exe"%1',
                            'REG_SZ')
            except:
                a = False

            try:
                reg.write_value("HKCU\\SOFTWARE\\Classes\\mtasa", 'URL:MTA San Andreas Protocol', '', 'REG_SZ')
            except:
                a = False

            try:
                reg.write_value("HKCU\\SOFTWARE\\Classes\\mtasa", 'URL Protocol', '', 'REG_SZ')
            except:
                a = False

            try:
                reg.write_value("HKCU\\SOFTWARE\\Classes\\mtasa\\DefaultIcon", '', dir_path + '\\mtaSystem\\Multi Theft Auto.exe, 0',
                                'REG_SZ')
            except:
                a = False

            try:
                reg.write_value("HKCU\\SOFTWARE\\Classes\\mtasa\\shell\\open\\command", '',
                                '"' + dir_path + '\\mtaSystem\\Multi Theft Auto.exe"%1',
                                'REG_SZ')
            except:
                a = False

            try:
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5", "Installer Language",
                            "1046", 'REG_SZ')
            except:
                a = False

            try:
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5", "Last Install Location",
                            dir_path + "\\mtaSystem", "REG_SZ")
            except:
                a = False

            try:
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5", "Last Run Location",
                            dir_path + "\\mtaSystem", "REG_SZ")
            except:
                a = False

            try:
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5", "Last Run Path",
                            dir_path + "\\mtaSystem\\Multi Theft Auto.exe", "REG_SZ")
            except:
                a = False

            try:
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5", "Last Run Path Hash",
                            "84B788AB9D9DF9A35227D7B693983078", "REG_SZ")
            except:
                a = False

            try:
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5", "Last Run Path Version",
                            "1.5", "REG_SZ")
            except:
                a = False

            try:
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5", "OnQuitCommand", "",
                            "REG_SZ")
            except:
                a = False

            try:
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5", "OnRestartCommand",
                            "1.5.8-9.20743", "REG_SZ")
            except:
                a = False

            try:
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5", "PostUpdateConnect",
                            "host=&time=1607459825", "REG_SZ")
            except:
                a = False

            try:
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5", "Last Run Location",
                            dir_path + "\\mtaSystem", "REG_SZ")
            except:
                a = False

            try:
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\Common", "File Cache Path",
                            dir_path + "\\mtaSystem\\mods\\deathmatch", "REG_SZ")
            except:
                a = False

            try:
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\Common", "GTA:SA Path",
                            dir_path + "\\GTA", "REG_SZ")
            except:
                a = False

            try:
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\diagnostics",
                            "bsod-detect-skip", "", "REG_SZ")
            except:
                a = False

            try:
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\diagnostics",
                            "crash-data", "", "REG_SZ")

                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\diagnostics",
                                "createdevice-last-status", "3", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\diagnostics",
                                "d3dlegacy", "373", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\diagnostics",
                                "d3dver", "1", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\diagnostics",
                                "debug-setting", "none", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\diagnostics",
                                "game-begin-time", "", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\diagnostics",
                                "game-connect-time", "0", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\diagnostics",
                                "gta-fopen-fail", "", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\diagnostics",
                                "gta-fopen-last", "", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\diagnostics",
                                "gta-model-fail", "", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\diagnostics",
                                "gta-upgrade-fail", "", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\diagnostics",
                                "img-file-corrupt", "", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\diagnostics",
                                "last-crash-info", "", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\diagnostics",
                                "last-crash-reason", "", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\diagnostics",
                                "last-dump-extra", "added-anim-task", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\diagnostics",
                                "last-dump-save", "", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\diagnostics",
                                "last-dump-extra", "2020-11-16 23:52:08", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\diagnostics",
                                "last-sys-dump-time", "01d6bc73-7e867192", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\diagnostics",
                                "num-minidump-detected", "1", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\diagnostics",
                                "preloading-upgrades-hiscore", "1194", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\diagnostics",
                                "send-dumps", "yes", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\general",
                                "admin2user_comms", "_argc=1&_pc_label=appcompat_end:&_pc_offset=2", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\general",
                                "aero-changeable", "1", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\general",
                                "aero-enabled", "1", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\general",
                                "bsod-markers", "#00#00#00#00#00#00#00dne#00", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\general",
                                "cachechecksum", "A43B7F1644B0364ECCGB1BC:E96G38F417:FB352C3D5E263D1CAE1B7D911CEBC",
                                "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\general",
                                "customized-sa-files-request", "0", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\general",
                                "customized-sa-files-show", "0", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\general",
                                "customized-sa-files-using", "0", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\general",
                                "debugfilter", "", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\general",
                                "device-selection-disabled", "0", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\general",
                                "gta-exe-md5", "170B3A9108687B26DA2D8901C6948A18", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\general",
                                "is-admin", "0", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\general",
                                "last-server-ip", "1", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\general",
                                "last-server-port", "22143", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\1.5\\Settings\\general",
                                "last-server-time", "1607459936", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\general",
                                "locale", "pt_BR", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\general",
                                "mta-version-ext", "1.5.8-9.20743.0.000", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\general",
                                "news-install", "", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\general",
                                "news-updated", "1", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\general",
                                "noav-last-asked-time", "444764", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\general",
                                "noav-user-says-skip", "1", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\general",
                                "no-cycle-event-log", "0", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\general",
                                "os-version", "6.2", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\general",
                                "pending-browse-to-solution", "", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\general",
                                "real-os-build", "19041", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\general",
                                "real-os-version", "10.0", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\general",
                                "reportsettings", "", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\\general",
                                "serial", "", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\general",
                                "times-connected", "928", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\general",
                                "times-connected-editor", "53", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\general",
                                "trouble-url",
                                "http://updatesa.multitheftauto.com/sa/trouble/?v=%VERSION%&id=%ID%&tr=%TROUBLE%", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\general",
                                "Win8Color16", "0", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\general",
                                "Win8MouseFix", "0", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\nvhacks",
                                "optimus", "0", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\nvhacks",
                                "optimus-alt-startup", "0", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\nvhacks",
                                "optimus-export-enablement", "0", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\nvhacks",
                                "optimus-force-windowed", "0", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\nvhacks",
                                "optimus-rename-exe", "0", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\watchdog", "CR1",
                                "0", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\watchdog", "CR2",
                                "0", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\watchdog", "CR3",
                                "0", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\watchdog", "L0",
                                "1", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\watchdog", "L1",
                                "0", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\watchdog", "L2",
                                "0", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\watchdog", "L3",
                                "0", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\watchdog", "L4",
                                "0", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\watchdog", "L5",
                                "0", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\watchdog",
                                "lastruncrash", "0", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\watchdog",
                                "preload-upgrades", "0", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\watchdog", "Q0",
                                "1", "REG_SZ")
                reg.write_value("HKLM\\SOFTWARE\\WOW6432Node\\Multi Theft Auto: San Andreas All\\1.5\\Settings\\watchdog",
                                "uncleanstop", "0", "REG_SZ")
            except:
                a = False

            pid = os.getpid()
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.call(dir_path+'\\Brasil Sao Paulo RP.exe', startupinfo=si)
            subprocess.call('taskkill /F /PID ' + str(pid), startupinfo=si)


    Terminatedown = False
    down = Thread(target=DownloadItem, args=(Terminatedown,can,MensagemDownloadItem,))
    down.start()

    TelaDownload.mainloop()