import os
import shutil
import sys
import pysrt
import datetime
import webbrowser
import cv2
import numpy as np
import mediapipe as mdp
import pyautogui
import time
import youtube_dl
import instaloader
import requests
import string
import face_recognition
import tempfile
import threading
from bs4 import BeautifulSoup

import self as self
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import *
import moviepy.editor as mp

import PIL
from PIL import Image

import image_file
from tkinter import *
from tkinter import messagebox
from tkinter import messagebox as mbox
from tkinter.messagebox import askokcancel
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import *
from tkinter import filedialog

from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from rembg import remove

import speech_recognition as sr
from gtts import gTTS
from rich import palette

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt, QUrl, QTime, QTimer, QThread, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QIcon, QKeySequence, QFont, QPixmap, QImage
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QSlider, QFileDialog, QStyle, QLabel, QAction, \
    QSizePolicy, QWidget, QGridLayout, QLineEdit, QComboBox, QMessageBox, QRadioButton, QProgressBar, QListWidget, \
    QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox

# Untuk Compress Size Image
from PIL import Image

# Untuk Spotify Downloader
# Variabel
CWD = os.getcwd()
LOCATION = os.path.join(CWD,'MUSIC')
if os.path.isdir(LOCATION)==False:
    os.mkdir(LOCATION)


# Fungsi
def get_ID(session, id):
    LINK = f'https://api.spotifydown.com/getId/{id}'
    headers = {
        'authority': 'api.spotifydown.com',
        'method': 'GET',
        'path': f'/getId/{id}',
        'origin': 'https://spotifydown.com',
        'referer': 'https://spotifydown.com/',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-fetch-mode': 'cors',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }
    response = session.get(url=LINK, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    return None


def generate_Analyze_id(session, yt_id):
    DL = 'https://corsproxy.io/?https://www.y2mate.com/mates/analyzeV2/ajax'
    data = {
        'k_query': f'https://www.youtube.com/watch?v={yt_id}',
        'k_page': 'home',
        'hl': 'en',
        'q_auto': 0,
    }
    headers = {
        'authority': 'corsproxy.io',
        'method': 'POST',
        'path': '/?https://www.y2mate.com/mates/analyzeV2/ajax',
        'origin': 'https://spotifydown.com',
        'referer': 'https://spotifydown.com/',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-fetch-mode': 'cors',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                      '537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }
    RES = session.post(url=DL, data=data, headers=headers)
    if RES.status_code == 200:
        return RES.json()
    return None


def generate_Conversion_id(session, analyze_yt_id, analyze_id):
    DL = 'https://corsproxy.io/?https://www.y2mate.com/mates/convertV2/index'
    data = {
        'vid': analyze_yt_id,
        'k': analyze_id,
    }
    headers = {
        'authority': 'corsproxy.io',
        'method': 'POST',
        'path': '/?https://www.y2mate.com/mates/analyzeV2/ajax',
        'origin': 'https://spotifydown.com',
        'referer': 'https://spotifydown.com/',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-fetch-mode': 'cors',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                      '537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }

    RES = session.post(url=DL, data=data, headers=headers)
    if RES.status_code == 200:
        return RES.json()
    return None


def returnSPOT_ID(link):
    return link.split('/')[-1].split('?si')[0]


class LisensiKey(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Pilih Lisensi Key')
        self.setGeometry(800, 400, 400, 120)
        # Fix Size
        self.setFixedSize(400, 120)
        self.setWindowIcon(QtGui.QIcon(':/Logo.png'))
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)

        central_widget = QWidget()
        layout = QVBoxLayout()

        label = QLabel('Silahkan Pilih Lisensi Key Yang Anda Ingin Kan !')
        # Size Font dan agak ke tengah
        label.setFont(QFont('Arial', 12))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)


        button_teks = QPushButton('Teks')
        # Button Resize
        button_teks.setFixedSize(380, 25)
        button_teks.clicked.connect(self.handle_teks)
        layout.addWidget(button_teks)

        button_mendeteksi_wajah = QPushButton('Mendeteksi Wajah')
        # Button Resize
        button_mendeteksi_wajah.setFixedSize(380, 25)
        button_mendeteksi_wajah.clicked.connect(self.handle_mendeteksi_wajah)
        layout.addWidget(button_mendeteksi_wajah)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def handle_teks(self):
        self.lisensi_key = TextLisensiKey()
        self.lisensi_key.show()
        self.close()

    def handle_mendeteksi_wajah(self):
        self.face_recognition_window = FaceRecognitionLisensiKey()
        self.face_recognition_window.show()
        self.close()


class TextLisensiKey(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Lisensi Key Pemutar Media'
        self.left = 500
        self.top = 150
        self.width = 520
        self.height = 75
        self.setFixedSize(self.width, self.height)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QtGui.QIcon(':/Logo.png'))

        self.label = QLabel(self)
        self.label.setText('Lisensi Key: ')
        self.label.move(30, 30)

        self.textbox = QLineEdit(self)
        self.textbox.move(120, 20)
        self.textbox.resize(280, 30)

        self.lisensiButton = QPushButton('Cek Lisensi Key', self)
        self.lisensiButton.move(420, 20)
        self.lisensiButton.resize(85, 30)
        # self.lisensiButton.setShortcut(QKeySequence("Ctrl+L"))  # menambahkan shortcut Ctrl+L
        self.lisensiButton.clicked.connect(self.cek_lisensi_key)

        self.show()

    @pyqtSlot()
    def cek_lisensi_key(self):
        lisensi_key = 'Ahmad Bujai Rimi', 'UEU Teknik Informatika 2019'
        #if self.textbox.text() in lisensi_key:
        if self.textbox.text() == lisensi_key[0] or self.textbox.text() == lisensi_key[1]:
            mbox.showinfo('Lisensi Key', 'Lisensi Key sudah masuk')
            self.close()
            # Masuk Ke Class Window(QMainWindow)
            self.window = Window()
            self.window.show()
        else:
            mbox.showinfo('Lisensi Key', 'Lisensi Key belum masuk')
            self.close()
            self.lisensi_key = LisensiKey()
            self.lisensi_key.show()


class FaceRecognitionLisensiKey(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Mendeteksi Wajah Untuk Lisensi Key')
        self.setWindowIcon(QtGui.QIcon(':/Logo.png'))
        self.setGeometry(100, 100, 662, 500)
        # Fix Size
        self.setFixedSize(self.size())
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)

        self.init_ui()

        self.target_face = cv2.imread('foto/foto5.jpg')
        self.target_face_encoding = self.get_face_encoding(self.target_face)
        self.start_time = None

    def init_ui(self):
        self.image_label = QLabel(self)
        self.image_label.setGeometry(10, 10, 640, 480)
        self.start_button = QPushButton('Start', self)
        self.start_button.setGeometry(520, 410, 100, 40)
        self.start_button.clicked.connect(self.start)

    def start(self):
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(20)
        self.start_time = time.time()

    def update_frame(self):
        ret, frame = self.cap.read()

        face_found = False
        face_encodings = self.get_face_encodings(frame)
        for encoding in face_encodings:
            if self.compare_faces(self.target_face_encoding, encoding):
                face_found = True
                self.timer.stop()
                self.cap.release()
                QMessageBox.information(self, 'Muka Terdeteksi',
                                        'Selamat Muka Anda Terdeteksi Sebagai Lisensi Media Player')
                self.close()
                self.window = Window()
                self.window.show()
                break

        if not face_found and time.time() - self.start_time >= 10:
            self.timer.stop()
            self.cap.release()
            QMessageBox.warning(self, 'Muka Tidak Terdeteksi',
                                'Mohon Maaf Muka Anda Tidak Terdaftar Dalam Aplikasi Ini')
            self.close()
            self.lisensi_key = LisensiKey()
            self.lisensi_key.show()

        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(image))

    def get_face_encoding(self, image):
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        face_encodings = face_recognition.face_encodings(rgb_image)
        return face_encodings[0] if face_encodings else None

    def get_face_encodings(self, image):
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return face_recognition.face_encodings(rgb_image)

    def compare_faces(self, face1_encoding, face2_encoding):
        if face1_encoding is None or face2_encoding is None:
            return False
        return face_recognition.compare_faces([face1_encoding], face2_encoding, tolerance=0.6)[0]


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.videoWidget = QVideoWidget()
        self.setWindowTitle("Pemutar Media Sederhana (Coded By: Enjay)")
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)

        self.setGeometry(100, 100, 800, 600)
        #self.setStyleSheet("background-color: Black; color: red; font-weight: bold; border: 2px solid red; border-radius: 10px;"
        #                   "padding: 5px; border-width: 2px; selection-color: black;selection-background-color: red;")

        p = self.palette()
        p.setColor(self.backgroundRole(), QtCore.Qt.black)
        self.setPalette(p)

        self.setWindowIcon(QtGui.QIcon(':/Logo.png'))

        # Create Media Player Object
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.playlist = QMediaPlaylist() # Create Playlist Object
        self.playlist.currentMediaChanged.connect(self.update_label)

        # Create Video Widget Object
        videoWidget = QVideoWidget()

        # Create MenuBar
        main_menu = self.menuBar()
        main_menu.setStyleSheet("background-color: Black; color: red; font-weight: bold; border-radius: 10px; selection-color: black; selection-background-color: red;"
                                "border: 2px solid red; padding: 2px; border-width: 2px; border-style: outset;")

        file_menu = main_menu.addMenu("Dokumen")
        tools_menu = main_menu.addMenu("Alat")
        downloader_menu = main_menu.addMenu("Downloader")
        ai_menu = main_menu.addMenu("AI")
        view_menu = main_menu.addMenu("View")
        help_menu = main_menu.addMenu("Bantuan")

        # Create Open Action
        open_file_action = QAction("Buka File", self)
        open_file_action.setShortcut(QKeySequence("Ctrl+O"))
        open_file_action.setIcon(QIcon("icons/open.png"))
        open_file_action.triggered.connect(self.open_file)

        # Create Open Folder Action
        open_folder_action = QAction("Buka Folder", self)
        open_folder_action.setShortcut(QKeySequence("Ctrl+F"))
        open_folder_action.setIcon(QIcon("icons/folder.png"))
        open_folder_action.triggered.connect(self.open_folder)

        # Create Exit Action
        exit_action = QAction("Keluar", self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.setIcon(QIcon("icons/exit.png"))
        exit_action.triggered.connect(self.exit_app)

        # Create Open Subtitle Action
        open_subtitle_action = QAction("Buka Subtitle", self)
        open_subtitle_action.setShortcut(QKeySequence("Ctrl+S"))
        open_subtitle_action.setIcon(QIcon("icons/subtitle.png"))
        open_subtitle_action.triggered.connect(self.open_subtitle)

        # Sub Menu Tools
        speed_menu = tools_menu.addMenu("Kecepatan Video")
        speed_menu.addAction("Lambat", self.slow_video)
        speed_menu.addAction("Normal", self.normal_video)
        speed_menu.addAction("Cepat", self.fast_video)

        # repeat menu
        repeat_menu = tools_menu.addMenu("Ulangi Video")
        repeat_menu.addAction("Aktifkan", self.video_auto_on)
        repeat_menu.addAction("Matikan", self.video_auto_off)

        # Create Sleep Time
        sleep_time_menu = tools_menu.addMenu("Waktu Tidur")
        sleep_time_menu.addAction("1 Menit", self.sleep_time_1_minute)
        sleep_time_menu.addAction("15 Menit", self.sleep_time_15_minute)
        sleep_time_menu.addAction("30 Menit", self.sleep_time_30_minute)
        sleep_time_menu.addAction("45 Menit", self.sleep_time_45_minute)
        sleep_time_menu.addAction("1 Jam", self.sleep_time_60_minute)
        sleep_time_menu.addAction("Matikan", self.timer_stop)

        # Create ScreenShot Action
        screenshot_action = QAction("Ambil Gambar", self)
        screenshot_action.setShortcut(QKeySequence("Ctrl+P"))
        screenshot_action.setIcon(QIcon("icons/screenshot.png"))
        screenshot_action.triggered.connect(self.screen)

        # Create Hand Gesture Action
        hand_gesture_action = QAction("AI Gerakan Tangan", self)
        hand_gesture_action.setShortcut(QKeySequence("Ctrl+G"))
        hand_gesture_action.setIcon(QIcon("icons/hand.png"))
        hand_gesture_action.triggered.connect(self.hand_gesture)

        # Create Objek Video Action
        objek_video_action = QAction("AI Objek Video", self)
        objek_video_action.setShortcut(QKeySequence("Ctrl+V"))
        objek_video_action.setIcon(QIcon("icons/objek.png"))
        objek_video_action.triggered.connect(self.deteksi_objek_video)

        # Create Objek Foto Action
        objek_foto_action = QAction("AI Objek Foto", self)
        objek_foto_action.setShortcut(QKeySequence("Ctrl+F"))
        objek_foto_action.setIcon(QIcon("icons/objek.png"))
        objek_foto_action.triggered.connect(self.deteksi_objek_foto)

        # Create Objek Kamera Action
        #objek_kamera_action = QAction("AI Objek Kamera", self)
        #objek_kamera_action.setShortcut(QKeySequence("Ctrl+K"))
        #objek_kamera_action.setIcon(QIcon("icons/objek.png"))
        #objek_kamera_action.triggered.connect(self.deteksi_objek_kamera)

        # Create Youtube Downloader Action
        youtube_downloader_action = QAction("Youtube Downloader", self)
        youtube_downloader_action.setShortcut(QKeySequence("Ctrl+Y"))
        youtube_downloader_action.setIcon(QIcon("icons/youtube.png"))
        youtube_downloader_action.triggered.connect(self.youtube_downloader)

        # Create Subtitle Video Downloader Action
        subtitle_video_downloader_action = QAction("Subtitle Video Downloader", self)
        subtitle_video_downloader_action.setShortcut(QKeySequence("Ctrl+D"))
        subtitle_video_downloader_action.setIcon(QIcon("icons/subtitle.png"))
        subtitle_video_downloader_action.triggered.connect(self.subtitle_video_downloader)

        # Create Video Faceboook Downloader Action
        video_facebook_downloader_action = QAction("Video Facebook Downloader", self)
        video_facebook_downloader_action.setShortcut(QKeySequence("Ctrl+F"))
        video_facebook_downloader_action.setIcon(QIcon("icons/facebook.png"))
        video_facebook_downloader_action.triggered.connect(self.video_facebook_downloader)

        # Create Video Instagram Downloader Action
        video_instagram_downloader_action = QAction("Profile Instagram Downloader", self)
        video_instagram_downloader_action.setShortcut(QKeySequence("Ctrl+I"))
        video_instagram_downloader_action.setIcon(QIcon("icons/instagram.png"))
        video_instagram_downloader_action.triggered.connect(self.instagram_downloader)

        # Create Spotify Downloader Action
        spotify_downloader_action = QAction("Spotify Downloader", self)
        spotify_downloader_action.setShortcut(QKeySequence("Ctrl+P"))
        spotify_downloader_action.setIcon(QIcon("icons/spotify.png"))
        spotify_downloader_action.triggered.connect(self.spotify_downloader)

        # Create Remove Image Background Action
        remove_image_background_action = QAction("Hapus Latar Belakang Gambar", self)
        remove_image_background_action.setShortcut(QKeySequence("Ctrl+R"))
        remove_image_background_action.setIcon(QIcon("icons/remove.png"))
        remove_image_background_action.triggered.connect(self.remove_background_foto)

        # Sub Menu Convert Video
        convert_video_menu = tools_menu.addMenu("Konversi Format Video dan Audio")
        convert_video_menu.addAction("Avi To Mp4", self.video_converter_avi_to_mp4)
        convert_video_menu.addAction("Mp4 To Mp3", self.video_converter_mp4_to_mp3)

        # Sub Menu Cut and Combine Video
        cut_and_combine_video_menu = tools_menu.addMenu("Potong dan Gabungkan Video")
        cut_and_combine_video_menu.addAction("Potong Video", self.cut_video)
        cut_and_combine_video_menu.addAction("Gabungkan Video", self.video_combine)

        # Sub Menu Video and Image Converter
        video_converter_menu = ai_menu.addMenu("Konversi Video dan Foto")
        video_converter_menu.addAction("Mengubah Video Ke Foto", self.convert_video_to_per_frame_image)
        video_converter_menu.addAction("Mengubah Foto Ke Video", self.convert_image_per_frame_to_video)

        # Sub Menu Text and Speech Converter
        text_speech_converter_menu = ai_menu.addMenu("Konversi Teks dan Suara")
        text_speech_converter_menu.addAction("Mengubah Video Ke Text", self.convert_video_to_text)
        text_speech_converter_menu.addAction("Mengubah Text Ke Suara", self.convert_text_to_speech)

        # Sub Menu Foto and Webcam Sketch Pencil
        sketch_pencil_menu = ai_menu.addMenu("Sketch Pencil")
        sketch_pencil_menu.addAction("Mengubah Foto Ke Sketch Pencil", self.foto_sketch_pencil)
        sketch_pencil_menu.addAction("Mengubah Webcam Ke Sketch Pencil", self.webcam_sketch_pencil)

        # Sub Menu Video and Image Compress
        video_compress_menu = tools_menu.addMenu("Mengubah Video dan Foto")
        video_compress_menu.addAction("Mengubah Resolusi dan Frame Rate Video", self.change_video_resolution_and_frame_rate)
        video_compress_menu.addAction("Mengubah Ukuran Size dan Kualitas Foto", self.compress_size_foto)

        # Sub Menu Time Watch
        time_watch_menu = view_menu.addMenu("Jam Digital")
        time_watch_menu.addAction("Tampilkan", self.showTimeWatch)
        time_watch_menu.addAction("Sembuyikan", self.hideTimeWatch)

        # Sub Speed Effect Sound
        sound_efect_menu = view_menu.addMenu("Efek Suara")
        sound_efect_menu.addAction("Tampilkan", self.show_speed)
        sound_efect_menu.addAction("Sembuyikan", self.hide_speed)

        # Sub Menu Subtitle
        subtitle_menu = view_menu.addMenu("Subtitle")
        subtitle_menu.addAction("Tampilkan", self.show_subtitle)
        subtitle_menu.addAction("Sembuyikan", self.hide_subtitle)

        # Create MyGithub Action
        mygithub_action = QAction("Github Saya", self)
        mygithub_action.setShortcut(QKeySequence("Ctrl+G"))
        mygithub_action.setIcon(QIcon("icons/about.png"))
        mygithub_action.triggered.connect(self.mygithub_app)

        # Create About Media Player With Voice Assistant Action
        about_media_player_with_voice_assistant_action = QAction("Cara Penggunaan Media Player Dengan Mbah Google", self)
        about_media_player_with_voice_assistant_action.setShortcut(QKeySequence("Ctrl+M"))
        about_media_player_with_voice_assistant_action.setIcon(QIcon("icons/about.png"))
        about_media_player_with_voice_assistant_action.triggered.connect(self.voice_assistant)

        # Create About AI Hand Gesture Action
        about_ai_hand_gesture_action = QAction("Penggunaan AI Gerakan Tangan", self)
        about_ai_hand_gesture_action.setShortcut(QKeySequence("Ctrl+A"))
        about_ai_hand_gesture_action.setIcon(QIcon("icons/about.png"))
        about_ai_hand_gesture_action.triggered.connect(self.about_ai_hand_gesture)

        # Create About Shortkey Action
        about_shortkey_action = QAction("Penggunaan Shortkey", self)
        about_shortkey_action.setShortcut(QKeySequence("Ctrl+J"))
        about_shortkey_action.setIcon(QIcon("icons/about.png"))
        about_shortkey_action.triggered.connect(self.about_shortcut)

        # Create update Action
        update_action = QAction("Fitur Tebaru", self)
        update_action.setShortcut(QKeySequence("Ctrl+T"))
        update_action.setIcon(QIcon("icons/about.png"))
        update_action.triggered.connect(self.update_app)

        # Create About Action
        about_action = QAction("Tentang Aplikasi", self)
        about_action.setShortcut(QKeySequence("Ctrl+A"))
        about_action.setIcon(QIcon("icons/about.png"))
        about_action.triggered.connect(self.about_app)

        # Create Action
        file_menu.addAction(open_file_action)
        file_menu.addAction(open_folder_action)
        file_menu.addAction(open_subtitle_action)
        # file_menu.addSeparator()
        file_menu.addAction(exit_action)
        tools_menu.addAction(screenshot_action)
        tools_menu.addAction(remove_image_background_action)
        downloader_menu.addAction(youtube_downloader_action)
        downloader_menu.addAction(subtitle_video_downloader_action)
        downloader_menu.addAction(video_facebook_downloader_action)
        downloader_menu.addAction(video_instagram_downloader_action)
        downloader_menu.addAction(spotify_downloader_action)
        ai_menu.addAction(hand_gesture_action)
        ai_menu.addAction(objek_video_action)
        #ai_menu.addAction(objek_kamera_action)
        ai_menu.addAction(objek_foto_action)

        help_menu.addAction(mygithub_action)
        help_menu.addAction(about_media_player_with_voice_assistant_action)
        # help_menu.addSeparator()
        help_menu.addAction(about_ai_hand_gesture_action)
        help_menu.addAction(update_action)
        help_menu.addAction(about_action)
        help_menu.addAction(about_shortkey_action)

        self.openBtn = QPushButton('Buka Video/Musik')
        self.openBtn.clicked.connect(self.open_file)
        self.openBtn.setStyleSheet("background-color: white; color: black; font-size: 13px; border-style: outset; "
                                   "border-width: 2px; border-radius: 10px; min-width: 3em; padding: 3px;")

        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)
        self.playBtn.setShortcut(QKeySequence("Space"))
        self.playBtn.setStyleSheet("color: red; border-style: outset; border-width: 2px; border-radius: 10px;"
                                              "min-width: 3em; padding: 3px;")

        self.stopBtn = QPushButton()
        self.stopBtn.setEnabled(False)
        self.stopBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.stopBtn.clicked.connect(self.stop_video)
        self.stopBtn.setShortcut(QKeySequence("S"))
        self.stopBtn.setStyleSheet("color: red; border-style: outset; border-width: 2px; border-radius: 10px;"
                                              "min-width: 3em; padding: 3px;")

        self.muteBtn = QPushButton()
        self.muteBtn.setEnabled(False)
        self.muteBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
        self.muteBtn.clicked.connect(self.mute_video)
        self.muteBtn.setShortcut(QKeySequence("M"))
        self.muteBtn.setStyleSheet("color: red; border-style: outset; border-width: 2px; border-radius: 10px;"
                                              "min-width: 3em; padding: 3px;")

        self.forwardButton = QPushButton()
        self.forwardButton.setEnabled(False)
        self.forwardButton.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekForward))
        self.forwardButton.clicked.connect(self.forward_video)
        self.forwardButton.setShortcut(QKeySequence("Right"))
        self.forwardButton.setStyleSheet("color: red; border-style: outset; border-width: 2px; border-radius: 10px;"
                                              "min-width: 3em; padding: 3px;")

        self.backwardButton = QPushButton()
        self.backwardButton.setEnabled(False)
        self.backwardButton.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekBackward))
        self.backwardButton.clicked.connect(self.backward_video)
        self.backwardButton.setShortcut(QKeySequence("Left"))
        self.backwardButton.setStyleSheet("color: red; border-style: outset; border-width: 2px; border-radius: 10px;"
                                              "min-width: 3em; padding: 3px;")

        self.fullscreenBtn = QPushButton()
        self.fullscreenBtn.setEnabled(False)
        self.fullscreenBtn.setIcon(self.style().standardIcon(QStyle.SP_TitleBarMaxButton))
        self.fullscreenBtn.clicked.connect(self.fullscreen_video)
        self.fullscreenBtn.setShortcut(QKeySequence("F"))
        self.fullscreenBtn.setStyleSheet("color: red; border-style: outset; border-width: 2px; border-radius: 10px;"
                                              "min-width: 3em; padding: 3px;")

        # Create Slider Video Position
        self.slider = QSlider(QtCore.Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)

        # Create Slider Volume Position
        self.sliderVolume = QSlider(QtCore.Qt.Horizontal)
        self.sliderVolume.setRange(0, 200)
        self.sliderVolume.setValue(100)
        # Membuat up dan down volume dengan tombol panah atas dan bawah
        self.sliderVolume.valueChanged.connect(self.set_volume)
        self.sliderVolume.sliderMoved.connect(self.set_volume)

        # Create Speed Slider
        self.speedSlider = QSlider(Qt.Horizontal)
        self.speedSlider.setRange(0, 200)
        self.speedSlider.setValue(100)
        self.speedSlider.setTickPosition(QSlider.TicksBelow)
        self.speedSlider.setTickInterval(10)
        self.speedSlider.valueChanged.connect(self.set_speed)

        # Create Speed Label
        self.speedLabel = QLabel()
        self.speedLabel.setText('100%')
        self.speedLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.speedLabel.setStyleSheet("color: red; font-size: 12px;")

        # Create Label
        self.label = QLabel()
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)

        # Create Watch Digital Clock
        self.labelWatch = QLabel()
        self.labelWatch.setAlignment(Qt.AlignRight)
        self.labelWatch.setFont(QFont("Times New Roman", 14))
        self.labelWatch.setStyleSheet("color:Red; font-weight: bold")
        self.labelWatch.setText(self.timeWatch())
        self.labelWatch.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # Create Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.run_watch)
        self.timer.start(1000)

        # label volume
        self.labelVolume = QtWidgets.QLabel()
        self.labelVolume.setText("Volume :")
        self.labelVolume.setStyleSheet("color: white;")

        # label position
        self.labelPosition = QtWidgets.QLabel()
        self.labelPosition.setText("Position :")
        self.labelPosition.setStyleSheet("color: white;")

        self.elapsed_time_label = QLabel("00:00:00")
        self.elapsed_time_label.setStyleSheet("color: white;")

        self.remaining_time_label = QLabel("00:00:00")
        self.remaining_time_label.setStyleSheet("color: white;")

        # Membuat label untuk menampilkan nama file
        self.labelFile = QLabel()
        self.labelFile.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        self.labelFile.setStyleSheet("color: white; font-size: 15px;")

        # Membuat label untuk menampilkan nama file dalam folder
        self.labelFolder = QLabel()
        self.labelFolder.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        self.labelFolder.setStyleSheet("color: white; font-size: 12px;")

        # Membuat Label untuk menampilkan subtitle video yang sedang diputar format .srt
        self.labelSubtitle = QLabel()
        self.labelSubtitle.setAlignment(Qt.AlignCenter)
        self.labelSubtitle.setFont(QFont("Times New Roman", 14))
        self.labelSubtitle.setStyleSheet("color:Red; font-weight: bold")
        self.labelSubtitle.setText("")
        # label size subtitle 600
        self.labelSubtitle.setFixedWidth(600)
        # Jika Text Subtitle melebihi label maka akan di scroll
        self.labelSubtitle.setWordWrap(True)
        self.labelSubtitle.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        self.position = 0
        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

        hboxLayout = QtWidgets.QHBoxLayout()
        hboxLayout.setContentsMargins(0, 0, 0, 0)
        #hboxLayout.addWidget(self.openBtn)
        hboxLayout.addWidget(self.playBtn)
        hboxLayout.addWidget(self.stopBtn)
        hboxLayout.addWidget(self.muteBtn)
        hboxLayout.addWidget(self.backwardButton)
        hboxLayout.addWidget(self.forwardButton)
        hboxLayout.addWidget(self.fullscreenBtn)

        hboxLayoutVolume = QtWidgets.QHBoxLayout()
        hboxLayoutVolume.setContentsMargins(0, 0, 0, 0)
        hboxLayoutVolume.addWidget(self.labelVolume)
        hboxLayoutVolume.addWidget(self.sliderVolume)

        hboxLayoutPosition = QtWidgets.QHBoxLayout()
        hboxLayoutPosition.setContentsMargins(0, 0, 0, 0)
        hboxLayoutPosition.addWidget(self.labelPosition)
        hboxLayoutPosition.addWidget(self.slider)

        hboxLayoutTime = QtWidgets.QHBoxLayout()
        hboxLayoutTime.setContentsMargins(0, 0, 0, 0)
        hboxLayoutTime.addWidget(self.elapsed_time_label, 0, Qt.AlignLeft)
        hboxLayoutTime.addWidget(self.remaining_time_label, 1, Qt.AlignRight)
        hboxLayoutTime.addWidget(self.label)

        hboxLayoutSpeed = QtWidgets.QHBoxLayout()
        hboxLayoutSpeed.setContentsMargins(0, 0, 0, 0)
        hboxLayoutSpeed.addWidget(self.speedSlider)
        hboxLayoutSpeed.addWidget(self.speedLabel)

        hboxLayoutFolderName = QtWidgets.QHBoxLayout()
        hboxLayoutFolderName.setContentsMargins(0, 0, 0, 0)
        hboxLayoutFolderName.addWidget(self.labelFolder)

        hboxLayoutFileName = QtWidgets.QHBoxLayout()
        hboxLayoutFileName.setContentsMargins(0, 0, 0, 0)
        hboxLayoutFileName.addWidget(self.labelFile)

        hboxLayoutSubtitle = QtWidgets.QHBoxLayout()
        hboxLayoutSubtitle.setContentsMargins(0, 0, 0, 0)
        hboxLayoutSubtitle.addWidget(self.labelSubtitle)

        vboxLayout = QtWidgets.QVBoxLayout()
        vboxLayout.addWidget(self.labelWatch)
        vboxLayout.addWidget(videoWidget)
        vboxLayout.addLayout(hboxLayoutSubtitle)
        vboxLayout.addLayout(hboxLayoutFolderName)
        vboxLayout.addLayout(hboxLayoutFileName)
        vboxLayout.addLayout(hboxLayoutTime)
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addLayout(hboxLayoutPosition)
        vboxLayout.addLayout(hboxLayoutVolume)
        vboxLayout.addLayout(hboxLayoutSpeed)

        wid = QtWidgets.QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(vboxLayout)

        self.mediaPlayer.setVideoOutput(videoWidget)

        # Set Speed Slider
        self.speedSlider.hide()

        # Set Speed Label
        self.speedLabel.hide()

        # set Time Watch Show
        self.labelWatch.hide()

        # Set Subtitle
        self.labelSubtitle.hide()

        self.mediaPlayer.setPlaylist(self.playlist) # set playlist

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Buka Video/Musik", os.curdir, "Format Video (*.avi *.mp3)")

        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)
            self.stopBtn.setEnabled(True)
            self.muteBtn.setEnabled(True)
            self.forwardButton.setEnabled(True)
            self.backwardButton.setEnabled(True)
            self.fullscreenBtn.setEnabled(True)
            # Menampilkan nama file yang dipilih tidak termasuk path
            self.labelFile.setText(os.path.basename(filename))
            # labelFolder hide
            self.labelFolder.hide()

    def open_folder(self):
        global filename
        foldername = QFileDialog.getExistingDirectory(self, "Buka Folder", os.curdir)

        if foldername != '':
            self.playlist.clear()
            file_list = ""
            for filename in os.listdir(foldername):
                if filename.endswith(".mp3") or filename.endswith(".avi"):
                    self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(foldername + "/" + filename)))
                    file_list += os.path.basename(filename) + "\n"
            self.mediaPlayer.setPlaylist(self.playlist)
            self.playBtn.setEnabled(True)
            self.stopBtn.setEnabled(True)
            self.muteBtn.setEnabled(True)
            self.forwardButton.setEnabled(True)
            self.backwardButton.setEnabled(True)
            self.fullscreenBtn.setEnabled(True)
            self.labelFolder.setText(file_list)
            self.labelFile.setText(os.path.basename(foldername + " - " + filename))
            self.labelFolder.show()

    def update_label(self, media):
        if not media.isNull():
            url = media.canonicalUrl()
            self.labelFile.setText(os.path.basename(url.toLocalFile()))

    # Buka Subtitle File .srt
    def open_subtitle(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Buka Subtitle", os.curdir, "Format Subtitle (*.srt)")

        if filename != '':
            self.subtitle = pysrt.open(filename)
            # Subtitle position in seconds (float)
            self.subtitle_position = 0
            # Subtitle index
            self.subtitle_index = 0
            # Subtitle text
            self.subtitle_text = ""
            # Subtitle timer
            self.subtitle_timer = QTimer()
            self.subtitle_timer.timeout.connect(self.update_subtitle)
            self.subtitle_timer.start(1000)

    def update_subtitle(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.subtitle_position = self.mediaPlayer.position() / 1000
            if self.subtitle_index < len(self.subtitle):
                if self.subtitle_position >= self.subtitle[self.subtitle_index].start.minutes * 60 + self.subtitle[self.subtitle_index].start.seconds + self.subtitle[self.subtitle_index].start.milliseconds / 1000:
                    self.subtitle_text = self.subtitle[self.subtitle_index].text
                    self.labelSubtitle.setText(self.subtitle_text)
                    self.subtitle_index += 1
                    # Masih terdapat bug
                    '''# Jika video sudah selesai dan durasi video ulang dari awal maka subtitle akan di reset ke awal
                    if self.subtitle_index == len(self.subtitle):
                        self.subtitle_index = 0
                        self.subtitle_position = 0
                        self.subtitle_text = ""
                        self.labelSubtitle.setText(self.subtitle_text)'''
        else:
            self.labelSubtitle.setText("")

    def show_subtitle(self):
        self.labelSubtitle.show()

    def hide_subtitle(self):
        self.labelSubtitle.hide()

    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def stop_video(self):
        self.mediaPlayer.stop()

    def mute_video(self):
        if self.mediaPlayer.isMuted():
            self.mediaPlayer.setMuted(False)
            self.muteBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
        else:
            self.mediaPlayer.setMuted(True)
            self.muteBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaVolumeMuted))

    def forward_video(self):
        self.mediaPlayer.setPosition(self.position + 5000)

    def backward_video(self):
        self.mediaPlayer.setPosition(self.position - 5000)

    def fullscreen_video(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    def set_volume(self, volume):
        self.mediaPlayer.setVolume(volume)
        # Jika volume 0 maka icon mute akan muncul
        if volume == 0:
            self.muteBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaVolumeMuted))
        else:
            self.muteBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))

    def position_changed(self, position):
        self.slider.setValue(position)
        self.position = position

        elapsed_time = QTime(0, 0, 0)
        elapsed_time = elapsed_time.addMSecs(position)
        elapsed_time_string = elapsed_time.toString("hh:mm:ss")
        self.elapsed_time_label.setText(elapsed_time_string)

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

        remaining_time = QTime(0, 0, 0)
        remaining_time = remaining_time.addMSecs(duration)
        remaining_time_string = remaining_time.toString("hh:mm:ss")
        self.remaining_time_label.setText(remaining_time_string)

    def slow_video(self):
        self.mediaPlayer.setPlaybackRate(0.5)

    def normal_video(self):
        self.mediaPlayer.setPlaybackRate(1.0)

    def fast_video(self):
        self.mediaPlayer.setPlaybackRate(2.0)

    def set_speed(self, speed):
        self.speedLabel.setText(str(speed) + '%')
        self.mediaPlayer.setPlaybackRate(speed / 100)

    def show_speed(self):
        self.speedSlider.show()
        self.speedLabel.show()

    def hide_speed(self):
        self.speedSlider.hide()
        self.speedLabel.hide()

    def exit_app(self):
        ans = askokcancel('Keluar', "Anda Yakin Ingin Keluar?")  # menampilkan kotak konfirmasi
        if ans:
            self.close()

    def timeWatch(self):
        time = datetime.datetime.now()
        return time.strftime("Waktu Jakarta: " + "%H:%M:%S")

    def showTimeWatch(self):
        self.labelWatch.show()
        self.labelWatch.setText(self.timeWatch())

    def hideTimeWatch(self):
        self.labelWatch.hide()

    def run_watch(self):
        self.labelWatch.setText(self.timeWatch())

    def sleep_time_1_minute(self):
        self.sleepTimer = QTimer()
        self.sleepTimer.setSingleShot(True)
        self.sleepTimer.timeout.connect(self.sleep_video)
        self.sleepTimer.start(1 * 60000)

    def sleep_time_15_minute(self):
        self.sleepTimer = QTimer()
        self.sleepTimer.setSingleShot(True)
        self.sleepTimer.timeout.connect(self.sleep_video)
        self.sleepTimer.start(15 * 60000)

    def sleep_time_30_minute(self):
        self.sleepTimer = QTimer()
        self.sleepTimer.setSingleShot(True)
        self.sleepTimer.timeout.connect(self.sleep_video)
        self.sleepTimer.start(30 * 60000)

    def sleep_time_45_minute(self):
        self.sleepTimer = QTimer()
        self.sleepTimer.setSingleShot(True)
        self.sleepTimer.timeout.connect(self.sleep_video)
        self.sleepTimer.start(45 * 60000)

    def sleep_time_60_minute(self):
        self.sleepTimer = QTimer()
        self.sleepTimer.setSingleShot(True)
        self.sleepTimer.timeout.connect(self.sleep_video)
        self.sleepTimer.start(60 * 60000)

    def sleep_video(self):
        self.mediaPlayer.pause()
        ans = askokcancel('Waktu Tidur Sudah Habis', "Apakah Anda Ingin Keluar?")  # menampilkan kotak konfirmasi
        if ans:
            self.close()

    # membuat fungsi untuk mengulangi video otomatis jika sudah durasi video sudah selesai
    def video_auto_on(self):
        self.mediaPlayer.positionChanged.connect(self.video_on)

    def video_on(self, position):
        if self.mediaPlayer.duration() - position < 1000:
            self.mediaPlayer.setPosition(0)
            # untuk mengulangi musik otomatis jika durasi musik sudah selesai
            if self.mediaPlayer.mediaStatus() == QMediaPlayer.EndOfMedia:
                self.mediaPlayer.play()

    # membuat fungsi untuk mematikan video otomatis
    def video_auto_off(self):
        self.mediaPlayer.positionChanged.connect(self.video_off)

    def video_off(self, position):
        if self.mediaPlayer.duration() - position < 1000:
            self.play_video()
            # fungsi untuk mematikan musik otomatis jika durasi musik sudah selesai
            if self.mediaPlayer.mediaStatus() == QMediaPlayer.EndOfMedia:
                self.mediaPlayer.pause()

    def timer_stop(self):
        self.sleepTimer.stop()

    # membuat fungsi untuk menghubungkan class screen
    def screen(self):
        self.screen = screen()
        self.screen.show()

    # membuat fungsi untuk menghubungkan class handGesture
    def hand_gesture(self):
        self.gerakanTangan = handGesture()
        self.gerakanTangan.show()

    # membuat fungsi untuk menghubungkan class youtube downloader
    def youtube_downloader(self):
        self.youtubeDownloader = Youtube_Downloder()
        self.youtubeDownloader.show()

    # membuat fungsi untuk menghubungkan class subtitle video downloader
    def subtitle_video_downloader(self):
        self.subtitleVideoDownloader = Youtube_Subtitle_Downloader()
        self.subtitleVideoDownloader.show()

    # membuat fungsi untuk menghubungkan class video facebook downloader
    def video_facebook_downloader(self):
        self.videoFacebookDownloader = VideoFacebookDownloader()
        self.videoFacebookDownloader.show()

    # membuat fungsi untuk menghubungkan class instagram downloader
    def instagram_downloader(self):
        self.instagramDownloader = InstagramDownloader()
        self.instagramDownloader.show()

    # membuat fungsi untuk menghubungkan class SPOTIFY DOWNLOADER
    def spotify_downloader(self):
        self.spotifyDownloader = SpotifyDownloaderGUI()
        self.spotifyDownloader.show()

    # membuat fungsi untuk menghubungkan class video converter avi to mp4
    def video_converter_avi_to_mp4(self):
        self.videoConverterAviToMp4 = Video_Converter_Avi_To_Mp4()
        self.videoConverterAviToMp4.show()

    # membuat fungsi untuk menghubungkan class video converter mp4 to avi
    def video_converter_mp4_to_mp3(self):
        self.videoConverterMp4ToMp3 = Video_Converter_Mp4_To_Mp3()
        self.videoConverterMp4ToMp3.show()

    # membuat fungsi untuk menghubungkan class cut video
    def cut_video(self):
        self.cutVideo = CutVideoGUI()
        self.cutVideo.show()

    # membuat fungsi untuk menghubungkan video
    def video_combine(self):
        self.videoCombine = Combine_Video()
        self.videoCombine.show()

    # membuat fungsi untuk Remove Background Foto
    def remove_background_foto(self):
        self.removeBackgroundFoto = RemoveBackgroundImage()
        self.removeBackgroundFoto.show()

    # membuat fungsi untuk Compress Size Foto
    def compress_size_foto(self):
        self.compressSizeFoto = ImageCompressor()
        self.compressSizeFoto.show()

    # membuat fungsi untuk Convert Video To Per Frame Image
    def convert_video_to_per_frame_image(self):
        self.convertVideoToPerFrameImage = VideoToImageConverter()
        self.convertVideoToPerFrameImage.show()

    # membuat fungsi untuk convert image Per Frame To Video
    def convert_image_per_frame_to_video(self):
        self.convertImagePerFrameToVideo = ImageToVideoGUI()
        self.convertImagePerFrameToVideo.show()

    # membuat fungsi untuk convert video To Text
    def convert_video_to_text(self):
        self.convertVideoToText = VideoToText()
        self.convertVideoToText.show()

    # membuat fungsi untuk convert text To speech
    def convert_text_to_speech(self):
        self.convertTextToSpeech = TextToSpeech()
        self.convertTextToSpeech.show()

    # membuat fungsi untuk menghubungkan Change Video Resolution and Frame Rate
    def change_video_resolution_and_frame_rate(self):
        self.changeVideoResolutionAndFrameRate = ChangeResolusiAndFrame()
        self.changeVideoResolutionAndFrameRate.show()

    def deteksi_objek_video(self):
        self.DeteksiObjekVideo = ObjectDetectionVideo()
        self.DeteksiObjekVideo.show()

    #def deteksi_objek_kamera(self):
    #    self.DeteksiObjekCamera = ObjectDetectionCamera()
    #    self.DeteksiObjekCamera.show()

    def deteksi_objek_foto(self):
        self.DeteksiObjekFoto = MendeteksiObjekFoto()
        self.DeteksiObjekFoto.show()

    # Membuat Fungsi untuk menghubungkan class Foto Sketch Pencil
    def foto_sketch_pencil(self):
        self.fotoSketchPencil = PhotoEditorSketchPencil()
        self.fotoSketchPencil.show()

    # Membuat Fungsi untuk menghubungkan class Webcame Sketch Pencil
    def webcam_sketch_pencil(self):
        self.webcamSketchPencil = WebcamSketchPencil()
        self.webcamSketchPencil.show()

    def voice_assistant(self):
        self.voiceAssistant = VoiceAssistantGoogle()
        self.voiceAssistant.show()

    def mygithub_app(self):
        webbrowser.open_new(r"https://github.com/bujay")  # pergi ke Github saya

    def about_app(self):
        mbox.showinfo("Pemutar Media Sederhana", "Media Player (Beta Version)\n"
                                                 "Versi: 1.0.15\n"
                                                 "Date Release: 09-09-2022\n"
                                                 "Date Update: 02-04-2023\n"
                                                 "Format: Avi, Mp3\n"
                                                 "OS: Windows 7,8,10,11\n\n"
                                                 "Developer: Ahmad Bujay Rimi | Enjay Studio\n"
                                                 "Teknik Informatika, Universitas Esa Unggul")

    def about_ai_hand_gesture(self):
        mbox.showinfo("Penggunaan AI Pergerakan Tangan (Tahap Pengembang)",
                      "Angkat tangan ke arah kamera dan sesuaikan jari anda"
                      "\ndengan jari yang ada di layar untuk mengontrol media player.\n"
                      "Berawal dari jari telunjuk, jari tengah, jari manis, jari kelingking, dan jari kecil.\n\n"
                      "- Jari Telunjuk (1) = play/pause\n"
                      "- Jari Tengah (2) = mute\n"
                      "- Jari Manis (3) = backward\n"
                      "- Jari Kelingking (4) = forward\n"
                      "- Jari Kecil/Ibu Jari (5) = fullscreen\n\n"
                      "Developer: Ahmad Bujay Rimi | Enjay Studio\n""Teknik Informatika, Universitas Esa Unggul")

    def update_app(self):
        mbox.showinfo("Fitur Terbaru Versi: 1.0.15", "- Fitur MenuBar.\n"
                                                     "- Durasi Video.\n"
                                                     "- Penambahan Fitur Borderless.\n"
                                                     "- Memindahkan Open File ke MenuBar.\n"
                                                     "- Menambahkan Fitur Efek Suara Dan Kecepatan Video.\n"
                                                     "- Menambahkan Fitur Waktu Jakarta.\n"
                                                     "- Menambahkan Pengaturan Waktu Tidur.\n"
                                                     "- Menambahkan Fitur Auto Repeat Video.\n"
                                                     "- Menambahkan Fitur FileName.\n"
                                                     "- Memindahkan Waktu Jam Ke MenuBar.\n"
                                                     "- Menambahkan Fitur Subtitle.\n"
                                                     "- Bug Fix Subtitle.\n"
                                                     "- Menambahkan Fitur ScreenShot.\n"
                                                     "- Menambahkan Fitur Hand Gesture (Beta).\n"
                                                     "- Menambahkan Fitur Deteksi Objek Video (Beta).\n"
                                                     "- Menambahkan Fitur Deteksi Objek Kamera (Beta).\n"
                                                     "- Menambahkan Fitur Deteksi Objek Foto (Beta).\n"
                                                     "- Youtube Downloader.\n"
                                                     "- Subtitle Video Downloader(Beta).\n"
                                                     "- Video Facebook Downloader.\n"
                                                     "- Profile Instragram Downloader.\n"
                                                     "- Video Converter Avi To Mp4.\n"
                                                     "- Video Converter Mp4 To Mp3.\n"
                                                     "- Potong Video.\n"
                                                     "- Gabungkan Video.\n"
                                                     "- Merubah Video Ke Per Frame Foto.\n"
                                                     "- Merubah Per Frame Foto Ke Video (Beta).\n"
                                                     "- Mengubah Resolusi Video Dan Frame Rate.\n"
                                                     "- Mengubah Ukuran dan Kualitas Foto.\n"
                                                     "- Hapus Background Foto (Beta).\n")

    def about_shortcut(self):
        mbox.showinfo("Short Key", "Space = Play/Pause.\n"
                                   "M = Mute.\n"
                                   "Left = Backward.\n"
                                   "Right = Forward.\n"
                                   "F = Fullscreen.\n"
                                   "Ctrl + O = Open File.\n"
                                   "Ctrl + S = Open Subtitle.\n"
                                   "Ctrl + Q = Keluar.\n"
                                   "Ctrl + G = Github.\n"
                                   "Ctrl + A = About App.\n"
                                   "Ctrl + K = About AI Hand Gesture.\n"
                                   "Ctrl + J = About Shortcut.\n"
                                   "Ctrl + L = Update App.\n")


# Class Untuk ScreenShot
class screen(QWidget):
    def __init__(self, parent=None):
        super(screen, self).__init__()
        self.preview_screen = QApplication.primaryScreen().grabWindow(QApplication.desktop().winId())
        print(QApplication.screens())
        self.settings()
        self.create_widgets()
        self.set_layout()

    def settings(self):
        self.resize(570, 320)
        self.setWindowTitle("Gambar Layar ScreenShot")
        self.setWindowIcon(QtGui.QIcon(':/Logo.png'))

    def create_widgets(self):
        self.img_preview = QLabel()
        self.img_preview.setPixmap(self.preview_screen.scaled(550, 550, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.btn_save_screenshot = QPushButton("Simpan screenshot")
        self.btn_new_screenshot = QPushButton("Keluar")

        # signals connections
        self.btn_save_screenshot.clicked.connect(self.save_screenshot)
        self.btn_new_screenshot.clicked.connect(self.new_screenshot)

    def set_layout(self):
        self.layout = QGridLayout(self)
        self.layout.addWidget(self.img_preview, 0, 0, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.btn_save_screenshot, 2, 0, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.btn_new_screenshot, 2, 0, alignment=Qt.AlignRight)
        self.setLayout(self.layout)

    def save_screenshot(self):
        img, _ = QFileDialog.getSaveFileName(self, "Menyimpan File",
                                             filter="PNG(*.png);; JPEG(*.jpg)")
        if img[-3:] == "png":
            self.preview_screen.save(img, "png")
        elif img[-3:] == "jpg":
            self.preview_screen.save(img, "jpg")

    def new_screenshot(self):
        self.close()


class handGesture(QThread):
    def __init__(self, parent=None):
        super(handGesture, self).__init__()
        self.cap = cv2.VideoCapture(0)
        self.drawing = mdp.solutions.drawing_utils
        self.hands = mdp.solutions.hands
        self.hand_obj = self.hands.Hands(max_num_hands=1)
        self.start_init = False
        self.prev = -1
        self.start_time = 0
        self.end_time = 0

    def count_fingers(self, lst):
        cnt = 0
        thresh = (lst.landmark[0].y * 100 - lst.landmark[9].y * 100) / 2
        if (lst.landmark[5].y * 100 - lst.landmark[8].y * 100) > thresh:
            cnt += 1
        if (lst.landmark[9].y * 100 - lst.landmark[12].y * 100) > thresh:
            cnt += 1
        if (lst.landmark[13].y * 100 - lst.landmark[16].y * 100) > thresh:
            cnt += 1
        if (lst.landmark[17].y * 100 - lst.landmark[20].y * 100) > thresh:
            cnt += 1
        if (lst.landmark[5].x * 100 - lst.landmark[4].x * 100) > 6:
            cnt += 1
        return cnt

    def run(self):
        while True:
            self.end_time = time.time()
            _, frm = self.cap.read()
            frm = cv2.flip(frm, 1)
            res = self.hand_obj.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))
            if res.multi_hand_landmarks:
                hand_keyPoints = res.multi_hand_landmarks[0]
                cnt = self.count_fingers(hand_keyPoints)
                print(self.count_fingers(hand_keyPoints))
                if not (self.prev == cnt):
                    if not (self.start_init):
                        self.start_time = time.time()
                        self.start_init = True
                    elif (self.end_time - self.start_time) > 0.2:
                        if (cnt == 0):
                            pyautogui.press("Escape")
                        elif (cnt == 1):
                            pyautogui.press("space")
                        elif (cnt == 2):
                            pyautogui.press("m")
                        elif (cnt == 3):
                            pyautogui.press("left")
                        elif (cnt == 4):
                            pyautogui.press("right")
                        elif (cnt == 5):
                            pyautogui.press("f")
                        self.prev = cnt
                        self.start_init = False
                self.drawing.draw_landmarks(frm, hand_keyPoints, self.hands.HAND_CONNECTIONS)
            cv2.imshow("Window Pergerakan Tangan", frm)
            if cv2.waitKey(1) == 27:
                cv2.destroyAllWindows()
                self.cap.release()
                break

    def show(self):
        self.start()
        pass


# Class Untuk Mendeteksi Objek Dari Video
class ObjectDetectionVideo(QThread):
    def __init__(self, parent=None):
        super(ObjectDetectionVideo, self).__init__(parent)
        self.net = cv2.dnn.readNet("weight/yolov3-tiny.weights", "cfg_realtime/yolov3-tiny.cfg")
        self.net = cv2.dnn.readNet("weight/yolov3.weights", "cfg_realtime/yolov3.cfg")
        self.classes = []
        with open("coco.names_object/coco.names", "r") as f:
            self.classes = [line.strip() for line in f.readlines()]
        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))

    def run(self):
        timeframe = time.time()
        frame_id = 0
        while True:
            _, frm = self.cap.read()
            frame_id += 1
            # frm = cv2.flip(frm, 1)
            height, width, channels = frm.shape

            # Detecting objects
            blob = cv2.dnn.blobFromImage(frm, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

            self.net.setInput(blob)
            outs = self.net.forward(self.output_layers)

            # Showing informations on the screen
            class_ids = []
            confidences = []
            boxes = []
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.5:
                        # Object detected
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)

                        # Rectangle coordinates
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)

                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)

            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
            font = cv2.FONT_HERSHEY_SIMPLEX
            for i in range(len(boxes)):
                if i in indexes:
                    x, y, w, h = boxes[i]
                    label = str(self.classes[class_ids[i]])
                    confidence = confidences[i]
                    color = self.colors[i]
                    color = (30, 144, 255)
                    rectangle_bgr = (30, 144, 255)
                    cv2.rectangle(frm, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frm, label, (x, y + 30), font, 1, color, 2)
                    cv2.putText(frm, label + " " + str(round(confidence, 2)), (x, y + 30), font, 1, color, 2)

            elapsed_time = time.time() - timeframe
            fps = frame_id / elapsed_time
            cv2.putText(frm, str(round(fps, 2)), (10, 50), font, 2, (0, 0, 255), 2)
            cv2.putText(frm, "FPS", (220, 50), font, 2, (0, 0, 255), 2)
            cv2.imshow("Mendeteksi Objek Video (Tahap Pengembangan)", frm)

            # Jika menekan escape maka akan keluar dari program
            if cv2.waitKey(1) & 0xFF == 27:
                cv2.destroyAllWindows()
                self.cap.release()
                break
            #if cv2.waitKey(1) & 0xFF == ord('q'):
            #    break

        self.cap.release()
        cv2.destroyAllWindows()

    def show(self):
        filename, _ = QFileDialog.getOpenFileName(None, "Pilih Video", "", "Format Video (*.mp4 *.avi)")
        self.cap = cv2.VideoCapture(filename)
        self.start()
        pass

'''
class ObjectDetectionCamera(QThread):
    def __init__(self, file_path, parent=None):
        super(ObjectDetectionVideo, self).__init__(parent)
        self.net = cv2.dnn.readNet("weight/yolov3-tiny.weights", "cfg_realtime/yolov3-tiny.cfg")
        self.net = cv2.dnn.readNet("weight/yolov3.weights", "cfg_realtime/yolov3.cfg")
        self.classes = []
        with open("coco.names_object/coco.names", "r") as f:
            self.classes = [line.strip() for line in f.readlines()]
        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))
        self.file_path = file_path

    def run(self):
        cap = cv2.VideoCapture(self.file_path)
        timeframe = time.time()
        frame_id = 0
        while True:
            _, frm = cap.read()
            if not _:
                break
            frame_id += 1
            # frm = cv2.flip(frm, 1)
            height, width, channels = frm.shape

            # Detecting objects
            blob = cv2.dnn.blobFromImage(frm, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

            self.net.setInput(blob)
            outs = self.net.forward(self.output_layers)

            # Showing informations on the screen
            class_ids = []
            confidences = []
            boxes = []
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.5:
                        # Object detected
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)

                        # Rectangle coordinates
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)

                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)

            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
            font = cv2.FONT_HERSHEY_SIMPLEX
            for i in range(len(boxes)):
                if i in indexes:
                    x, y, w, h = boxes[i]
                    label = str(self.classes[class_ids[i]])
                    confidence = confidences[i]
                    color = self.colors[i]
                    color = (30, 144, 255)
                    rectangle_bgr = (30, 144, 255)
                    cv2.rectangle(frm, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frm, label, (x, y + 30), font, 1, color, 2)
                    cv2.putText(frm, label + " " + str(round(confidence, 2)), (x, y + 30), font, 1, color, 2)

            elapsed_time = time.time() - timeframe
            fps = frame_id / elapsed_time
            cv2.putText(frm, str(round(fps, 2)) + " fps", (10, 50), font, 1, (0, 0, 255), 2)

            cv2.imshow("Object Detection", frm)
            key = cv2.waitKey(1)
            if key == 27:
                break

        cap.release()
        cv2.destroyAllWindows()
'''


# Class Untuk Mendeteksi Objek dari Foto
class MendeteksiObjekFoto(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mendeteksi Objek dari Foto (Tahap Pengembangan)")
        self.setWindowIcon(QtGui.QIcon(':/Logo.png'))
        self.setGeometry(100, 100, 500, 200)
        self.setFixedSize(500, 200)

        self.img_path_label = QLabel("File Foto:", self)
        self.img_path_label.setGeometry(20, 20, 80, 30)

        self.img_path_lineedit = QLineEdit(self)
        self.img_path_lineedit.setGeometry(110, 20, 280, 30)
        self.img_path_lineedit.setReadOnly(True)

        self.img_path_button = QPushButton("Buka File", self)
        self.img_path_button.setGeometry(400, 20, 80, 30)
        self.img_path_button.clicked.connect(self.browse_img)

        self.save_path_label = QLabel("Simpen Ke:", self)
        self.save_path_label.setGeometry(20, 60, 80, 30)

        self.save_path_lineedit = QLineEdit(self)
        self.save_path_lineedit.setGeometry(110, 60, 280, 30)
        self.save_path_lineedit.setReadOnly(True)

        self.save_path_button = QPushButton("Buka Folder", self)
        self.save_path_button.setGeometry(400, 60, 80, 30)
        self.save_path_button.clicked.connect(self.browse_save_path)

        self.detect_button = QPushButton("Mulai Mendeteksi Objek!", self)
        self.detect_button.setGeometry(110, 110, 280, 30)
        self.detect_button.clicked.connect(self.detect_objects)

        self.quit_button = QPushButton("Informasi", self)
        self.quit_button.setGeometry(110, 150, 280, 30)
        self.quit_button.clicked.connect(self.informasi)

    def browse_img(self):
        img_path, _ = QFileDialog.getOpenFileName(self, "Pilih Foto", "", "Format Foto (*.jpg)")
        if img_path:
            self.img_path_lineedit.setText(img_path)

    def browse_save_path(self):
        save_path = QFileDialog.getExistingDirectory(self, "Pilih Folder Simpan")
        if save_path:
            self.save_path_lineedit.setText(save_path)

    def detect_objects(self):
        img_path = self.img_path_lineedit.text()
        save_path = self.save_path_lineedit.text()
        if not img_path or not save_path:
            QMessageBox.warning(self, "Peringatan", "Foto atau Folder Simpan Tidak Boleh Kosong")
            return

        net = cv2.dnn.readNet("weight/yolov3.weights", "cfg_object/yolov3.cfg")
        classes = []
        with open("coco.names_object/coco.names", "r") as f:
            classes = [line.strip() for line in f.readlines()]
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
        colors = np.random.uniform(0, 255, size=(len(classes), 3))

        # Loading image
        img = cv2.imread(img_path)
        # img = cv2.resize(img, None, fx=0.4, fy=0.4)
        height, width, channels = img.shape

        # Detecting objects
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        # Showing informations on the screen
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        font = cv2.FONT_HERSHEY_SIMPLEX
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                color = colors[class_ids[i]]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, label, (x, y - 5), font, 2, color, 2)

        # Saving image
        filename = os.path.basename(img_path)
        filename, extension = os.path.splitext(filename)
        save_path = os.path.join(save_path, filename + "_deteksi_objek" + extension)
        cv2.imwrite(save_path, img)

        QMessageBox.information(self, "Berhasil", "Mendeteksi Objek Foto Sudah Selesai")

    def informasi(self):
        mbox.showinfo("Informasi Penggunaan", "1. Pilih Foto yang ingin dideteksi objeknya.\n"
                                              "2. Pilih Folder Simpan Video.\n"
                                              "3. Klik Tombol 'Mulai Mendeteksi Objek!'.\n"
                                              "4. Tunggu hingga muncul notifikasi "
                                              "'Mendeteksi Objek Foto Sudah Selesai'.\n"
                                              "5. Selesai.\n"
                                              "5. Foto yang sudah dideteksi objeknya akan "
                                              "tersimpan di folder yang sudah dipilih.\n\n"
                                              "Developer: Ahmad Bujay Rimi | Enjay Studio\n"
                                              "Teknik Informatika, Universitas Esa Unggul")


# Class Untuk Youtube Downloader
class Youtube_Downloder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.initUi()

    def setupUi(self):
        self.setFixedSize(450, 300)
        self.setWindowTitle('Youtube Downloader')
        self.setWindowIcon(QtGui.QIcon(':/Logo.png'))
        self.move(300, 300)

        self.label = QLabel(self)
        self.label.setText('Masukan URL Video:')
        self.label.move(20, 20)

        self.lineEdit = QLineEdit(self)
        self.lineEdit.move(20, 50)
        self.lineEdit.resize(350, 25)

        self.label2 = QLabel(self)
        self.label2.setText('Simpan Ke:')
        # Size
        self.label2.resize(200, 25)
        self.label2.move(20, 80)

        self.pushButton = QPushButton(self)
        self.pushButton.setText('Buka Folder')
        self.pushButton.move(20, 102)
        # Size
        self.pushButton.resize(200, 25)
        self.pushButton.clicked.connect(self.pilih_folder)

        self.label3 = QLabel(self)
        self.label3.setText('Pilih Format')
        self.label3.move(20, 130)

        self.label4 = QLabel(self)
        self.label4.setText('Tidak ada folder yang dipilih')
        self.label4.resize(210, 25)
        self.label4.move(80, 80)

        self.comboBox = QComboBox(self)
        self.comboBox.addItems(['3GPP', 'mp4', 'mp4 (Hanya Suara)'])
        # Size
        self.comboBox.resize(125, 25)
        self.comboBox.move(20, 155)

        self.pushButton2 = QPushButton(self)
        self.pushButton2.setText('Mulai Download Video Youtube!')
        self.pushButton2.move(20, 195)
        # Size
        self.pushButton2.resize(200, 25)
        self.pushButton2.clicked.connect(self.download)

        self.pushButton3 = QPushButton(self)
        self.pushButton3.setText('Informasi')
        self.pushButton3.move(20, 230)
        # Size
        self.pushButton3.resize(200, 25)
        self.pushButton3.clicked.connect(self.informasi)

    def initUi(self):
        self.show()

    def pilih_folder(self):
        self.folder = QFileDialog.getExistingDirectory(self, 'Pilih Folder Penyimpanan')
        self.setWindowIcon(QtGui.QIcon(':/Logo.png'))
        self.label4.setText(self.folder)

    def download(self):
        choice = self.comboBox.currentText()
        url = self.lineEdit.text()

        if(len(url) > 1):
            yt = YouTube(url)

            if(choice == '720p'):
                select = yt.streams.filter(progressive=True).first()

            elif(choice == 'mp4'):
                select = yt.streams.filter(progressive=True, file_extension='mp4').last()

            elif(choice == 'mp4 (Hanya Suara)'):
                select = yt.streams.filter(only_audio=True).first()

            select.download(self.folder)
            QMessageBox.information(self, 'Informasi', 'Video Selesai Di Download')
        else:
            QMessageBox.warning(self, 'Peringatan', 'Masukan URL Video')

    def informasi(self):
        mbox.showinfo("Informasi Penggunaan", "1. Masukan URL Video.\n"
                                              "2. Pilih Folder Penyimpanan.\n"
                                              "3. Pilih Format (3GPP, Mp4(720p), Mp4(Hanya Suara)).\n"
                                              "4. Klik Tombol Download.\n"
                                              "5. Tunggu Muncul Notifikasi 'Video Selesai Di Download'.\n"
                                              "6. Selesai.\n\n"
                                              "Note: \n"
                                              "1. Harus Terhubung Dengan Internet.\n\n"
                                              "Developer: Ahmad Bujay Rimi | Enjay Studio\n"
                                              "Teknik Informatika, Universitas Esa Unggul")


# Class Untuk Mendownload Subtitle Youtube
class Youtube_Subtitle_Downloader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.initUi()

    def setupUi(self):
        self.setFixedSize(500, 300)
        self.setWindowTitle('Youtube Subtitle Downloader (Tahap Pengembangan)')
        self.setWindowIcon(QtGui.QIcon(':/Logo.png'))
        self.move(300, 300)

        self.label = QLabel(self)
        self.label.setText('Masukan URL Video:')
        # Size
        self.label.resize(160, 25)
        self.label.move(20, 20)

        self.lineEdit = QLineEdit(self)
        self.lineEdit.move(20, 50)
        self.lineEdit.resize(350, 25)

        self.label2 = QLabel(self)
        self.label2.setText('Simpan Ke:')
        # Size
        self.label2.resize(200, 25)
        self.label2.move(20, 80)

        self.pushButton = QPushButton(self)
        self.pushButton.setText('Buka Folder')
        self.pushButton.move(20, 102)
        # Size
        self.pushButton.resize(200, 25)
        self.pushButton.clicked.connect(self.pilih_folder)

        self.label3 = QLabel(self)
        self.label3.setText('Pilih Bahasa')
        self.label3.move(20, 130)

        self.comboBox = QComboBox(self)
        self.comboBox.addItems(['Indonesia', 'Inggris'])
        # Size
        self.comboBox.resize(125, 25)
        self.comboBox.move(20, 155)

        self.pushButton2 = QPushButton(self)
        self.pushButton2.setText('Mulai Download Subtitle Youtube!')
        self.pushButton2.move(20, 195)
        # Size
        self.pushButton2.resize(200, 25)
        self.pushButton2.clicked.connect(self.download)

        self.pushButton3 = QPushButton(self)
        self.pushButton3.setText('Informasi')
        self.pushButton3.move(20, 230)
        # Size
        self.pushButton3.resize(200, 25)
        self.pushButton3.clicked.connect(self.informasi)

    def initUi(self):
        self.show()

    def pilih_folder(self):
        self.folder = QFileDialog.getExistingDirectory(self, 'Pilih Folder Penyimpanan')
        self.setWindowIcon(QtGui.QIcon(':/Logo.png'))
        self.label4 = QLabel(self)
        self.label4.setText(self.folder)
        self.label4.move(20, 230)

    def download(self):
        choice = self.comboBox.currentText()
        url = self.lineEdit.text()

        if(len(url) > 1):
            if(choice == 'Indonesia'):
                #srt = YouTubeTranscriptApi.get_transcript(url, languages=['id'])
                # Jika url nya: https://www.youtube.com/watch?v=1iWTl8DM7Rg&list=RDMM_Ycq9H6tbLI&index=3, maka yang diambil hanya: 1iWTl8DM7Rg
                srt = YouTubeTranscriptApi.get_transcript(url[32:43], languages=['id'])
                with open('srt_file.txt', 'w') as f:
                    f.writelines('%s \n' % i for i in srt)

            elif(choice == 'Inggris'):
                #srt = YouTubeTranscriptApi.get_transcript(url, languages=['en'])
                srt = YouTubeTranscriptApi.get_transcript(url[32:43], languages=['en'])
                with open('srt_file.txt', 'w') as f:
                    f.writelines('%s \n' % i for i in srt)

            shutil.move('srt_file.txt', self.folder)
            QMessageBox.information(self, 'Informasi', 'Subtitle Selesai Di Download')
        else:
            QMessageBox.warning(self, 'Peringatan', 'Masukan URL Video')

    def informasi(self):
        mbox.showinfo("Informasi Penggunaan", "1. Masukan URL Video.\n"
                                              "2. Pilih Folder Penyimpanan.\n"
                                              "3. Pilih Bahasa (Indonesia, Inggris).\n"
                                              "4. Klik Tombol Download.\n"
                                              "5. Tunggu Muncul Notifikasi 'Subtitle Selesai Di Download'.\n"
                                              "6. Selesai.\n\n"
                                              "Note: \n"
                                              "1. Harus Terhubung Dengan Internet.\n\n"
                                              "Developer: Ahmad Bujay Rimi | Enjay Studio\n"
                                              "Teknik Informatika, Universitas Esa Unggul")


# Class Untuk Merubah Format Video .avi ke .mp4
class Video_Converter_Avi_To_Mp4(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.setFixedSize(490, 135)
        self.setWindowTitle('Convert Video From .avi to .mp4')
        self.setWindowIcon(QtGui.QIcon(':/Logo.png'))
        self.move(300, 300)

        self.label = QLabel(self)
        self.label.setText('Merubah Format Video .avi ke .mp4')
        self.label.setFont(QFont('Times', 15, QFont.Bold))
        self.label.move(20, 20)

        self.pushButton = QPushButton(self)
        self.pushButton.setText('Mulai Format Video!')
        # Size
        self.pushButton.resize(450, 30)
        self.pushButton.move(20, 50)
        self.pushButton.clicked.connect(self.convert_video)

        self.pushButton = QPushButton(self)
        self.pushButton.setText('Informasi')
        # Size
        self.pushButton.resize(450, 30)
        self.pushButton.move(20, 90)
        self.pushButton.clicked.connect(self.informasi)

    def convert_video(self):
        file = QFileDialog.getOpenFileName(self, 'Pilih File', os.getcwd(), "Format Video (*.avi)")
        if file:
            file_name = os.path.basename(file[0])
            file_name_without_extension = os.path.splitext(file_name)[0]
            new_file_name = file_name_without_extension + '.mp4'
            new_file_path = os.path.join(os.path.dirname(file[0]), new_file_name)
            clip = VideoFileClip(file[0])
            clip.write_videofile(new_file_path)

            QMessageBox.information(self, 'Informasi', 'Convert Video Selesai')
        else:
            QMessageBox.warning(self, 'Peringatan', 'File Video Tidak Ditemukan')

    def informasi(self):
        mbox.showinfo("Informasi Penggunaan", "1. Pilih File Video yang akan di convert.\n"
                                              "2. Klik tombol Merubah Format Video.\n"
                                              "3. Tunggu hingga muncul notifikasi Convert Video Selesai.\n\n"
                                              "Note: File video yang akan di convert harus berformat .avi "
                                              "dan hasil convert akan berformat .mp4 di folder yang sama "
                                              "dengan file video yang akan di convert.\n\n" 
                                              "Developer: Ahmad Bujay Rimi | Enjay Studio\n"
                                              "Teknik Informatika, Universitas Esa Unggul")


# Class Untuk Mengubah Format Video .mp4 ke Musik .mp3
class Video_Converter_Mp4_To_Mp3(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.setFixedSize(490, 135)
        self.setWindowTitle('Convert Video From .mp4 to .mp3')
        self.setWindowIcon(QtGui.QIcon(':/Logo.png'))
        self.move(300, 300)

        self.label = QLabel(self)
        self.label.setText('Merubah Format Video .mp4 ke .mp3')
        self.label.setFont(QFont('Times', 15, QFont.Bold))
        self.label.move(20, 20)

        self.pushButton = QPushButton(self)
        self.pushButton.setText('Mulai Format Video ke Audio!')
        # Size
        self.pushButton.resize(450, 30)
        self.pushButton.move(20, 50)
        self.pushButton.clicked.connect(self.convert_video)

        self.pushButton = QPushButton(self)
        self.pushButton.setText('Informasi')
        # Size
        self.pushButton.resize(450, 30)
        self.pushButton.move(20, 90)
        self.pushButton.clicked.connect(self.informasi)

    def convert_video(self):
        file = QFileDialog.getOpenFileName(self, 'Pilih File', os.getcwd(), "Format Video (*.mp4)")
        if file:
            file_name = os.path.basename(file[0])
            file_name_without_extension = os.path.splitext(file_name)[0]
            new_file_name = file_name_without_extension + '.mp3'
            new_file_path = os.path.join(os.path.dirname(file[0]), new_file_name)
            clip = VideoFileClip(file[0])
            audioClip = clip.audio # Extract audio from video
            audioClip.write_audiofile(new_file_path)

            QMessageBox.information(self, 'Informasi', 'Convert Video ke Audio Selesai')
        else:
            QMessageBox.warning(self, 'Peringatan', 'File Video Tidak Ditemukan')

    def informasi(self):
        mbox.showinfo("Informasi Penggunaan", "1. Pilih File Video yang akan di convert.\n"
                                              "2. Klik tombol Merubah Format Video.\n"
                                              "3. Tunggu hingga muncul notifikasi 'Convert Video ke Audio Selesai'.\n\n"
                                              "Note: File video yang akan di convert harus berformat .mp4 "
                                              "dan hasil convert akan berformat .mp3 di folder yang sama "
                                              "dengan file video yang akan di convert.\n\n" 
                                              "Developer: Ahmad Bujay Rimi | Enjay Studio\n"
                                              "Teknik Informatika, Universitas Esa Unggul")


# Class Untuk Memotong Video
class CutVideoGUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(CutVideoGUI, self).__init__()

        # set window title
        self.setWindowTitle("Potong Video (.mp4)")
        self.setWindowIcon(QtGui.QIcon(':/Logo.png'))

        # set window dimensions
        self.setFixedSize(500, 450)

        # create label for input file
        self.input_label = QtWidgets.QLabel(self)
        self.input_label.setText("File Video: ")
        self.input_label.move(20, 20)

        # create input file line edit
        self.input_file_edit = QtWidgets.QLineEdit(self)
        self.input_file_edit.setReadOnly(True)
        self.input_file_edit.move(120, 20)
        self.input_file_edit.resize(230, 30)

        # create browse button for input file
        self.input_file_button = QtWidgets.QPushButton(self)
        self.input_file_button.setText("Buka Folder")
        self.input_file_button.move(370, 20)
        self.input_file_button.resize(100, 30)
        self.input_file_button.clicked.connect(self.browse_input_file)

        # create label for duration
        self.duration_label = QtWidgets.QLabel(self)
        self.duration_label.setText("Durasi Video: ")
        self.duration_label.move(20, 80)

        # create duration label
        self.duration_text = QtWidgets.QLabel(self)
        self.duration_text.setText("")
        self.duration_text.move(120, 80)

        # create label for output folder
        self.output_label = QtWidgets.QLabel(self)
        self.output_label.setText("Simpan Ke: ")
        self.output_label.move(20, 140)

        # create output folder line edit
        self.output_folder_edit = QtWidgets.QLineEdit(self)
        self.output_folder_edit.setReadOnly(True)
        self.output_folder_edit.move(120, 140)
        self.output_folder_edit.resize(230, 30)

        # create browse button for output folder
        self.output_folder_button = QtWidgets.QPushButton(self)
        self.output_folder_button.setText("Buka Folder")
        self.output_folder_button.move(370, 140)
        self.output_folder_button.resize(100, 30)
        self.output_folder_button.clicked.connect(self.browse_output_folder)

        # create label for cut options
        self.cut_label = QtWidgets.QLabel(self)
        self.cut_label.setText("Pilih Yang ingin Di Cut Video nya: ")
        self.cut_label.move(20, 200)
        # Size
        self.cut_label.resize(200, 30)

        # create radio buttons for cut options
        self.cut_seconds_button = QtWidgets.QRadioButton(self)
        self.cut_seconds_button.setText("Per Detik")
        self.cut_seconds_button.setChecked(True)
        self.cut_seconds_button.move(100, 240)

        self.cut_minutes_button = QtWidgets.QRadioButton(self)
        self.cut_minutes_button.setText("Per Menit")
        self.cut_minutes_button.move(200, 240)

        # create labels and line edits for start and end time
        self.start_label = QtWidgets.QLabel(self)
        self.start_label.setText("Waktu Mulai")
        self.start_label.move(20, 300)

        self.start_edit = QtWidgets.QLineEdit(self)
        self.start_edit.move(100, 300)
        self.start_edit.resize(100, 30)

        self.end_label = QtWidgets.QLabel(self)
        self.end_label.setText("Waktu Selesai")
        self.end_label.move(220, 300)

        self.end_edit = QtWidgets.QLineEdit(self)
        self.end_edit.move(300, 300)
        self.end_edit.resize(100, 30)

        # create button to cut video
        self.cut_button = QtWidgets.QPushButton(self)
        self.cut_button.setText("Mulai Cut Video!")
        self.cut_button.move(100, 360)
        self.cut_button.resize(300, 30)
        self.cut_button.clicked.connect(self.cut_video)

        # create button to Informasi
        self.informasi_button = QtWidgets.QPushButton(self)
        self.informasi_button.setText("Informasi")
        self.informasi_button.move(100, 400)
        self.informasi_button.resize(300, 30)
        self.informasi_button.clicked.connect(self.informasi)

    def browse_input_file(self):
        """Browse input file"""
        file_name, _ = QFileDialog.getOpenFileName(self, "Pilih File Video", "", "Format Video (*.mp4)")
        self.input_file_edit.setText(file_name)
        self.get_duration()

    def browse_output_folder(self):
        """Browse output folder"""
        # Get the file name from the input file line edit
        input_file = self.input_file_edit.text()

        # Get the path to the input file
        path = os.path.dirname(input_file)

        # Create a default file name for the output file
        default_output_file_name = os.path.basename(input_file).split('.')[0] + '_terpotong.mp4'

        # Join the default file name with the output folder path to create the default output file path
        default_output_file_path = os.path.join(self.output_folder_edit.text(), default_output_file_name)

        # Open the file dialog to select the output file
        output_file, _ = QFileDialog.getSaveFileName(self, "Save Video File", default_output_file_path,
                                                     "Video Files (*.mp4)")

        # Set the output folder line edit text to the selected output file's directory
        self.output_folder_edit.setText(os.path.dirname(output_file))

    def get_duration(self):
        """Get duration of input video"""
        input_file = self.input_file_edit.text()
        if os.path.isfile(input_file):
            video = VideoFileClip(input_file)
            duration = int(video.duration)
            minutes = duration // 60
            seconds = duration % 60
            self.duration_text.setText("{} Menit {} Detik".format(minutes, seconds))
        else:
            self.duration_text.setText("")

    def cut_video(self):
        """Cut video based on user input"""
        input_file = self.input_file_edit.text()
        output_folder = self.output_folder_edit.text()
        start_time = self.start_edit.text()
        end_time = self.end_edit.text()

        if os.path.isfile(input_file) and os.path.isdir(output_folder) and start_time != "" and end_time != "":
            video = VideoFileClip(input_file)
            if self.cut_seconds_button.isChecked():
                start_time = float(start_time)
                end_time = float(end_time)
            else:
                start_time = float(start_time) * 60
                end_time = float(end_time) * 60

            # Get the name of the output file from the input file name and add the '_terpotong' suffix
            output_file_name = os.path.basename(input_file).split('.')[0] + '_terpotong.mp4'

            # Join the output folder path and the output file name to create the full output file path
            output_file_path = os.path.join(output_folder, output_file_name)

            video = video.subclip(start_time, end_time)
            video.write_videofile(output_file_path)

            QtWidgets.QMessageBox.information(self, "Berhasil", "Video Berhasil Di Cut.")
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Silahkan Masukan File Video Yang Ingin Di Cut, "
                                                         "Folder Untuk Menyimpan Hasil Yang Sudah Di cut,"
                                                         "waktu mulai dan waktu selesai.")

    def informasi(self):
        mbox.showinfo("Informasi Penggunaan", "1. Aplikasi ini digunakan untuk memotong video dengan format .mp4.\n\n"
                                              "2. Silahkan masukan file video yang ingin di potong, folder untuk "
                                              "menyimpan hasil cut video.\n\n"
                                              "3. waktu mulai dan waktu selesai cut video, "
                                              "lalu klik tombol mulai cut video.\n\n"
                                              "4. Untuk memotong video per detik, pilih radio button per detik, "
                                              "jika ingin memotong video per menit.\n\n"
                                              "5. pilih radio button per menit.\n\n"
                                              "6. Hasil cut video akan disimpan dengan nama file yang sama "
                                              "dengan file video yang di cut.\n\n"
                                              "7. dengan tambahan suffix '_terpotong'.\n\n"
                                              "8. Contoh: video.mp4 akan menjadi video_terpotong.mp4.\n\n"
                                              "9. Jika ingin memotong video per menit, masukan waktu mulai dan waktu "
                                              "selesai dalam satuan menit.\n" "Contoh: 1.5 menit, masukan 1.5.\n\n"
                                              "10. Jika ingin memotong video per detik, masukan waktu mulai dan waktu "
                                              "selesai dalam satuan detik.\n" "Contoh: 90 detik, masukan 90.\n\n"
                                              "Developer: Ahmad Bujay Rimi | Enjay Studio\n"
                                              "Teknik Informatika, Universitas Esa Unggul")


# Class Untuk Download Video Facebook
class VideoFacebookDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.resize(450, 200)
        # Fix Size
        self.setFixedSize(450, 200)
        self.move(300, 300)
        self.setWindowTitle('Video Facebook Downloader')
        self.setWindowIcon(QtGui.QIcon(':/Logo.png'))

        self.label1 = QLabel('URL Facebook:')
        self.url_edit = QLineEdit()
        self.label2 = QLabel('Simpan Ke:')
        self.path_edit = QLineEdit()
        self.path_edit.setReadOnly(True)
        self.browse_button = QPushButton('Buka Folder')
        self.browse_button.clicked.connect(self.browse_path)
        self.download_button = QPushButton('Mulai Download Video Facebook!')
        self.download_button.clicked.connect(self.download_video)
        self.informasi_button = QPushButton('Informasi')
        self.informasi_button.clicked.connect(self.informasi)

        grid = QGridLayout()
        grid.addWidget(self.label1, 0, 0)
        grid.addWidget(self.url_edit, 0, 1)
        grid.addWidget(self.label2, 1, 0)
        grid.addWidget(self.path_edit, 1, 1)
        grid.addWidget(self.browse_button, 1, 2)
        grid.addWidget(self.download_button, 2, 1)
        grid.addWidget(self.informasi_button, 3, 1)

        self.setLayout(grid)

    def browse_path(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Pilih Folder')
        self.path_edit.setText(folder_path)

    def download_video(self):
        url = self.url_edit.text()
        path = self.path_edit.text()

        ydl_opts = {'outtmpl': os.path.join(path, '%(title)s.%(ext)s')}

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading..." + url)
            ydl.download([url])

        QMessageBox.information(self, 'Download Selesai', 'Video Facebook Sudah Di Download')

    def informasi(self):
        mbox.showinfo("Informasi Penggunaan", "1. Aplikasi ini digunakan untuk mendownload video dari facebook.\n\n" 
                                              "2. Silahkan masukan url video facebook yang ingin di download, "
                                              "lalu pilih folder untuk menyimpan hasil download video.\n\n" 
                                              "3. Klik tombol download untuk memulai proses download video.\n" 
                                              "4. Jika proses selesai, maka akan muncul pesan "
                                              "'Video Facebook Sudah Di Download'.\n\n"
                                              "Note: \n"
                                              "1. Harus Terhubung Dengan Internet.\n\n" 
                                              "Developer: Ahmad Bujay Rimi | Enjay Studio\n" 
                                              "Teknik Informatika, Universitas Esa Unggul")


# Class Untuk Download Profile Instagram
class InstagramDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.resize(450, 200)
        # Fix Size
        self.setFixedSize(450, 200)
        self.move(300, 300)
        self.setWindowTitle('Instagram Proile Downloader')
        self.setWindowIcon(QtGui.QIcon(':/Logo.png'))

        self.label1 = QLabel('Nama Profile:')
        self.profile_edit = QLineEdit()
        self.label2 = QLabel('Simpan Ke:')
        self.folder_label = QLineEdit()
        self.folder_label.setReadOnly(True)
        self.folder_button = QPushButton('Buka Folder')
        self.folder_button.clicked.connect(self.pilih_folder)
        self.download_button = QPushButton('Mulai Download Profile Instagram!')
        self.download_button.clicked.connect(self.download)
        self.informasi_button = QPushButton('Informasi')
        self.informasi_button.clicked.connect(self.informasi)

        grid = QGridLayout()
        grid.addWidget(self.label1, 0, 0)
        grid.addWidget(self.profile_edit, 0, 1)
        grid.addWidget(self.label2, 1, 0)
        grid.addWidget(self.folder_label, 1, 1)
        grid.addWidget(self.folder_button, 1, 2)
        grid.addWidget(self.download_button, 2, 1)
        grid.addWidget(self.informasi_button, 3, 1)

        self.setLayout(grid)

    def pilih_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Pilih Folder')
        self.folder_label.setText('Folder: ' + folder_path)

    def download(self):
        profile_name = self.profile_edit.text()
        if not profile_name:
            QMessageBox.warning(self, 'Peringatan', 'Silahkan masukan nama profile.')
            return

        folder_path = self.folder_label.text()[15:]
        if not folder_path:
            QMessageBox.warning(self, 'Peringatan', 'Silahkan pilih folder untuk menyimpan hasil download.')
            return

        print("Downloading profile picture and videos of " + profile_name)
        L = instaloader.Instaloader(dirname_pattern=os.path.join(folder_path, profile_name))
        profile = instaloader.Profile.from_username(L.context, profile_name)

        for post in profile.get_posts():
            L.download_post(post, target=profile.username)

        QMessageBox.information(self, 'Berhasil', 'Video dan Foto Proile Sudah Di Download.')

    def informasi(self):
        mbox.showinfo("Informasi Penggunaan", "1. Aplikasi ini digunakan untuk mendownload video dan foto dari "
                                              "profile instagram.\n\n" 
                                              "2. Silahkan masukan nama profile instagram yang ingin di download, "
                                              "lalu pilih folder untuk menyimpan hasil download video.\n\n" 
                                              "3. Klik tombol download untuk memulai proses download video.\n\n"
                                              "4. Jika proses download sudah selesai, maka akan muncul pesan, "
                                              "Video dan Foto Proile Sudah Di Download.\n\n"
                                              "Note: \n"
                                              "1. Tidak Bisa Download, Jika Profile Bersifat Private.\n"
                                              "2. Harus Terhubung Dengan Internet.\n\n" 
                                              "Developer: Ahmad Bujay Rimi | Enjay Studio\n" 
                                              "Teknik Informatika, Universitas Esa Unggul")


# Class untuk menggabungkan video
class Combine_Video(QMainWindow):
    def __init__(self):
        super().__init__()
        self.video_list = []
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 392, 360)
        self.setWindowTitle('Menggabungkan Video')
        self.setWindowIcon(QtGui.QIcon(':/Logo.png'))
        # Fix Size
        self.setFixedSize(392, 360)

        self.video_count_label = QLabel('Jumlah Video: 0', self)
        self.video_count_label.move(20, 20)

        self.video_listbox = QListWidget(self)
        self.video_listbox.setGeometry(20, 50, 350, 100)

        self.add_video_button = QPushButton('Tambah Video', self)
        self.add_video_button.setGeometry(20, 160, 350, 30)
        self.add_video_button.clicked.connect(self.add_video)

        self.combine_button = QPushButton('Mulai Gabungkan Video!', self)
        self.combine_button.setGeometry(20, 270, 350, 30)
        self.combine_button.clicked.connect(self.combine_video)

        self.folder_label = QLabel('Simpan Ke:', self)
        self.folder_label.move(20, 200)

        self.folder_path_label = QLabel('', self)
        self.folder_path_label.setGeometry(85, 205, 300, 20)

        self.folder_button = QPushButton('Buka Folder', self)
        self.folder_button.setGeometry(20, 230, 350, 30)
        self.folder_button.clicked.connect(self.choose_folder)

        self.informasi_button = QPushButton('Informasi', self)
        self.informasi_button.setGeometry(20, 315, 350, 30)
        self.informasi_button.clicked.connect(self.informasi)

    def add_video(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Pilih Video', '', 'Video Files (*.mp4)')
        if file_path:
            self.video_list.append(file_path)
            self.video_count_label.setText(f'Jumlah Video: {len(self.video_list)}')
            self.video_listbox.addItem(os.path.basename(file_path))

    def choose_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Pilih Folder Simpan')
        if folder_path:
            self.folder_path_label.setText(folder_path)

    def combine_video(self):
        if len(self.video_list) == 0:
            return

        if not self.folder_path_label.text():
            return

        file_name = os.path.splitext(os.path.basename(self.video_list[0]))[0]
        output_path = os.path.join(self.folder_path_label.text(), f'{file_name}_tergabung.mp4')

        clips = [mp.VideoFileClip(v) for v in self.video_list]
        final_clip = mp.concatenate_videoclips(clips)

        final_clip.write_videofile(output_path)
        final_clip.close()

        self.video_list = []
        self.video_count_label.setText('Jumlah Video: 0')
        self.video_listbox.clear()
        self.folder_path_label.setText('')
        QMessageBox.information(self, 'Berhasil', 'Video Sudah Di Gabungkan Menjadi Satu.')

    def informasi(self):
        mbox.showinfo("Informasi Penggunaan", "1. Pilih video yang akan digabungkan. \n\n"
                                              "2. Pilih folder hasil video. \n\n"
                                              "3. Klik tombol 'gabungkan video'. \n\n"
                                              "4. Tunggu hingga muncul notifikasi "
                                              "'Video Sudah Di Gabungkan Menjadi Satu'. \n\n"
                                              "5. Video yang sudah digabungkan akan "
                                              "tersimpan di folder hasil video. \n\n"
                                              "6. Jika ingin menggabungkan video lagi, klik tombol 'Tambah Video' "
                                              "dan pilih video yang akan digabungkan. \n\n" 
                                              "Note: \n"
                                              "1. Harus Terhubung Dengan Internet.\n\n"
                                              "Developer: Ahmad Bujay Rimi | Enjay Studio\n"
                                              "Teknik Informatika, Universitas Esa Unggul")


# Class Untuk Menghapus Background Foto
class RemoveBackgroundImage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hapus Background Foto (Beta)")
        # self.setFixedSize(340, 600)
        self.setFixedSize(340, 600)
        self.setWindowIcon(QtGui.QIcon(':/Logo.png'))

        # Input gambar
        self.image_label = QLabel(self)
        self.image_label.move(20, 20)
        self.image_label.resize(300, 300)

        self.image_button = QPushButton("Pilih Gambar", self)
        self.image_button.move(20, 370)
        self.image_button.resize(300, 30)
        self.image_button.clicked.connect(self.choose_image)

        self.image_path = QLineEdit(self)
        self.image_path.move(20, 330)
        self.image_path.resize(300, 30)
        self.image_path.setReadOnly(True)

        # Folder hasil remove background
        self.output_path = QLineEdit(self)
        self.output_path.move(20, 420)
        self.output_path.resize(300, 30)
        self.output_path.setReadOnly(True)

        self.output_button = QPushButton("Buka Folder", self)
        self.output_button.move(20, 460)
        self.output_button.resize(300, 30)
        self.output_button.clicked.connect(self.choose_output_folder)

        # Tombol remove background
        self.remove_button = QPushButton("Mulai Hapus Background Foto!", self)
        self.remove_button.move(20, 520)
        self.remove_button.resize(300, 30)
        self.remove_button.clicked.connect(self.remove_background)

        # Tombol Informasi
        self.info_button = QPushButton("Informasi", self)
        self.info_button.move(20, 560)
        self.info_button.resize(300, 30)
        self.info_button.clicked.connect(self.informasi)

    def choose_image(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Pilih Foto", "", "Format Foto (*.png *.jpg *.bmp)")
        self.image_path.setText(filename)

        pixmap = QPixmap(filename)
        self.image_label.setPixmap(pixmap.scaled(300, 415, Qt.KeepAspectRatio))

    def choose_output_folder(self):
        folder_dialog = QFileDialog()
        folder_dialog.setFileMode(QFileDialog.DirectoryOnly)
        folder_dialog.exec_()
        folder_path = folder_dialog.selectedFiles()[0]
        self.output_path.setText(folder_path)

    def remove_background(self):
        image_path = self.image_path.text()
        output_path = self.output_path.text()
        if image_path and output_path:
            filename = os.path.basename(image_path)
            output_filename = os.path.splitext(filename)[0] + "_remove_bg.png"
            output_file_path = os.path.join(output_path, output_filename)
            with open(image_path, "rb") as image_file:
                with open(output_file_path, "wb") as output_file:
                    output_file.write(remove(image_file.read()))
            QMessageBox.information(self, "Berhasil", "Background Foto Sudah Di Hapus")
        else:
            QMessageBox.warning(self, "Peringatan", "Silakan pilih gambar dan folder output terlebih dahulu")

    def informasi(self):
        mbox.showinfo("Informasi Penggunaan", "1. Pilih Foto yang ingin dihapus backgroundnya.\n"
                                              "2. Pilih Folder untuk menyimpan hasil hapus background.\n"
                                              "3. Klik tombol 'Hapus Background Foto' "
                                              "untuk menghapus background foto.\n"
                                              "4. Tunggu hingga muncul notifikasi 'Background Foto Sudah Di Remove'.\n" 
                                              "5. Foto yang sudah dihapus backgroundnya akan tersimpan di folder yang "
                                              "telah dipilih sebelumnya.\n\n" 
                                              "Developer: Ahmad Bujay Rimi | Enjay Studio\n"
                                              "Teknik Informatika, Universitas Esa Unggul")


# Class Untuk Kompres Size Foto
class ImageCompressor(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle('Kompres Size Foto')
        self.setGeometry(100, 100, 400, 565)
        self.setWindowIcon(QtGui.QIcon(':/Logo.png'))
        self.setFixedSize(self.size())

        # Initialize instance variables
        self.image_path = ''
        self.output_path = ''
        self.image_width = ''
        self.image_height = ''
        self.quality = 85

        # Create widgets
        self.image_label = QLabel(self)
        self.image_label.setGeometry(110, 12, 200, 200)

        self.image_button = QPushButton('Buka File', self)
        self.image_button.setGeometry(20, 260, 360, 30)
        self.image_button.clicked.connect(self.select_image)

        self.image_path_label = QLineEdit(self)
        self.image_path_label.setGeometry(20, 222, 360, 30)
        self.image_path_label.setReadOnly(True)

        self.Width_height_label = QLabel('Masukkan Lebar Dan Tinggi Foto Kalian: ', self)
        self.Width_height_label.setGeometry(20, 288, 360, 30)

        self.width_label = QLabel('Lebar:', self)
        self.width_label.setGeometry(20, 318, 50, 30)
        self.width_input = QLineEdit(self)
        self.width_input.setGeometry(70, 318, 100, 30)
        self.width_input.textChanged[str].connect(self.set_width)

        self.height_label = QLabel('Tinggi:', self)
        self.height_label.setGeometry(230, 318, 50, 30)
        self.height_input = QLineEdit(self)
        self.height_input.setGeometry(280, 318, 100, 30)
        self.height_input.textChanged[str].connect(self.set_height)

        self.quality_label = QLabel('Kualitas:', self)
        self.quality_label.setGeometry(20, 350, 50, 30)
        self.quality_slider = QSlider(Qt.Horizontal, self)
        self.quality_slider.setGeometry(70, 358, 280, 30)
        self.quality_slider.setTickPosition(QSlider.TicksBelow)
        self.quality_slider.setTickInterval(5)
        self.quality_slider.setMaximum(100)
        self.quality_slider.setValue(self.quality)
        self.quality_slider.valueChanged.connect(self.set_quality)

        # Create Label to show the value of the slider
        self.quality_value_label = QLabel(str(self.quality) + " %", self)
        self.quality_value_label.setGeometry(358, 350, 50, 30)

        self.output_button = QPushButton('Buka Folder', self)
        self.output_button.setGeometry(20, 440, 360, 30)
        self.output_button.clicked.connect(self.select_output_path)

        self.output_path_label = QLineEdit(self)
        self.output_path_label.setGeometry(20, 400, 360, 30)
        self.output_path_label.setReadOnly(True)

        self.compress_button = QPushButton('Mulai Kompres Size Foto!', self)
        self.compress_button.setGeometry(20, 480, 360, 30)
        self.compress_button.clicked.connect(self.compress_image)

        self.informasi_button = QPushButton('Informasi', self)
        self.informasi_button.setGeometry(20, 520, 360, 30)
        self.informasi_button.clicked.connect(self.informasi)

    def select_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, 'Pilih Foto', '', 'Format Foto (*.png *.jpg)')
        if file_name:
            self.image_path = file_name
            pixmap = QPixmap(self.image_path)
            # self.image_label.setPixmap(pixmap)
            self.image_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
            self.image_path_label.setText(self.image_path)

    def select_output_path(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog | QFileDialog.ShowDirsOnly
        folder_path = QFileDialog.getExistingDirectory(self, 'Pilih Folder Simpan')
        if folder_path:
            self.output_path = folder_path
            self.output_path_label.setText(self.output_path)

            # Create quality label and slider
            quality_label = QLabel('Kualitas:', self)
            quality_label.setGeometry(20, 400, 50, 30)
            self.quality_slider = QSlider(Qt.Horizontal, self)
            self.quality_slider.setGeometry(70, 400, 200, 30)
            self.quality_slider.setMinimum(0)
            self.quality_slider.setMaximum(100)
            self.quality_slider.setValue(85)
            self.quality_slider.setTickPosition(QSlider.TicksBelow)
            self.quality_slider.setTickInterval(10)
            self.quality_slider.valueChanged.connect(self.set_quality)

    def set_width(self, value):
        self.image_width = value

    def set_height(self, value):
        self.image_height = value

    def set_quality(self, value):
        self.quality = value
        self.quality_value_label.setText(str(self.quality) + " %")

    def compress_image(self):
        if not self.image_path:
            QMessageBox.warning(self, 'Peringatan', 'Tolong Masukkan Foto Anda')
            return
        if not self.image_width or not self.image_height:
            QMessageBox.warning(self, 'Peringatan', 'Tolong Masukkan Lebar Dan Tinggi Foto Anda')
            return
        if not self.output_path:
            QMessageBox.warning(self, 'Peringatan', 'Tolong Masukkan Folder Yang Ingin Di Simpan')
            return

        try:
            # Validate width and height input
            try:
                width = int(self.width_input.text())
                height = int(self.height_input.text())
            except ValueError:
                QMessageBox.warning(self, 'Peringatan', 'Tolong Masukkan Angka Lebar Dan Tinggi Foto Anda')
                return
            if width <= 0 or height <= 0:
                QMessageBox.warning(self, 'Peringatan', 'Tolong Masukkan Angka Lebar Dan Tinggi Foto Anda')
                return
            if width > 12000 or height > 16000:
                QMessageBox.warning(self, 'Peringatan', 'Lebar dan Tinggi Foto Tidak Boleh Melebihi 12000 dan 16000')
                return

            # Open the image and resize it
            with Image.open(self.image_path) as img:
                img = img.resize((width, height), PIL.Image.ANTIALIAS)

                # Save the compressed image to the output folder
                filename, extension = os.path.splitext(os.path.basename(self.image_path))
                output_file_path = os.path.join(self.output_path, f"{filename}_compressed{extension}")
                img.save(output_file_path, optimize=True, quality=self.quality)

                # Show a success message
                QMessageBox.information(self, 'Berhasil', 'Size Foto Berhasil Di Kompres')
        except Exception as e:
            QMessageBox.warning(self, 'Peringatan', f'Terjadi Kesalahan Saat Mengompresi Foto: {e}')

    def informasi(self):
        mbox.showinfo("Informasi Penggunaan", "1. Pilih Foto yang akan di kompress ukurannya.\n"
                                              "2. Masukkan ukuran foto yang diinginkan.\n"
                                              "3. 'Pilih folder simpan' foto yang sudah dikompress.\n"
                                              "4. Tekan tombol kompress foto.\n"
                                              "5. Selesai.\n\n"
                                              "Developer: Ahmad Bujay Rimi | Enjay Studio\n"
                                              "Teknik Informatika, Universitas Esa Unggul")


# Class Untuk Mengubah Resolusi dan Frame Rate Video
class ChangeResolusiAndFrame(QWidget):
    def __init__(self):
        super().__init__()

        # set window properties
        self.setGeometry(100, 100, 580, 370)
        self.setWindowTitle("Ganti Resolusi dan Frame Rate Video")
        self.setWindowIcon(QtGui.QIcon(':/Logo.png'))
        # Size Fixed
        self.setFixedSize(self.size())

        # create labels
        self.video_label = QLabel("File Video:", self)
        self.video_label.setGeometry(20, 20, 100, 30)

        self.fps_label = QLabel("Frame Rate:", self)
        self.fps_label.setGeometry(20, 80, 100, 30)

        self.resolution_label = QLabel("Resolusi Video:", self)
        self.resolution_label.setGeometry(20, 140, 100, 30)

        self.output_label = QLabel("Simpan Ke:", self)
        self.output_label.setGeometry(20, 210, 100, 30)

        # create line edit widgets
        self.video_path = QLineEdit(self)
        self.video_path.setGeometry(120, 20, 350, 30)
        self.video_path.setReadOnly(True)

        self.output_path = QLineEdit(self)
        self.output_path.setGeometry(120, 210, 350, 30)
        self.output_path.setReadOnly(True)

        # create buttons
        self.browse_video_btn = QPushButton("Pilih File", self)
        self.browse_video_btn.setGeometry(480, 20, 80, 30)
        self.browse_video_btn.clicked.connect(self.browse_video)

        self.browse_output_btn = QPushButton("Pilih Folder", self)
        self.browse_output_btn.setGeometry(480, 210, 80, 30)
        self.browse_output_btn.clicked.connect(self.browse_output)

        self.convert_btn = QPushButton("Mulai Convert Resolusi dan Frame Rate Video!", self)
        self.convert_btn.setGeometry(120, 270, 350, 30)
        self.convert_btn.clicked.connect(self.convert_video)

        self.cancel_btn = QPushButton("Informasi", self)
        self.cancel_btn.setGeometry(120, 315, 350, 30)
        self.cancel_btn.clicked.connect(self.informasi)

        # create slider widget for fps
        self.fps_slider = QSlider(Qt.Horizontal, self)
        self.fps_slider.setGeometry(120, 80, 350, 30)
        self.fps_slider.setMinimum(0)
        self.fps_slider.setMaximum(120)
        self.fps_slider.setTickPosition(QSlider.TicksBelow)
        self.fps_slider.setTickInterval(5)
        self.fps_slider.setValue(15)
        self.fps_slider.valueChanged.connect(self.show_fps_value)

        self.fps_value_label = QLabel("15% (fps)", self)
        self.fps_value_label.setGeometry(480, 80, 80, 30)

        # create combo box for resolution
        self.resolution_combo = QComboBox(self)
        self.resolution_combo.setGeometry(120, 140, 350, 30)
        self.resolution_combo.addItem("240p (SD)")
        self.resolution_combo.addItem("360p (SD)")
        self.resolution_combo.addItem("480p (SD)")
        self.resolution_combo.addItem("720p (HD)")
        self.resolution_combo.addItem("1080p (HD)")
        self.resolution_combo.addItem("1440p (2k)")
        self.resolution_combo.addItem("2160p (4k)")

    def browse_video(self):
        # open file dialog to select video file
        filename, _ = QFileDialog.getOpenFileName(self, "File Video", "", "Format Video (*.mp4 *.mov *.avi *.mkv)")
        # set the video file path to the line edit widget
        self.video_path.setText(filename)

    def browse_output(self):
        # open file dialog to select output file path
        directory = QFileDialog.getExistingDirectory(self, "Pilih Folder Simpan")
        # set the output file path to the line edit widget
        self.output_path.setText(directory)

    def show_fps_value(self):
        # update fps value label when slider value is changed
        fps = self.fps_slider.value()
        self.fps_value_label.setText(str(fps) + "% (fps)")

    def convert_video(self):
        # get the input and output file paths
        input_file = self.video_path.text()
        output_folder = self.output_path.text()

        # check if the input file path is empty
        if not input_file:
            QMessageBox.warning(self, "Peringatan", "Tolong Masukkan Video Yang Ingin Kamu Convert")
            return

        # check if the output file path is empty
        if not output_folder:
            QMessageBox.warning(self, "Peringatan", "Tolong Masukkan Directory/Folder Yang Ingin "
                                                    "Kamu Simpan Hasil Convert Video")
            return

        # get the selected fps and resolution
        fps = self.fps_slider.value()
        resolution = self.resolution_combo.currentText()

        # get the dimensions based on the selected resolution
        dimensions = {
            "240p (SD)": (426, 240),
            "360p (SD)": (640, 360),
            "480p (SD)": (854, 480),
            "720p (HD)": (1280, 720),
            "1080p (HD)": (1920, 1080),
            "1440p (2k)": (2560, 1440),
            "2160p (4k)": (3840, 2160)
        }

        # get the dimensions based on the selected resolution
        width, height = dimensions[resolution]

        # create ffmpeg command to convert the video
        output_file = os.path.join(output_folder, os.path.splitext(os.path.basename(input_file))[0] +
                                   "_ganti_resolusi_dan_frame_rate.mp4")
        command = f"ffmpeg -i \"{input_file}\" -vf scale={width}:{height} -r {fps} \"{output_file}\""

        # execute the command
        os.system(command)

        # show success message box
        QMessageBox.information(self, "Berhasil", "Resolusi dan Frame Rate Video Anda Sudah Dirubah")

    def informasi(self):
        mbox.showinfo("Informasi Penggunaan", "1. Pilih Video yang akan diubah resolusinya.\n"
                                              "2. Pilih Folder untuk menyimpan hasil konversi.\n"
                                              "3. Pilih Resolusi Video yang diinginkan.\n"
                                              "4. Pilih Frame Rate yang diinginkan.\n"
                                              "5. Klik Convert untuk memulai proses konversi.\n"
                                              "6. Tunggu sampai muncul notifikasi "
                                              "'Resolusi dan Frame Rate Video Anda Sudah Dirubah'.\n"
                                              "7. Hasil konversi akan tersimpan di "
                                              "folder yang telah dipilih sebelumnya.\n"
                                              "8. Selesai.\n\n" 
                                              "Note: \n"
                                              "Tidak Rekomendasikan untuk mengubah frame rate Kecil ke Besar.\n\n"
                                              "Developer: Ahmad Bujay Rimi | Enjay Studio\n"
                                              "Teknik Informatika, Universitas Esa Unggul")


# Class Untuk Merubah Video Ke Per Frame Foto
class VideoToImageConverter(QWidget):
    def __init__(self):
        super().__init__()

        self.video_path = ''
        self.output_path = ''

        self.setWindowTitle('Merubah Video Ke Per Frame Foto')
        self.setGeometry(100, 100, 600, 200)
        self.setWindowIcon(QtGui.QIcon(':/Logo.png'))
        # Size Fixed
        self.setFixedSize(600, 200)

        self.video_label = QLabel(self)
        self.video_label.setText('File Video:')
        self.video_label.setGeometry(50, 30, 100, 30)

        self.video_line_edit = QLineEdit(self)
        self.video_line_edit.setGeometry(150, 30, 300, 30)
        # ReadOnly
        self.video_line_edit.setReadOnly(True)

        self.video_button = QPushButton(self)
        self.video_button.setText('Buka File')
        self.video_button.setGeometry(470, 30, 100, 30)
        self.video_button.clicked.connect(self.choose_video)

        self.output_label = QLabel(self)
        self.output_label.setText('Simpan Ke: ')
        self.output_label.setGeometry(50, 70, 100, 30)

        self.output_line_edit = QLineEdit(self)
        self.output_line_edit.setGeometry(150, 70, 300, 30)
        # ReadOnly
        self.output_line_edit.setReadOnly(True)

        self.output_button = QPushButton(self)
        self.output_button.setText('Buka Folder')
        self.output_button.setGeometry(470, 70, 100, 30)
        self.output_button.clicked.connect(self.choose_output)

        self.convert_button = QPushButton(self)
        self.convert_button.setText(' Mulai Convert Video Ke Per Frame Foto!')
        self.convert_button.setGeometry(150, 120, 300, 30)
        self.convert_button.clicked.connect(self.convert)

        self.informasi_button = QPushButton(self)
        self.informasi_button.setText('Informasi')
        self.informasi_button.setGeometry(150, 160, 300, 30)
        self.informasi_button.clicked.connect(self.informasi)

    def choose_video(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(self, 'Pilih Video', '', 'Format Video (*.mp4)')
        if file_path:
            self.video_path = file_path
            self.video_line_edit.setText(self.video_path)

    def choose_output(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dir_path = QFileDialog.getExistingDirectory(self, 'Pilih Folder Simpan')
        if dir_path:
            self.output_path = dir_path
            self.output_line_edit.setText(self.output_path)

    def convert(self):
        if not self.video_path:
            QMessageBox.warning(self, 'Peringatan', 'Tolong Masukkan File Video Yang Ingin Di Convert')
            return

        if not self.output_path:
            QMessageBox.warning(self, 'Peringatan', 'Tolong Masukkan Folder Tujuan Simpan')
            return

        vid = cv2.VideoCapture(self.video_path)

        try:
            if not os.path.exists(self.output_path):
                os.makedirs(self.output_path)
        except OSError:
            QMessageBox.warning(self, 'Peringatan', 'Gagal Membuat Folder Tujuan Simpan')
            return

        currentframe = 0

        while True:
            success, frame = vid.read()
            if success:
                name = os.path.join(self.output_path, 'frame_' + str(currentframe) + '.jpg')
                cv2.imwrite(name, frame)
                currentframe += 1
            else:
                break

        vid.release()
        # cv2.destroyAllWindows()

        QMessageBox.information(self, 'Berhasil', 'Video Sudah Terekstrak Menjadi Beberapa Per - Frame Foto')

    def informasi(self):
        mbox.showinfo("Informasi Penggunaan", "1. Pilih Video yang akan di konversi ke foto.\n"
                                              "2. Pilih Folder untuk menyimpan foto hasil konversi.\n"
                                              "3. Klik tombol Convert untuk memulai proses konversi.\n"
                                              "4. Tunggu hingga muncul notifikasi "
                                              "'Video Sudah Terekstrak Menjadi Beberapa Per - Frame Foto'.\n" 
                                              "5. Selesai.\n" 
                                              "6. Hasil konversi akan tersimpan di folder yang telah dipilih.\n\n" 
                                              "Note: \n"
                                              "Pilih folder yang kosong untuk menyimpan hasil konversi.\n\n" 
                                              "Developer: Ahmad Bujay Rimi | Enjay Studio\n"
                                              "Teknik Informatika, Universitas Esa Unggul")


# Class Untuk Merubah Per Frame Foto Ke Video
class ImageToVideoGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Set the window title
        self.setWindowTitle('Convert Foto ke Video (Tahap Pengembangan)')

        # Set the window dimensions
        self.setGeometry(100, 100, 500, 300)
        # Fixed Size
        self.setFixedSize(500, 300)
        self.setWindowIcon(QtGui.QIcon(':/Logo.png'))

        # Add a label for the input folder path
        input_label = QLabel('Folder Foto:', self)
        input_label.setGeometry(20, 50, 100, 30)

        # Add a line edit to display the input folder path
        self.input_line_edit = QLineEdit(self)
        # ReadOnly
        self.input_line_edit.setReadOnly(True)
        self.input_line_edit.setGeometry(110, 50, 250, 30)

        # Add a button to select the input folder
        input_button = QPushButton('Buka Folder', self)
        input_button.setGeometry(380, 50, 100, 30)
        input_button.clicked.connect(self.select_input_folder)

        # Add a label for the output folder path
        output_label = QLabel('Simpan Ke:', self)
        output_label.setGeometry(20, 100, 100, 30)

        # Add a line edit to display the output folder path
        self.output_line_edit = QLineEdit(self)
        # ReadOnly
        self.output_line_edit.setReadOnly(True)
        self.output_line_edit.setGeometry(110, 100, 250, 30)

        # Add a button to select the output folder
        output_button = QPushButton('Buka Folder', self)
        output_button.setGeometry(380, 100, 100, 30)
        output_button.clicked.connect(self.select_output_folder)

        # Add a label for frame rate video
        fps_label = QLabel('Frame Rate:', self)
        fps_label.setGeometry(20, 150, 100, 30)

        # Add a slider for frame rate video
        self.fps_slider = QSlider(self)
        self.fps_slider.setOrientation(Qt.Horizontal)
        self.fps_slider.setGeometry(110, 160, 250, 20)
        self.fps_slider.setTickPosition(QSlider.TicksBelow)
        self.fps_slider.setTickInterval(5)
        self.fps_slider.setMinimum(0)
        self.fps_slider.setMaximum(60)
        self.fps_slider.setValue(30)

        # Add a label for slider value
        self.slider_value_label = QLabel('30%', self)
        self.slider_value_label.setGeometry(370, 150, 50, 30)

        # Add a button to start the conversion process
        convert_button = QPushButton('Mulai Convert Foto Ke Video!', self)
        convert_button.setGeometry(110, 210, 250, 30)
        convert_button.clicked.connect(self.convert_images_to_video)

        # Add a button to informasi
        info_button = QPushButton('Informasi', self)
        info_button.setGeometry(110, 260, 250, 30)
        info_button.clicked.connect(self.informasi)

        # Connect the fps slider to the function that updates the label
        self.fps_slider.valueChanged.connect(self.update_fps_label)

    def select_input_folder(self):
        # Open a file dialog to select the input folder
        input_folder = QFileDialog.getExistingDirectory(self, 'Pilih folder input Foto')

        # Set the input folder path in the line edit
        self.input_line_edit.setText(input_folder)

    def select_output_folder(self):
        # Open a file dialog to select the output folder
        output_folder = QFileDialog.getExistingDirectory(self, 'Pilih Folder Simpan')

        # Set the output folder path in the line edit
        self.output_line_edit.setText(output_folder)

    def update_fps_label(self, value):
        # Update the label text with the new value
        self.slider_value_label.setText(f'{value}%')

    def convert_images_to_video(self):
        input_folder = self.input_line_edit.text()
        output_folder = self.output_line_edit.text()
        fps = self.fps_slider.value()

        # Check if the input folder path is valid
        if not os.path.isdir(input_folder):
            QMessageBox.warning(self, 'Peringatan', 'Tolong Pilih Folder Yang Anda Ingin Konversi')
            return

        # Check if the output folder path is valid
        if not os.path.isdir(output_folder):
            QMessageBox.warning(self, 'Peringatan', 'Tolong Pilih Folder Yang Anda Ingin Simpan')
            return

        # Get the list of image files in the input folder
        image_files = [f for f in os.listdir(input_folder) if f.endswith('.jpg') or f.endswith('.png')]

        # Sort the image files alphabetically
        image_files.sort()

        # Check if there are any image files in the input folder
        if not image_files:
            QMessageBox.warning(self, 'Peringatan', 'Folder Yang Anda Pilih Tidak Memiliki Foto.')
            return

        # Get the width and height of the first image
        image_path = os.path.join(input_folder, image_files[0])
        image = cv2.imread(image_path)
        height, width, channels = image.shape

        # Create the video writer object
        video_path = os.path.join(output_folder, '_gabungan_per_frame_foto.mp4')
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(video_path, fourcc, fps, (width, height))

        # Loop through the image files and write them to the video
        for image_file in image_files:
            image_path = os.path.join(input_folder, image_file)
            image = cv2.imread(image_path)

            # Check if the image is valid
            if image is None:
                continue

            # Resize the image to the video dimensions
            resized_image = cv2.resize(image, (width, height))

            # Write the image to the video
            video_writer.write(resized_image)

        # Release the video writer object and display a message box
        video_writer.release()
        QMessageBox.information(self, 'Berhasil', 'Per Frame Foto Berhasil Convert Ke Video')

    def informasi(self):
        mbox.showinfo("Informasi Penggunaan", "1. Pilih Folder Foto Yang Ingin Anda Convert Ke Video.\n"
                                              "2. Pilih Folder Simpan Video.\n"
                                              "3. Pilih Frame Rate Video.\n"
                                              "4. Klik Tombol Convert Foto Ke Video.\n" 
                                              "5. Tunggu Sampai Muncul Notifikasi "
                                              "'Per Frame Foto Berhasil Convert Ke Video'.\n" 
                                              "6. Video Berhasil Disimpan Di Folder Yang Anda Pilih.\n" 
                                              "7. Selesai.\n\n" 
                                              "Note: \n"
                                              "1. Jika Tidak Ada Foto Di Folder Yang Anda Pilih, "
                                              "Maka Aplikasi Akan Menampilkan Notifikasi "
                                              "'Folder Yang Anda Pilih Tidak Memiliki Foto'.\n"
                                              "2. Nama Per Frame Foto Harus Berurutan Dan Berakhiran "
                                              ".jpg Atau .png, Misalnya foto01, foto02, ...., foto1000\n\n" 
                                              "Developer: Ahmad Bujay Rimi | Enjay Studio\n"
                                              "Teknik Informatika, Universitas Esa Unggul")


# Class Untuk Spotify Downloader
class SpotifyDownloaderGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 600, 182)
        # Fixed Size
        self.setFixedSize(600, 182)
        self.setWindowTitle('Spotify Downloader (Tahap Pengembangan)')
        self.setWindowIcon(QtGui.QIcon(':/Logo.png'))

        self.label = QLabel('Link Spotify:', self)
        self.label.setGeometry(10, 20, 100, 30)

        self.lineEdit_spotify = QLineEdit(self)
        self.lineEdit_spotify.setGeometry(110, 20, 480, 30)

        self.label_folder = QLabel('Simpan Ke:', self)
        self.label_folder.setGeometry(10, 60, 100, 30)

        self.lineEdit_folder = QLineEdit(self)
        # Read Only
        self.lineEdit_folder.setReadOnly(True)
        self.lineEdit_folder.setGeometry(110, 60, 400, 30)

        self.button_folder = QPushButton('Buka Folder', self)
        self.button_folder.setGeometry(520, 60, 70, 30)
        self.button_folder.clicked.connect(self.browse_folder)

        self.button_download = QPushButton('Mulai Download Lagu Spotify!', self)
        self.button_download.setGeometry(110, 100, 400, 30)
        self.button_download.clicked.connect(self.download_music)

        self.button_informasi = QPushButton('Informasi', self)
        self.button_informasi.setGeometry(110, 138, 400, 30)
        self.button_informasi.clicked.connect(self.informasi)

    def browse_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Pilih Folder Simpan')
        self.lineEdit_folder.setText(folder_path)

    def download_music(self):
        global LOCATION
        LOCATION = self.lineEdit_folder.text()
        if not os.path.isdir(LOCATION):
            os.mkdir(LOCATION)

        SPOTIFY_PLAYLIST_LINK = self.lineEdit_spotify.text()
        OFFSET_VARIABLE = 0
        ID = returnSPOT_ID(SPOTIFY_PLAYLIST_LINK)

        headers = {
            'authority': 'api.spotifydown.com',
            'method': 'GET',
            'path': f'/trackList/playlist/{ID}',
            'scheme': 'https',
            'accept': '*/*',
            'dnt': '1',
            'origin': 'https://spotifydown.com',
            'referer': 'https://spotifydown.com/',
            'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }
        Playlist_Link = f'https://api.spotifydown.com/trackList/playlist/{ID}'

        session = requests.Session()

        offset_data = {}

        offset = OFFSET_VARIABLE
        page = 0
        offset_data['offset'] = offset

        response = session.get(url=Playlist_Link, headers=headers, params=offset_data)

        while offset != None:
            if response.status_code == 200:
                Tdata = response.json()['trackList']
                page = response.json()['nextOffset']
                for count, song in enumerate(Tdata):
                    yt_id = get_ID(session=session, id=song['id'])
                    if yt_id is not None:
                        filename = song['title'].translate(str.maketrans('', '', string.punctuation)) + ' - ' + song[
                            'artists'].translate(str.maketrans('', '', string.punctuation)) + '.mp3'
                        try:
                            data = generate_Analyze_id(session=session, yt_id=yt_id['id'])
                            DL_ID = data['links']['mp3']['mp3128']['k']
                            DL_DATA = generate_Conversion_id(session=session, analyze_yt_id=data['vid'],
                                                             analyze_id=DL_ID)
                            DL_LINK = DL_DATA['dlink']
                            link = session.get(DL_LINK)
                            with open(os.path.join(LOCATION, filename), 'wb') as f:
                                f.write(link.content)
                        except Exception as error_status:
                            print('[*] Error Status Code : ', error_status)
                            QMessageBox.warning(self, 'Peringatan', 'Terjadi kesalahan saat mengunduh musik')
                    else:
                        print('[*] No data found for : ', song)
            if page != None:
                offset_data['offset'] = page
                response = session.get(url=Playlist_Link, params=offset_data, headers=headers)
                offset = page  # Perbaikan: Tambahkan ini untuk menghentikan loop tak terbatas
            else:
                break

        QMessageBox.information(self, 'Berhasil', 'Musik Spotify sudah terdownload')

    def informasi(self):
        mbox.showinfo("Informasi Penggunaan", "1. Tempelkan tautan playlist Spotify yang ingin Anda unduh lagunya di "
                                              "bidang teks yang diberi label 'Link Spotify'\n\n"
                                              "2. Pilih folder tempat Anda ingin menyimpan lagu yang diunduh dengan "
                                              "mengklik tombol 'Pilih Folder' di samping bidang teks 'Pilih Folder "
                                              "Simpan'. Jendela dialog akan terbuka untuk memilih folder tujuan.\n\n"
                                              "3. Setelah memilih folder tujuan, klik tombol 'Download Lagu Spotify!' "
                                              "untuk memulai proses pengunduhan lagu.\n\n"
                                              "4. Program akan mengunduh lagu dari playlist Spotify yang diberikan dan "
                                              "menyimpannya dalam format MP3 di folder yang Anda pilih sebelumnya.\n\n" 
                                              "5. Jika terjadi kesalahan saat mengunduh musik, Anda akan melihat pesan "
                                              "peringatan dengan teks 'Terjadi kesalahan saat mengunduh musik'.\n\n" 
                                              "6. Setelah proses pengunduhan selesai, Anda akan melihat pesan "
                                              "informasi dengan teks 'Musik Spotify sudah terdownload'.\n\n" 
                                              "7. Selesai.\n\n" 
                                              "Note: \n"
                                              "1. Harus Terhubung Dengan Internet.\n" 
                                              "2. Aplikasi Spotify Harus Terbuka.\n\n"
                                              "Developer: Ahmad Bujay Rimi | Enjay Studio\n"
                                              "Teknik Informatika, Universitas Esa Unggul")


# Class Untuk Mengubah Video ke Teks
class VideoToText(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Mengubah Video ke Teks (Tahap Pengembangan)')
        self.setGeometry(100, 100, 510, 200)
        self.setWindowIcon(QtGui.QIcon(':/Logo.png'))
        # Fix window size
        self.setFixedSize(self.size())

        # QLabel, QLineEdit, and QPushButton for video input
        self.label1 = QLabel('File Video:', self)
        self.label1.setGeometry(20, 20, 100, 25)

        self.line_edit1 = QLineEdit(self)
        # Read only
        self.line_edit1.setReadOnly(True)
        self.line_edit1.setGeometry(120, 20, 300, 25)

        self.button1 = QPushButton('Pilih File', self)
        self.button1.setGeometry(430, 20, 70, 25)
        self.button1.clicked.connect(self.open_video_file)

        # QLabel, QLineEdit, and QPushButton for output folder
        self.label2 = QLabel('Simpen Ke:', self)
        self.label2.setGeometry(20, 60, 100, 25)

        self.line_edit2 = QLineEdit(self)
        # Read only
        self.line_edit2.setReadOnly(True)
        self.line_edit2.setGeometry(120, 60, 300, 25)

        self.button2 = QPushButton('Pilih Folder', self)
        self.button2.setGeometry(430, 60, 70, 25)
        self.button2.clicked.connect(self.open_output_folder)

        # QLabel and QComboBox for language selection
        self.label3 = QLabel('Bahasa Video:', self)
        self.label3.setGeometry(20, 95, 100, 25)

        self.language_combo = QComboBox(self)
        self.language_combo.addItems(["Indonesia", "Jepang", "Inggris", "Amerika", "Arab Saudi"])
        self.language_combo.setGeometry(120, 95, 150, 25)

        self.language_map = {
            "Indonesia": "id-ID",
            "Jepang": "ja-JP",
            "Inggris": "en-GB",
            "Amerika": "en-US",
            "Arab Saudi": "ar-SA"
        }

        # QPushButton for starting the extraction
        self.button3 = QPushButton('Mulai Extract Video Ke Text!', self)
        self.button3.setGeometry(120, 135, 300, 25)
        self.button3.clicked.connect(self.on_click)

        self.button4 = QPushButton('Informasi', self)
        self.button4.setGeometry(120, 167, 300, 25)
        self.button4.clicked.connect(self.informasi)

    def open_video_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Pilih Video", "", "Format Video (*.mp4 *.avi)",
                                                   options=options)
        if file_name:
            self.line_edit1.setText(file_name)

    def open_output_folder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        folder_name = QFileDialog.getExistingDirectory(self, "Pilih Folder Simpan", options=options)
        if folder_name:
            self.line_edit2.setText(folder_name)

    def on_click(self):
        video_path = self.line_edit1.text()
        output_folder = self.line_edit2.text()
        selected_language = self.language_map[self.language_combo.currentText()]

        if not video_path or not output_folder:
            QMessageBox.warning(self, "Peringatan", "Silakan pilih directory/lokasi video dan "
                                                    "folder untuk menyimpan hasil video ke text.")
            return

        video_name = os.path.splitext(os.path.basename(video_path))[0]
        text_path = os.path.join(output_folder, video_name + "_extract_ke_text.txt")
        audio_path = os.path.join(output_folder, video_name + "_extract_ke_audio.wav")

        self.extract_video_to_text(video_path, text_path, audio_path, selected_language)
        QMessageBox.information(self, "Berhasil", "Video sudah di extract ke dalam text.")

    def extract_video_to_text(self, video_path, text_path, audio_path, selected_language):
        try:
            # Konversi video ke audio
            video = mp.VideoFileClip(video_path)
            video.audio.write_audiofile(audio_path, codec='pcm_s16le', ffmpeg_params=["-ac", "1"])

            # Konversi audio ke teks
            recognizer = sr.Recognizer()

            with sr.AudioFile(audio_path) as source:
                text = ""
                duration = 10  # set durasi dalam detik
                total_duration = int(video.duration)
                for i in range(0, total_duration, duration):
                    audio = recognizer.record(source, duration=duration, offset=i)
                    try:
                        transcript = recognizer.recognize_google(audio, language=selected_language)
                        text += transcript + " "
                    except sr.UnknownValueError:
                        pass
                    except sr.RequestError as e:
                        QMessageBox.critical(self, "Gagal",
                                             "Tidak dapat meminta hasil dari layanan "
                                             "Pengenalan Suara Google; {0}".format(e))

            with open(text_path, "w", encoding="utf-8") as f:
                f.write(text)

        except Exception as e:
            QMessageBox.critical(self, "Gagal", f"Terjadi kesalahan: {str(e)}")

    def informasi(self):
        QMessageBox.information(self, "Informasi Penggunaan",
                                "1. Pilih file video yang ingin di extract ke text\n"
                                "2. Pilih folder untuk menyimpan hasil video ke text\n"
                                "3. Pilih bahasa yang ada  di dalam video kamu\n"
                                "4. Klik tombol 'Extract Video Ke Text!' untuk memulai proses\n"
                                "5. Tunggu hingga proses selesai\n"
                                "6. Jika proses selesai, maka akan muncul pesan "
                                "'Video sudah di extract ke dalam text'.\n\n"
                                "Note: \n"
                                "1. Harus Terhubung Dengan Internet.\n\n"
                                "Developer: Ahmad Bujay Rimi | Enjay Studio\n"
                                "Teknik Informatika, Universitas Esa Unggul")


# Class Untuk Mengubah Teks ke Suara
class TextToSpeech(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Mengubah Teks ke Suara')
        self.setGeometry(100, 100, 510, 200)
        self.setWindowIcon(QtGui.QIcon(':/Logo.png'))
        self.setFixedSize(self.size())

        # QLabel, QLineEdit, and QPushButton for text input
        self.label1 = QLabel('File Teks:', self)
        self.label1.setGeometry(20, 20, 100, 25)

        self.line_edit1 = QLineEdit(self)
        # Read only
        self.line_edit1.setReadOnly(True)
        self.line_edit1.setGeometry(120, 20, 300, 25)

        self.button1 = QPushButton('Pilih File', self)
        self.button1.setGeometry(430, 20, 70, 25)
        self.button1.clicked.connect(self.select_text_file)

        # QLabel, QLineEdit, and QPushButton for output folder
        self.label2 = QLabel('Simpan Ke:', self)
        self.label2.setGeometry(20, 60, 100, 25)

        self.line_edit2 = QLineEdit(self)
        # Read only
        self.line_edit2.setReadOnly(True)
        self.line_edit2.setGeometry(120, 60, 300, 25)

        self.button2 = QPushButton('Pilih Folder', self)
        self.button2.setGeometry(430, 60, 70, 25)
        self.button2.clicked.connect(self.select_save_folder)

        # QLabel and QComboBox for language selection
        self.label3 = QLabel('Bahasa Suara:', self)
        self.label3.setGeometry(20, 95, 100, 25)

        self.language_combo_box = QComboBox(self)
        self.language_combo_box.addItems(["Indonesia", "Jepang", "Inggris (UK)", "Inggris (US)", "Arab Saudi"])
        self.language_combo_box.setGeometry(120, 95, 150, 25)

        self.language_map = {
            "Indonesia": "id",
            "Jepang": "ja",
            "Inggris (UK)": "en-uk",
            "Inggris (US)": "en-us",
            "Arab Saudi": "ar"
        }

        # QPushButton for starting the extraction
        self.button3 = QPushButton('Ubah teks ke suara', self)
        self.button3.setGeometry(120, 135, 300, 25)
        self.button3.clicked.connect(self.convert_text_to_speech)

        self.button4 = QPushButton('Informasi', self)
        self.button4.setGeometry(120, 167, 300, 25)
        self.button4.clicked.connect(self.informasi)

    def select_text_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Pilih file teks', '', 'Text Files (*.txt)')
        if file_name:
            self.line_edit1.setText(file_name)

    def select_save_folder(self):
        folder_name = QFileDialog.getExistingDirectory(self, 'Pilih folder')
        if folder_name:
            self.line_edit2.setText(folder_name)

    def convert_text_to_speech(self):
        text_file_path = self.line_edit1.text()
        save_folder_path = self.line_edit2.text()
        language = self.language_map[self.language_combo_box.currentText()]

        if not text_file_path or not save_folder_path:
            QMessageBox.warning(self, 'Peringatan', 'Pastikan file teks dan folder penyimpanan sudah dipilih.')
            return

        with open(text_file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        tts = gTTS(text, lang=language)
        audio_file_name = os.path.basename(text_file_path).replace('.txt', '_extract_ke_audio.mp3')
        audio_file_path = f'{save_folder_path}/{audio_file_name}'
        tts.save(audio_file_path)

        QMessageBox.information(self, 'Berhasil', 'Text sudah berubah menjadi suara')

    def informasi(self):
        QMessageBox.information(self, "Informasi Penggunaan", "1. Pilih file text yang ingin di extract ke suara.\n"
                                                              "2. Pilih folder untuk menyimpan hasil text ke suara.\n"
                                                              "3. Pilih bahasa yang akan di extract.\n"
                                                              "4. Klik tombol 'Ubah teks ke suara' "
                                                              "untuk memulai proses.\n"
                                                              "5. Tunggu hingga proses selesai.\n"
                                                              "6. Jika proses selesai, maka akan muncul pesan "
                                                              "'Text sudah berubah menjadi suara'.\n"
                                                              "7. Selessai\n\n"
                                                              "Note: \n"
                                                              "1. Harus Terhubung Dengan Internet.\n\n"
                                                              "Developer: Ahmad Bujay Rimi | Enjay Studio\n"
                                                              "Teknik Informatika, Universitas Esa Unggul")


# Class Untuk Foto Sketch Pensil
class PhotoEditorSketchPencil(QMainWindow):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Photo Editor (Tahap Pengembangan)")
        self.setGeometry(100, 100, 850, 780)
        self.setWindowIcon(QtGui.QIcon(':/Logo.png'))
        # Fix Size
        self.setFixedSize(self.size())

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.label1 = QLabel("File Foto: ", self)
        self.label1.setAlignment(Qt.AlignLeft)
        # Size
        self.label1.setFixedHeight(18)
        layout.addWidget(self.label1)

        self.filepath_line_edit = QLineEdit(self)
        # Read Only
        self.filepath_line_edit.setReadOnly(True)
        layout.addWidget(self.filepath_line_edit)

        self.browse_button = QPushButton("Pilih Foto", self)
        self.browse_button.clicked.connect(self.browse_image)
        layout.addWidget(self.browse_button)

        self.label2 = QLabel("Simpen Ke: ", self)
        self.label2.setAlignment(Qt.AlignLeft)
        # Size
        self.label2.setFixedHeight(18)
        layout.addWidget(self.label2)

        self.folderpath_line_edit = QLineEdit(self)
        # Read Only
        self.folderpath_line_edit.setReadOnly(True)
        layout.addWidget(self.folderpath_line_edit)

        self.folder_button = QPushButton("Pilih Folder", self)
        self.folder_button.clicked.connect(self.select_folder)
        layout.addWidget(self.folder_button)

        self.create_radio_buttons(layout)

        self.start_edit_button = QPushButton("Mulai Edit Photo!", self)
        self.start_edit_button.clicked.connect(self.process_image)
        layout.addWidget(self.start_edit_button)

        self.informasi_button = QPushButton("Informasi", self)
        self.informasi_button.clicked.connect(self.informasi)
        layout.addWidget(self.informasi_button)

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(1)
        self.slider.setMaximum(101)
        self.slider.setValue(31)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(3)
        layout.addWidget(self.slider)

        self.slider_value_label = QLabel("Value Kontras Warna: 31%", self)
        layout.addWidget(self.slider_value_label)
        self.slider.valueChanged.connect(self.update_slider_value_label)

        image_layout = QHBoxLayout()

        self.input_image_label = QLabel(self)
        self.input_image_label.setAlignment(Qt.AlignLeft)  # Menambahkan alignment kiri
        image_layout.addWidget(self.input_image_label)

        self.output_image_label = QLabel(self)
        self.output_image_label.setAlignment(Qt.AlignRight)  # Menambahkan alignment kanan
        image_layout.addWidget(self.output_image_label)

        layout.addLayout(image_layout)

    def create_radio_buttons(self, layout):
        self.radio_group = QGroupBox("Pilih Filter:")
        vbox = QVBoxLayout()

        self.gray_button = QRadioButton("Gray")
        vbox.addWidget(self.gray_button)

        self.invert_button = QRadioButton("Invert")
        vbox.addWidget(self.invert_button)

        self.blur_button = QRadioButton("Blur")
        vbox.addWidget(self.blur_button)

        self.pencil_sketch_button = QRadioButton("Pencil Sketch")
        vbox.addWidget(self.pencil_sketch_button)

        self.radio_group.setLayout(vbox)
        layout.addWidget(self.radio_group)

    def browse_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Pilih File Foto", "", "Format Foto (*.png *.jpg)")
        self.filepath_line_edit.setText(file_path)
        self.show_image(file_path)

    def show_image(self, file_path):
        image = cv2.imread(file_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        q_image = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.input_image_label.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio))

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        self.folderpath_line_edit.setText(folder_path)

    def update_slider_value_label(self):
        self.ensure_odd_slider_value()
        self.slider_value_label.setText(f"Value Kontras Warna: {self.slider.value()}" + "%")

    def ensure_odd_slider_value(self):
        value = self.slider.value()
        if value % 2 == 0:
            value += 1
            self.slider.setValue(value)

    def process_image(self):
        file_path = self.filepath_line_edit.text()
        if not file_path:
            return

        image = cv2.imread(file_path)
        ksize = self.slider.value()
        if ksize % 2 == 0:
            ksize += 1

        if self.gray_button.isChecked():
            edited_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        elif self.invert_button.isChecked():
            edited_image = 255 - image
        elif self.blur_button.isChecked():
            ksize_tuple = (ksize, ksize)
            edited_image = cv2.GaussianBlur(image, ksize_tuple, 0)
        elif self.pencil_sketch_button.isChecked():
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            inverted_gray_image = 255 - gray_image
            blurred_image = cv2.GaussianBlur(inverted_gray_image, (ksize, ksize), 0)
            inverted_blurred_image = 255 - blurred_image
            edited_image = cv2.divide(gray_image, inverted_blurred_image, scale=256.0)
        else:
            QMessageBox.warning(self, "Peringatan", "Tidak Ada Filter Terpilih!")
            return

        self.display_output_image(edited_image)
        self.save_image(edited_image, file_path)

    def display_output_image(self, edited_image):
        edited_image = cv2.cvtColor(edited_image, cv2.COLOR_BGR2RGB)
        q_image = QImage(edited_image.data, edited_image.shape[1], edited_image.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.output_image_label.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio))

    def save_image(self, edited_image, file_path):
        folder_path = self.folderpath_line_edit.text()
        if not folder_path:
            return

        file_name, file_extension = os.path.splitext(os.path.basename(file_path))
        new_file_path = os.path.join(folder_path, f"{file_name}_edit_foto_AI{file_extension}")

        cv2.imwrite(new_file_path, edited_image)
        QMessageBox.information(self, "Berhasil", "Foto Anda Sudah Di Edit Dengan AI")

    def informasi(self):
        QMessageBox.information(self, "Informasi Penggunaan", "1. Jalankan aplikasi dan klik 'Pilih Foto' "
                                                              "untuk memilih foto yang ingin diubah.\n"
                                                              "2. Klik 'Pilih Folder' untuk memilih folder "
                                                              "tempat menyimpan hasil edit foto.\n"
                                                              "3. Pilih opsi edit foto: Gray, Invert, Blur, atau Pencil Sketch.\n"
                                                              "4. Atur intensitas efek (jika diperlukan) dengan menggeser QSlider.\n"
                                                              "5. Klik 'Mulai Edit Photo!' untuk memproses foto. "
                                                              "Foto hasil edit akan ditampilkan di sebelah kanan."
                                                              "6. Hasil akan disimpan di folder yang dipilih sebelumnya, "
                                                              "dan Anda akan menerima notifikasi "
                                                              "'Foto Anda Sudah Di Edit Dengan AI'.\n\n"
                                                              "Note: \n"
                                                              "1. Harus Terhubung Dengan Internet.\n\n"
                                                              "Developer: Ahmad Bujay Rimi | Enjay Studio\n"
                                                              "Teknik Informatika, Universitas Esa Unggul")


# Class Untuk Webcam Sketch Pensil
running = True


class WebcamThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def run(self):
        cap = cv2.VideoCapture(0)
        while running:
            ret, frame = cap.read()
            self.change_pixmap_signal.emit(frame)
            cv2.waitKey(1)
        cap.release()


class WebcamWindow(QWidget):
    def __init__(self, slider):
        super().__init__()
        self.initUI()
        self.slider = slider

    def initUI(self):
        self.setWindowTitle('Webcam Window')
        self.setGeometry(100, 100, 600, 450)
        self.setWindowIcon(QtGui.QIcon(':/Logo.png'))
        self.setFixedSize(self.size())

        vbox = QVBoxLayout()

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        vbox.addWidget(self.label, stretch=1)
        vbox.setContentsMargins(0, 0, 0, 0)

        self.setLayout(vbox)

    def update_image(self, frame):
        blur_value = self.slider.value()
        if blur_value % 2 == 0:
            blur_value += 1
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        inverted_gray_frame = 255 - gray_frame
        blurred_frame = cv2.GaussianBlur(inverted_gray_frame, (blur_value, blur_value), 0)
        inverted_blurred_frame = 255 - blurred_frame
        pencil_sketch_frame = cv2.divide(gray_frame, inverted_blurred_frame, scale=256.0)

        height, width = pencil_sketch_frame.shape
        bytes_per_line = width
        image = QImage(pencil_sketch_frame.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixmap.scaled(self.width(), self.height(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))

        self.label.setMinimumSize(self.width(), self.height())
        self.label.setMaximumSize(self.width(), self.height())


class WebcamSketchPencil(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Webcam to Pencil Sketch')
        self.setWindowIcon(QtGui.QIcon(':/Logo.png'))
        self.setGeometry(100, 100, 600, 550)
        self.setFixedSize(self.size())
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)

        vbox = QVBoxLayout()

        self.label = QLabel(self)
        vbox.addWidget(self.label)

        hbox = QHBoxLayout()

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(1)
        self.slider.setMaximum(101)
        self.slider.setValue(31)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(3)
        self.slider.valueChanged.connect(self.update_slider_label)
        hbox.addWidget(self.slider)

        self.slider_label = QLabel(f"{self.slider.value()}%", self)
        hbox.addWidget(self.slider_label)

        vbox.addLayout(hbox)

        self.start_button = QPushButton('Mulai', self)
        self.start_button.clicked.connect(self.start_webcam)
        vbox.addWidget(self.start_button)

        self.webcam_button = QPushButton('Tampilkan Jendela Webcam', self)
        self.webcam_button.clicked.connect(self.show_webcam_window)
        vbox.addWidget(self.webcam_button)

        self.informasi_button = QPushButton('Informasi', self)
        self.informasi_button.clicked.connect(self.informasi)
        vbox.addWidget(self.informasi_button)

        self.exit_button = QPushButton('Keluar', self)
        self.exit_button.clicked.connect(self.exit_program)
        vbox.addWidget(self.exit_button)

        self.setLayout(vbox)

    def start_webcam(self):
        self.th = WebcamThread()
        self.th.change_pixmap_signal.connect(self.update_image)
        self.th.start()

    def show_webcam_window(self):
        if hasattr(self, 'th'):
            self.w = WebcamWindow(self.slider)
            self.th.change_pixmap_signal.connect(self.w.update_image)
            self.w.show()
        else:
            QMessageBox.warning(self, "Peringatan", "Mohon tekan tombol 'Mulai' terlebih dahulu sebelum menampilkan jendela webcam.")

    def update_image(self, frame):
        blur_value = self.slider.value()
        if blur_value % 2 == 0:
            blur_value += 1
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        inverted_gray_frame = 255 - gray_frame
        blurred_frame = cv2.GaussianBlur(inverted_gray_frame, (blur_value, blur_value), 0)
        inverted_blurred_frame = 255 - blurred_frame
        pencil_sketch_frame = cv2.divide(gray_frame, inverted_blurred_frame, scale=256.0)

        height, width = pencil_sketch_frame.shape
        bytes_per_line = width
        image = QImage(pencil_sketch_frame.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixmap.scaled(600, 430, Qt.KeepAspectRatio))

    def update_slider_label(self):
        self.slider_label.setText(f"{self.slider.value()}%")

    def exit_program(self):
        global running
        running = False
        self.close()

    def closeEvent(self, event):
        global running
        running = False

    def informasi(self):
        QMessageBox.information(self, "Informasi Penggunaan", "1. Klik tombol 'Mulai' untuk memulai menampilkan "
                                                              "gambar sketsa pensil dari webcam.\n"
                                                              "2. Geser QSlider untuk mengatur tingkat blur yang "
                                                              "diterapkan pada gambar.\n"
                                                              "3. Klik tombol 'Tampilkan Jendela Webcam' untuk membuka "
                                                              "jendela baru yang menampilkan gambar sketsa pensil dalam "
                                                              "mode layar penuh.\n"
                                                              "4. Klik tombol 'Keluar' untuk keluar dari aplikasi.\n\n"
                                                              "Note: \n"
                                                              "Ingatlah bahwa Kamu perlu menekan tombol 'Mulai' "
                                                              "sebelum menggunakan tombol 'Tampilkan Jendela Webcam'.\n")


class VoiceAssistantGoogle(QWidget):
    def __init__(self):
        super().__init__()

        self.recognizer = sr.Recognizer()
        self.player = QMediaPlayer()
        self.player.stateChanged.connect(self.player_state_changed)
        self.initUI()
        self.temp_file = None

    def initUI(self):
        self.setWindowTitle('Assistant Media Player (Beta)')
        self.setGeometry(300, 300, 650, 610)
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon(':/Logo.png'))

        vbox = QVBoxLayout()

        self.question_label = QLabel(
            'List Pertanyaan:\n'
            '1. Siapakah pembuat aplikasi ini?\n'
            '2. Bagaimana Cara Menggunakan Spotify Downloader ?\n'
            '3. Bagaimana Cara Menggunakan Kode Lisensi Key ?\n'
            '4. Bagaimana Cara Menggunakan Webcam Lisensi ?\n'
            '5. Bagaimana Cara Menggunakan ScreenShot ?\n'
            '6. Bagaimana Cara Menggunakan Untuk Mendeteksi Objek Pada Video ?\n'
            '7. Bagaimana Cara Menggunakan Untuk Mendeteksi Wajah Pada Foto ?\n'
            '8. Bagaimana Cara Menggunakan Youtube Downloader ?\n'
            '9. Bagaimana Cara Menggunakan Subtitle Youtube Downloader ?\n'
            '10. Bagaimana Cara Menggunakan Video Facebook Downloader ?\n'
            '11. Bagaimana Cara Menggunakan Profil Instragram Downloader ?\n'
            '12. Bagaimana Cara Menggunakan Untuk Merubah Format Video Dari AVI Ke MP4 ?\n'
            '13. Bagaimana Cara Menggunakan Untuk Merubah Format Video Dari MP4 Ke MP3 ?\n'
            '14. Bagaimana Cara Menggunakan Untuk Memotong Video ?\n'
            '15. Bagaimana Cara Menggunakan Untuk Menggabungkan Video ?\n'
            '16. Bagaimana Cara Menggunakan Untuk Menghapus Background Foto ?\n'
            '17. Bagaimana Cara Menggunakan Untuk Mengompres Ukuran Foto ?\n'
            '18. Bagaimana Cara Menggunakan Untuk Mengubah Resolusi dan Frame Pada Video ?\n'
            '19. Bagaimana Cara Menggunakan Untuk Merubah Video Ke Per Frame Foto ?\n'
            '20. Bagaimana Cara Menggunakan Untuk Merubah Per Frame Foto Ke Video ?\n'
            '21. Bagaimana Cara Menggunakan Untuk Merubah Video Ke Text ?\n'
            '22. Bagaimana Cara Menggunakan Untuk Merubah Text Ke Suara Google ?\n'
            '23. Bagaimana Cara Menggunakan Untuk Merubah Foto Ke Sketch Pensil ?\n'
            '24. Bagaimana Cara Menggunakan Untuk Merubah Webcam Ke Sketch Pensil ?\n',
            self)
        vbox.addWidget(self.question_label)

        font = QFont("Arial", 12)
        self.question_label.setFont(font)

        font_status = QFont("Arial", 10)
        self.status_label = QLabel('Status:', self)
        self.status_label.setFont(font_status)
        vbox.addWidget(self.status_label)

        self.start_button = QPushButton('Mulai', self)
        # Size of the button
        self.start_button.setFixedSize(625, 25)
        self.start_button.clicked.connect(self.start_button_click)
        vbox.addWidget(self.start_button)

        self.repeat_button = QPushButton('Ulang', self)
        # Size of the button
        self.repeat_button.setFixedSize(625, 25)
        self.repeat_button.clicked.connect(self.repeat_button_click)
        vbox.addWidget(self.repeat_button)

        self.setLayout(vbox)

    def start_button_click(self):
        font_status = QFont("Arial", 10)

        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.stop()
            return

        palette = self.status_label.palette()
        palette.setColor(self.status_label.foregroundRole(), QtGui.QColor("red"))
        self.status_label.setPalette(palette)
        self.status_label.setText('Status: Mendengar')
        self.status_label.setFont(font_status)
        QApplication.processEvents()

        threading.Thread(target=self.listen).start()

    def listen(self):
        with sr.Microphone() as source:
            audio = self.recognizer.listen(source)

        try:
            text = self.recognizer.recognize_google(audio, language='id-ID')
            self.handle_recorded(text)

        except sr.UnknownValueError:
            self.status_label.setText('Status: Tidak mengerti')
            palette.setColor(self.status_label.foregroundRole(), QtGui.QColor("black"))
            self.status_label.setPalette(palette)
        except sr.RequestError as e:
            self.status_label.setText('Status: Tidak bisa terhubung')
            palette.setColor(self.status_label.foregroundRole(), QtGui.QColor("black"))
            self.status_label.setPalette(palette)

    def handle_recorded(self, text):
        global answer
        font_status = QFont("Arial", 10)

        if text:
            self.status_label.setText('Status: Menjawab')
            self.status_label.setFont(font_status)
            palette = self.status_label.palette()
            palette.setColor(self.status_label.foregroundRole(), QtGui.QColor("green"))
            self.status_label.setPalette(palette)

            lower_text = text.lower()

            if 'siapakah pembuat aplikasi ini' in lower_text or 'siapa pembuat aplikasi ini' in lower_text:
                answer = (
                    'Yang membuat aplikasi media player ini adalah ahmad bujay rimi, dia adalah seorang mahasiswa teknik informatika'
                    ' universitas esa unggul, dia sekarang lagi kejar seminar proposal, tugas akhir dan mencari magang')
            elif 'bagaimana cara menggunakan spotify downloader' in lower_text:
                answer = (
                    'Program ini adalah Spotify Downloader yang memungkinkan pengguna untuk mengunduh lagu dari playlist Spotify dan '
                    'menyimpannya dalam format MP3 di folder pilihan pengguna. Berikut ini adalah langkah-langkah penggunaan program:\n\n'
                    '1. Tempelkan tautan playlist Spotify yang ingin Anda unduh lagunya di bidang teks yang diberi label "Link Spotify:".\n'
                    '2. Pilih folder tempat Anda ingin menyimpan lagu yang diunduh dengan mengklik tombol "Pilih Folder" di samping '
                    'bidang teks "Pilih Folder Simpan". Jendela dialog akan terbuka untuk memilih folder tujuan.\n'
                    '3. Setelah memilih folder tujuan, klik tombol "Download Lagu Spotify!" untuk memulai proses pengunduhan lagu.\n'
                    '4. Program akan mengunduh lagu dari playlist Spotify yang diberikan dan menyimpannya dalam format MP3 di folder '
                    'yang Anda pilih sebelumnya.\n'
                    '5. Jika terjadi kesalahan saat mengunduh musik, Anda akan melihat pesan peringatan dengan teks "Terjadi kesalahan '
                    'saat mengunduh musik\'.\n'
                    '6. Setelah proses pengunduhan selesai, Anda akan melihat pesan informasi dengan teks "Musik Spotify sudah terdownload".\n'
                    '7. Selesai.\n\n' 
                    'Catatan:\n' 
                    '1. Harus terhubung dengan internet.\n' 
                    '2. Aplikasi Spotify harus terbuka.\n\n' 
                    'Pengembang: Ahmad Bujay Rimi | Enjay Studio\n' 'Teknik Informatika, Universitas Esa Unggul')
            elif 'bagaimana cara menggunakan kode lisensi key' in lower_text:
                answer = ('Program ini adalah aplikasi untuk memverifikasi Lisensi Key sebelum menggunakan pemutar media. '
                          'Berikut ini adalah langkah-langkah penggunaan program:\n\n'
                          '1. Jalankan aplikasi, kemudian Anda akan melihat jendela dengan judul "Lisensi Key Pemutar Media" yang berisi bidang teks dan tombol "Cek Lisensi Key".\n'
                          '2. Masukkan Lisensi Key yang valid ke dalam bidang teks yang diberi label "Lisensi Key: ". Ada dua Lisensi Key yang valid, yaitu "Ahmad Bujai Rimi" dan "UEU Teknik Informatika 2019".\n'
                          '3. Klik tombol "Cek Lisensi Key" atau gunakan shortcut Ctrl+L (jika tidak dikomentari) untuk memverifikasi Lisensi Key yang Anda masukkan.\n'
                          '4. Jika Lisensi Key yang Anda masukkan valid, maka akan muncul pesan "Lisensi Key sudah masuk", dan Anda akan diarahkan ke jendela utama aplikasi pemutar media (class Window).\n'
                          '5. Jika Lisensi Key yang Anda masukkan tidak valid, maka akan muncul pesan "Lisensi Key belum masuk", dan Anda akan diminta untuk memasukkan Lisensi Key yang valid lagi.\n'
                          '6. Setelah memasukkan Lisensi Key yang valid, Anda dapat menggunakan aplikasi pemutar media seperti yang diharapkan.\n\n' 
                          'Catatan:\n\n' 
                          '1. Pastikan Lisensi Key yang dimasukkan benar dan valid.\n' 
                          '2. Program ini hanya akan berfungsi jika Lisensi Key yang dimasukkan valid.\n\n' 
                          'Pengembang: Ahmad Bujay Rimi | Enjay Studio\n' 'Teknik Informatika, Universitas Esa Unggul')
            elif 'bagaimana cara menggunakan webcam lisensi' in lower_text:
                answer = ('Program ini adalah aplikasi pendeteksian wajah untuk verifikasi lisensi key pada media player. Aplikasi ini membandingkan wajah yang ditangkap melalui kamera dengan wajah target yang telah terdaftar. Berikut ini adalah langkah-langkah penggunaan program:\n\n'
                          '1. Jalankan aplikasi, Anda akan melihat jendela utama dengan area tampilan gambar dan tombol "Start".\n' 
                          '2. Klik tombol "Start" untuk memulai proses pendeteksian wajah menggunakan kamera perangkat Anda.\n' 
                          '3. Aplikasi akan mencoba mendeteksi wajah dalam jangka waktu 10 detik. Jika wajah Anda cocok dengan wajah target yang terdaftar, maka aplikasi akan memberikan pesan informasi "Selamat Muka Anda Terdeteksi Sebagai Lisensi Media Player".\n'
                          '4. Jika wajah Anda terdeteksi, aplikasi akan menutup jendela pendeteksian wajah dan membuka jendela media player.\n' 
                          '5. Jika wajah Anda tidak terdeteksi dalam waktu 10 detik, aplikasi akan memberikan pesan peringatan "Mohon Maaf Muka Anda Tidak Terdaftar Dalam Aplikasi Ini".\n'
                          '6. Jika wajah Anda tidak terdeteksi, aplikasi akan menutup jendela pendeteksian wajah dan membuka jendela untuk memasukkan lisensi key secara manual.\n' 
                          '7. Selesai.\n\n' 
                          'Catatan:\n' '1. Pastikan kamera pada perangkat Anda berfungsi dengan baik.\n' 
                          '2. Pastikan pencahayaan cukup untuk mendeteksi wajah dengan jelas.\n\n' 
                          'Pengembang: Ahmad Bujay Rimi | Enjay Studio\n' 'Teknik Informatika, Universitas Esa Unggul')
            elif 'bagaimana cara menggunakan screenshot' in lower_text:
                answer = ('Program ini adalah aplikasi Screenshot yang memungkinkan pengguna untuk mengambil screenshot dari layar utama komputer dan menyimpannya dalam format gambar PNG atau JPEG. Berikut ini adalah langkah-langkah penggunaan program:\n\n'
                          '1. Jalankan aplikasi ini dan Anda akan melihat tampilan utama yang menampilkan screenshot layar komputer Anda saat ini.\n'
                          '2. Klik tombol "Simpan screenshot" untuk menyimpan gambar screenshot ke komputer Anda. Jendela dialog akan terbuka untuk memilih lokasi penyimpanan dan format gambar (PNG atau JPEG).\n'
                          '3. Setelah memilih lokasi penyimpanan dan format gambar, klik "Simpan" untuk menyimpan gambar screenshot.\n'
                          '4. Jika Anda ingin mengambil screenshot baru, klik tombol "Keluar" untuk menutup aplikasi saat ini. Kemudian, jalankan kembali aplikasi untuk mengambil screenshot baru dan mengikuti langkah-langkah yang sama untuk menyimpan gambar.\n'
                          '5. Selesai.\n\n'
                          'Catatan:\n'
                          '1. Pastikan bahwa aplikasi ini memiliki akses yang diperlukan untuk mengambil screenshot layar komputer Anda.\n\n'
                          'Pengembang: Ahmad Bujay Rimi | Enjay Studio\n' 'Teknik Informatika, Universitas Esa Unggul')
            elif 'bagaimana cara menggunakan untuk mendeteksi objek pada video' in lower_text:
                answer = ('Program ini adalah deteksi objek pada video menggunakan algoritma YOLO (You Only Look Once) dengan OpenCV. Program ini mampu mendeteksi berbagai objek dalam video dan menampilkan kotak pembatas dan label kelas di sekitar objek yang terdeteksi. Berikut ini adalah langkah-langkah penggunaan program:\n\n'
                          '1. Pastikan Anda memiliki file bobot (weights) dan konfigurasi (cfg) dari model YOLOv3 yang telah dilatih, serta file coco.names yang berisi daftar nama kelas objek.\n' 
                          '2. Jalankan program ini, yang akan membuka jendela dialog untuk memilih video yang ingin Anda proses.\n'
                          '3. Pilih video dengan format yang didukung (mis. *.mp4, *.avi) menggunakan jendela dialog "Pilih Video".\n'
                          '4. Setelah memilih video, program akan mulai memproses video dan menampilkan hasil deteksi objek pada jendela "Mendeteksi Objek Video (Tahap Pengembangan)".\n'
                          '5. Objek yang terdeteksi akan diberi kotak pembatas berwarna dan label kelas, dengan tingkat kepercayaan (confidence) deteksi.\n'
                          '6. Di pojok kiri atas jendela hasil, Anda akan melihat informasi tentang FPS (frames per second) dari proses deteksi objek.\n'
                          '7. Untuk menghentikan proses deteksi objek dan menutup jendela, tekan tombol "Esc" pada keyboard Anda.\n\n' 
                          'Catatan:\n' 
                          '1. Pastikan Anda memiliki file bobot (weights) dan konfigurasi (cfg) dari model YOLOv3 yang telah dilatih, serta file coco.names yang berisi daftar nama kelas objek.\n'
                          '2. Membutuhkan spesifikasi komputer yang tinggi terutama pada cpu'
                          'Pengembang: Ahmad Bujay Rimi | Enjay Studio\n' 'Teknik Informatika, Universitas Esa Unggul')
            elif 'bagaimana cara menggunakan untuk mendeteksi objek pada gambar' in lower_text:
                answer = ('Program ini adalah aplikasi deteksi objek dalam foto yang memungkinkan pengguna untuk mendeteksi objek dalam foto dan menyimpan hasilnya ke folder pilihan pengguna. Berikut ini adalah langkah-langkah penggunaan program:\n\n'
                          '1. Klik tombol "Buka File" di samping bidang teks "File Foto" untuk memilih foto yang ingin dideteksi objeknya. Jendela dialog akan terbuka untuk memilih file foto dengan format yang didukung (*.jpg).\n'
                          '2. Setelah memilih foto, pilih folder tempat Anda ingin menyimpan hasil deteksi objek dengan mengklik tombol "Buka Folder" di samping bidang teks "Simpen Ke". Jendela dialog akan terbuka untuk memilih folder tujuan.\n'
                          '3. Setelah memilih folder tujuan, klik tombol "Mulai Mendeteksi Objek!" untuk memulai proses deteksi objek dalam foto.\n'
                          '4. Program akan mendeteksi objek dalam foto yang diberikan dan menyimpan hasil deteksi dengan kotak dan label objek ke folder yang Anda pilih sebelumnya.\n'
                          '5. Jika foto atau folder simpan tidak diisi, Anda akan melihat pesan peringatan dengan teks "Foto atau Folder Simpan Tidak Boleh Kosong".\n'
                          '6. Setelah proses deteksi objek selesai, Anda akan melihat pesan informasi dengan teks "Mendeteksi Objek Foto Sudah Selesai".\n\n' 
                          'Catatan:\n'
                          '1. Pastikan Anda memiliki file bobot (weights) dan konfigurasi (cfg) dari model YOLOv3 yang telah dilatih, serta file coco.names yang berisi daftar nama kelas objek.\n\n' 
                          'Pengembang: Ahmad Bujay Rimi | Enjay Studio\n' 'Teknik Informatika, Universitas Esa Unggul')
            elif 'bagaimana cara menggunakan youtube downloader' in lower_text:
                answer = ('Program ini adalah Youtube Downloader yang memungkinkan pengguna untuk mengunduh video dari Youtube dan menyimpannya dalam format yang dipilih (3GPP, mp4, atau mp4 hanya suara) di folder pilihan pengguna. Berikut ini adalah langkah-langkah penggunaan program:\n\n'
                          '1. Tempelkan tautan video Youtube yang ingin Anda unduh di bidang teks yang diberi label "Masukan URL Video".\n'
                          '2. Pilih folder tempat Anda ingin menyimpan video yang diunduh dengan mengklik tombol "Buka Folder". Jendela dialog akan terbuka untuk memilih folder tujuan.\n'
                          '3. Setelah memilih folder tujuan, pilih format video yang ingin Anda unduh dengan menggunakan kotak pilihan (ComboBox) yang diberi label "Pilih Format". Anda dapat memilih antara "3GPP", "mp4", atau "mp4 (Hanya Suara)"\n.' 
                          '4. Klik tombol "Mulai Download Video Youtube!" untuk memulai proses pengunduhan video.\n'
                          '5. Program akan mengunduh video dari tautan Youtube yang diberikan dan menyimpannya dalam format yang Anda pilih sebelumnya di folder yang Anda pilih.\n'
                          '6. Jika video berhasil diunduh, Anda akan melihat pesan informasi dengan teks "Video Selesai Di Download". Jika terjadi kesalahan, Anda akan melihat pesan peringatan dengan teks "Masukan URL Video".\n'
                          '7. Selesai.\n\n'
                          'Catatan:\n' 
                          '1. Harus terhubung dengan internet.\n\n'
                          'Pengembang: Ahmad Bujay Rimi | Enjay Studio\n' 'Teknik Informatika, Universitas Esa Unggul')
            elif 'bagaimana cara menggunakan subtitle youtube downloader' in lower_text:
                answer = ('Program ini adalah Youtube Subtitle Downloader yang memungkinkan pengguna untuk mengunduh subtitle dari video Youtube dan menyimpannya dalam format teks di folder pilihan pengguna. Berikut ini adalah langkah-langkah penggunaan program:\n\n'
                          '1. Tempelkan tautan video Youtube yang ingin Anda unduh subtitlenya di bidang teks yang diberi label "Masukan URL Video:".\n'
                          '2. Pilih folder tempat Anda ingin menyimpan subtitle yang diunduh dengan mengklik tombol "Buka Folder" di samping bidang teks "Simpan Ke:". Jendela dialog akan terbuka untuk memilih folder tujuan.\n'
                          '3. Setelah memilih folder tujuan, pilih bahasa subtitle yang Anda inginkan (Indonesia atau Inggris) dari kotak kombinasi yang diberi label "Pilih Bahasa".\n'
                          '4. Klik tombol "Mulai Download Subtitle Youtube!" untuk memulai proses pengunduhan subtitle.\n'
                          '5. Program akan mengunduh subtitle dari video Youtube yang diberikan dan menyimpannya dalam format teks di folder yang Anda pilih sebelumnya.\n'
                          '6. Jika terjadi kesalahan saat mengunduh subtitle, Anda akan melihat pesan peringatan dengan teks "Masukan URL Video".\n'
                          '7. Setelah proses pengunduhan selesai, Anda akan melihat pesan informasi dengan teks "Subtitle Selesai Di Download".\n'
                          '8. Selesai.\n\n'
                          'Catatan:\n'
                          '1. Harus terhubung dengan internet.\n\n'
                          'Pengembang: Ahmad Bujay Rimi | Enjay Studio\n' 'Teknik Informatika, Universitas Esa Unggul')
            elif 'bagaimana cara menggunakan video facebook downloader' in lower_text:
                answer = ('Program ini adalah Video Facebook Downloader yang memungkinkan pengguna untuk mengunduh video dari Facebook dan menyimpannya dalam format video di folder pilihan pengguna. Berikut ini adalah langkah-langkah penggunaan program:\n\n' 
                          '1. Tempelkan tautan video Facebook yang ingin Anda unduh di bidang teks yang diberi label "URL Facebook:".\n' 
                          '2. Pilih folder tempat Anda ingin menyimpan video yang diunduh dengan mengklik tombol "Buka Folder" di samping bidang teks "Simpan Ke:". Jendela dialog akan terbuka untuk memilih folder tujuan.\n'
                          '3. Setelah memilih folder tujuan, klik tombol "Mulai Download Video Facebook!" untuk memulai proses pengunduhan video.\n' 
                          '4. Program akan mengunduh video dari tautan Facebook yang diberikan dan menyimpannya dalam format video di folder yang Anda pilih sebelumnya.\n'
                          '5. Jika terjadi kesalahan saat mengunduh video, Anda akan melihat pesan peringatan dengan teks "Terjadi kesalahan saat mengunduh video".\n'
                          '6. Setelah proses pengunduhan selesai, Anda akan melihat pesan informasi dengan teks "Video Facebook Sudah Di Download".\n'
                          '7. Selesai.\n\n' 
                          'Catatan:\n' 
                          '1. Harus terhubung dengan internet.\n\n' 
                          'Pengembang: Ahmad Bujay Rimi | Enjay Studio\n' 'Teknik Informatika, Universitas Esa Unggul')
            elif 'bagaimana cara menggunakan profil instragram downloader' in lower_text:
                answer = ('Program ini adalah Instagram Profile Downloader yang memungkinkan pengguna untuk mengunduh foto dan video dari profil Instagram dan menyimpannya dalam folder pilihan pengguna. Berikut ini adalah langkah-langkah penggunaan program:\n\n' 
                          '1. Masukkan nama profil Instagram yang ingin Anda unduh foto dan videonya di bidang teks yang diberi label "Nama Profile:".\n' 
                          '2. Pilih folder tempat Anda ingin menyimpan foto dan video yang diunduh dengan mengklik tombol "Buka Folder" di samping bidang teks "Simpan Ke:". Jendela dialog akan terbuka untuk memilih folder tujuan.\n' 
                          '3. Setelah memilih folder tujuan, klik tombol "Mulai Download Profile Instagram!" untuk memulai proses pengunduhan foto dan video.\n' 
                          '4. Program akan mengunduh foto dan video dari profil Instagram yang diberikan dan menyimpannya di folder yang Anda pilih sebelumnya.\n' 
                          '5. Jika proses pengunduhan selesai, Anda akan melihat pesan informasi dengan teks "Video dan Foto Proile Sudah Di Download.".\n' 
                          '6. Klik tombol "Informasi" untuk melihat informasi lebih lanjut tentang cara penggunaan aplikasi dan catatan penting.\n\n' 
                          'Catatan:\n' 
                          '1. Harus terhubung dengan internet.\n' 
                          '2. Tidak bisa mengunduh jika profil bersifat private.\n\n' 
                          'Pengembang: Ahmad Bujay Rimi | Enjay Studio\n' 'Teknik Informatika, Universitas Esa Unggul')
            elif 'bagaimana cara menggunakan untuk merubah format video dari avi ke mp4' in lower_text:
                answer = ('Program ini adalah Video Converter dari format .avi ke .mp4 yang memungkinkan pengguna untuk mengubah format video .avi menjadi format .mp4. Berikut ini adalah langkah-langkah penggunaan program:\n\n' 
                          '1. Buka program Video_Converter_Avi_To_Mp4.\n' 
                          '2. Klik tombol "Mulai Format Video!" untuk membuka jendela dialog yang memungkinkan Anda memilih file video .avi yang ingin diubah formatnya.\n'
                          '3. Setelah memilih file video, program akan mulai mengubah format video dari .avi menjadi .mp4.\n'
                          '4. Hasil konversi akan disimpan dalam folder yang sama dengan file video .avi yang dipilih, dengan nama file yang sama tetapi dengan ekstensi .mp4.\n'
                          '5. Jika file video tidak ditemukan atau terjadi kesalahan saat mengonversi video, Anda akan melihat pesan peringatan dengan teks "File Video Tidak Ditemukan".\n'
                          '6. Setelah proses konversi selesai, Anda akan melihat pesan informasi dengan teks "Convert Video Selesai".\n'
                          '7. Klik tombol "Informasi" untuk membaca informasi penggunaan dan detail pengembang.\n\n' 
                          'Catatan:\n'
                          '1. File video yang akan diubah formatnya harus berformat .avi.\n' 
                          '2. Hasil konversi akan berformat .mp4.\n\n' 
                          'Pengembang: Ahmad Bujay Rimi | Enjay Studio\n' 'Teknik Informatika, Universitas Esa Unggul')
            elif 'bagaimana cara menggunakan untuk merubah format video dari mp4 ke mp3' in lower_text:
                answer = ('Program ini adalah Video Converter MP4 ke MP3 yang memungkinkan pengguna untuk mengonversi video berformat .mp4 menjadi audio berformat .mp3. Berikut ini adalah langkah-langkah penggunaan program:\n\n' 
                          '1. Buka program Video Converter MP4 ke MP3.\n'
                          '2. Klik tombol "Mulai Format Video ke Audio!" untuk membuka jendela dialog yang memungkinkan Anda memilih file video .mp4 yang ingin dikonversi.\n'
                          '3. Pilih file video .mp4 yang ingin Anda konversi ke format audio .mp3.\n' 
                          '4. Setelah file video dipilih, program akan secara otomatis mengonversi video tersebut menjadi audio .mp3 dan menyimpannya di folder yang sama dengan file video asli.\n'
                          '5. Jika konversi berhasil, Anda akan melihat pesan informasi dengan teks "Convert Video ke Audio Selesai". Jika file video tidak ditemukan, Anda akan melihat pesan peringatan dengan teks "File Video Tidak Ditemukan".\n'
                          '6. Klik tombol "Informasi" untuk menampilkan informasi penggunaan dan keterangan tambahan tentang program ini.\n\n' 
                          'Catatan:\n' 
                          '1. File video yang akan dikonversi harus berformat .mp4 dan hasil konversi akan berformat .mp3.\n'
                          '2. Hasil konversi akan disimpan di folder yang sama dengan file video yang akan dikonversi.\n\n' 
                          'Pengembang: Ahmad Bujay Rimi | Enjay Studio\n' 'Teknik Informatika, Universitas Esa Unggul')
            elif 'bagaimana cara menggunakan untuk memotong video' in lower_text:
                answer = ('Program ini adalah Potong Video (Cut Video) yang memungkinkan pengguna untuk memotong video dengan format .mp4 dan menyimpan hasil potongan video ke folder pilihan pengguna. Berikut ini adalah langkah-langkah penggunaan program:\n\n'
                          '1. Klik tombol "Buka Folder" di samping bidang teks "File Video". Jendela dialog akan terbuka untuk memilih file video yang ingin dipotong.\n'
                          '2. Setelah memilih file video, durasi video akan ditampilkan di bawah label "Durasi Video".\n'
                          '3. Pilih folder tempat Anda ingin menyimpan hasil potongan video dengan mengklik tombol "Buka Folder" di samping bidang teks "Simpan Ke". Jendela dialog akan terbuka untuk memilih folder tujuan.\n'
                          '4. Tentukan apakah Anda ingin memotong video per detik atau per menit dengan memilih radio button "Per Detik" atau "Per Menit".\n'
                          '5. Masukkan waktu mulai dan waktu selesai untuk potongan video pada bidang teks "Waktu Mulai" dan "Waktu Selesai".\n' 
                          '6. Setelah mengatur semua opsi, klik tombol "Mulai Cut Video!" untuk memulai proses pemotongan video.\n' 
                          '7. Program akan memotong video sesuai dengan opsi yang dipilih dan menyimpan hasil potongan video dengan nama file yang sama ditambah sufiks "_terpotong" di folder yang Anda pilih sebelumnya.\n'
                          '8. Jika pemotongan video berhasil, Anda akan melihat pesan informasi dengan teks "Video Berhasil Di Cut." Jika terjadi kesalahan, Anda akan melihat pesan peringatan dengan teks "Silahkan Masukan File Video Yang Ingin Di Cut, Folder Untuk Menyimpan Hasil Yang Sudah Di cut, waktu mulai dan waktu selesai.".\n'
                          '9. Klik tombol "Informasi" untuk melihat informasi penggunaan lebih lanjut tentang program ini.\n\n' 
                          'Catatan:\n' 
                          '1. Program hanya mendukung pemotongan video dengan format .mp4.\n'
                          '2. Pastikan memasukkan waktu mulai dan waktu selesai dengan benar sesuai dengan format yang dipilih (detik atau menit).\n\n'
                          'Pengembang: Ahmad Bujay Rimi | Enjay Studio\n' 'Teknik Informatika, Universitas Esa Unggul')
            elif 'bagaimana cara menggunakan untuk menggabungkan video' in lower_text:
                answer = ('Program ini adalah aplikasi penggabung video yang memungkinkan pengguna untuk menggabungkan beberapa video menjadi satu file video dan menyimpannya dalam format MP4 di folder pilihan pengguna. Berikut ini adalah langkah-langkah penggunaan program:\n\n'
                          '1. Klik tombol "Tambah Video" untuk menambahkan video yang ingin digabungkan. Jendela dialog akan terbuka untuk memilih file video. Anda bisa menambahkan lebih dari satu video.\n'
                          '2. Pilih folder tempat Anda ingin menyimpan video yang telah digabungkan dengan mengklik tombol "Buka Folder" di bawah teks "Simpan Ke". Jendela dialog akan terbuka untuk memilih folder tujuan.\n'
                          '3. Setelah memilih folder tujuan, klik tombol "Mulai Gabungkan Video!" untuk memulai proses penggabungan video.\n'
                          '4. Program akan menggabungkan semua video yang telah Anda pilih sebelumnya dan menyimpannya dalam format MP4 di folder yang Anda pilih dengan nama file yang diakhiri "_tergabung.mp4".\n'
                          '5. Setelah proses penggabungan selesai, Anda akan melihat pesan informasi dengan teks "Video Sudah Di Gabungkan Menjadi Satu".\n'
                          '6. Jika Anda ingin menggabungkan video lagi, klik tombol "Tambah Video" dan pilih video yang akan digabungkan.\n\n'
                          'Catatan:\n'
                          '1. Harus terhubung dengan internet.\n\n'
                          'Pengembang: Ahmad Bujay Rimi | Enjay Studio\n' 'Teknik Informatika, Universitas Esa Unggul')
            elif 'bagaimana cara menggunakan untuk menghapus background foto' in lower_text:
                answer = ('Program ini adalah penghapus latar belakang foto yang memungkinkan pengguna untuk menghapus latar belakang dari gambar dan menyimpan hasilnya dalam format PNG di folder pilihan pengguna. Berikut ini adalah langkah-langkah penggunaan program:\n\n'
                          '1. Klik tombol "Pilih Gambar" untuk memilih foto yang ingin dihapus latar belakangnya. Jendela dialog akan terbuka untuk memilih gambar dalam format (*.png, *.jpg, *.bmp).\n'
                          '2. Setelah memilih gambar, tampilan pratinjau akan muncul di area yang disediakan.\n'
                          '3. Pilih folder tempat Anda ingin menyimpan gambar yang telah dihapus latar belakangnya dengan mengklik tombol "Buka Folder". Jendela dialog akan terbuka untuk memilih folder tujuan.\n'
                          '4. Setelah memilih folder tujuan, klik tombol "Mulai Hapus Background Foto!" untuk memulai proses penghapusan latar belakang.\n'
                          '5. Jika proses penghapusan berhasil, Anda akan melihat pesan informasi dengan teks "Background Foto Sudah Di Hapus".\n'
                          '6. Gambar yang telah dihapus latar belakangnya akan tersimpan dalam format PNG di folder yang Anda pilih sebelumnya.\n'
                          '7. Klik tombol "Informasi" untuk melihat informasi penggunaan dan detail pengembang.\n\n'
                          'Catatan:\n'
                          '1. Pastikan gambar yang dipilih memiliki format yang didukung (*.png, *.jpg, *.bmp).\n\n'
                          'Pengembang: Ahmad Bujay Rimi | Enjay Studio\n' 'Teknik Informatika, Universitas Esa Unggul')
            elif 'bagaimana cara menggunakan untuk mengompres ukuran foto' in lower_text:
                answer = ('Program ini adalah Kompresor Gambar yang memungkinkan pengguna untuk mengompres ukuran foto dan menyimpannya dengan kualitas yang dapat disesuaikan di folder pilihan pengguna. Berikut ini adalah langkah-langkah penggunaan program:\n\n'
                          '1. Klik tombol "Buka File" untuk memilih foto yang ingin Anda kompres. Jendela dialog akan terbuka untuk memilih file foto yang sesuai.\n'
                          '2. Masukkan ukuran lebar dan tinggi yang diinginkan untuk foto yang telah dikompres di bidang teks "Lebar:" dan "Tinggi:".\n'
                          '3. Atur kualitas kompresi foto dengan menggeser slider "Kualitas:" sesuai keinginan Anda.\n'
                          '4. Pilih folder tempat Anda ingin menyimpan foto yang telah dikompres dengan mengklik tombol "Buka Folder" di samping bidang teks "Pilih Folder Simpan". Jendela dialog akan terbuka untuk memilih folder tujuan.\n'
                          '5. Setelah memilih folder tujuan, klik tombol "Mulai Kompres Size Foto!" untuk memulai proses kompresi foto.\n'
                          '6. Program akan mengompres foto yang diberikan dan menyimpannya di folder yang Anda pilih sebelumnya.\n'
                          '7. Jika terjadi kesalahan saat mengompresi foto, Anda akan melihat pesan peringatan dengan teks "Terjadi Kesalahan Saat Mengompresi Foto: (detail kesalahan)".\n'
                          '8. Setelah proses kompresi selesai, Anda akan melihat pesan informasi dengan teks "Size Foto Berhasil Di Kompres".\n'
                          '9. Selesai.\n\n'
                          'Catatan:\n'
                          '1. Harus terhubung dengan internet.\n'
                          '2. Format foto yang didukung adalah .png dan .jpg.\n\n'
                          'Pengembang: Ahmad Bujay Rimi | Enjay Studio\n' 'Teknik Informatika, Universitas Esa Unggul')
            elif 'bagaimana cara menggunakan untuk mengubah resolusi dan frame pada video' in lower_text:
                answer = ('Program ini adalah aplikasi untuk mengubah resolusi dan frame rate video yang memungkinkan pengguna untuk mengubah resolusi dan frame rate video sesuai keinginan mereka. Berikut ini adalah langkah-langkah penggunaan program:\n\n'
                          '1. Klik tombol "Pilih File" untuk memilih video yang ingin Anda ubah resolusi dan frame ratenya. Jendela dialog akan terbuka untuk memilih file video.\n'
                          '2. Pilih folder tempat Anda ingin menyimpan video yang sudah dikonversi dengan mengklik tombol "Pilih Folder" di samping bidang teks "Simpan Ke". Jendela dialog akan terbuka untuk memilih folder tujuan.\n'
                          '3. Sesuaikan frame rate video dengan menggeser slider di bawah label "Frame Rate:". Nilai frame rate yang dipilih akan ditampilkan di sebelah kanan slider.\n'
                          '4. Pilih resolusi video yang diinginkan dari kotak kombinasi di bawah label "Resolusi Video:".\n'
                          '5. Setelah menyesuaikan frame rate dan resolusi, klik tombol "Mulai Convert Resolusi dan Frame Rate Video!" untuk memulai proses konversi video.\n'
                          '6. Program akan mengkonversi video sesuai dengan resolusi dan frame rate yang telah Anda pilih dan menyimpannya di folder yang Anda pilih sebelumnya.\n'
                          '7. Setelah proses konversi selesai, Anda akan melihat pesan informasi dengan teks "Resolusi dan Frame Rate Video Anda Sudah Dirubah".\n'
                          '8. Selesai.\n\n' 'Catatan:\n'
                          '1. Tidak disarankan untuk mengubah frame rate dari nilai yang lebih kecil ke nilai yang lebih besar.\n\n'
                          'Pengembang: Ahmad Bujay Rimi | Enjay Studio\n' 'Teknik Informatika, Universitas Esa Unggul')
            elif 'bagaimana cara menggunakan untuk merubah video ke per frame foto' in lower_text:
                answer = ('Program ini adalah Video to Image Converter yang memungkinkan pengguna untuk mengkonversi video menjadi beberapa frame foto dan menyimpannya dalam format JPG di folder pilihan pengguna. Berikut ini adalah langkah-langkah penggunaan program:\n\n'
                          '1. Klik tombol "Buka File" di sebelah bidang teks "File Video" untuk memilih video yang ingin Anda konversi. Jendela dialog akan terbuka untuk memilih file video dengan format .mp4.\n'
                          '2. Pilih folder tempat Anda ingin menyimpan foto hasil konversi dengan mengklik tombol "Buka Folder" di samping bidang teks "Simpan Ke". Jendela dialog akan terbuka untuk memilih folder tujuan.\n'
                          '3. Setelah memilih folder tujuan, klik tombol "Mulai Convert Video Ke Per Frame Foto!" untuk memulai proses konversi.\n'
                          '4. Program akan mengkonversi video yang diberikan menjadi beberapa frame foto dan menyimpannya dalam format JPG di folder yang Anda pilih sebelumnya.\n'
                          '5. Jika terjadi kesalahan saat mengkonversi video, Anda akan melihat pesan peringatan dengan teks "Peringatan".\n'
                          '6. Setelah proses konversi selesai, Anda akan melihat pesan informasi dengan teks "Video Sudah Terekstrak Menjadi Beberapa Per - Frame Foto".\n'
                          '7. Selesai.\n\n'
                          'Catatan:\n'
                          '1. Pilih folder yang kosong untuk menyimpan hasil konversi.\n\n'
                          'Pengembang: Ahmad Bujay Rimi | Enjay Studio\n' 'Teknik Informatika, Universitas Esa Unggul')
            elif 'bagaimana cara menggunakan untuk merubah per frame foto ke video' in lower_text:
                answer = ('Program ini adalah aplikasi konversi foto ke video yang memungkinkan pengguna untuk menggabungkan foto-foto dari folder yang dipilih dan menyimpannya dalam bentuk video dengan frame rate yang dapat disesuaikan. Berikut ini adalah langkah-langkah penggunaan program:\n\n'
                          '1. Klik tombol "Buka Folder" di samping bidang teks "Folder Foto" untuk memilih folder yang berisi foto yang ingin Anda konversi ke video. Jendela dialog akan terbuka untuk memilih folder.\n'
                          '2. Pilih folder tempat Anda ingin menyimpan video yang dihasilkan dengan mengklik tombol "Buka Folder" di samping bidang teks "Simpan Ke". Jendela dialog akan terbuka untuk memilih folder tujuan.\n'
                          '3. Atur frame rate video dengan menggeser slider yang berlabel "Frame Rate". Nilai frame rate akan ditampilkan di sebelah kanan slider.\n'
                          '4. Setelah memilih folder input dan output serta mengatur frame rate, klik tombol "Mulai Convert Foto Ke Video!" untuk memulai proses konversi.\n'
                          '5. Program akan menggabungkan foto-foto dari folder yang dipilih dan menyimpannya dalam bentuk video di folder yang Anda pilih sebelumnya.\n'
                          '6. Jika terjadi kesalahan atau folder yang dipilih tidak memiliki foto, Anda akan melihat pesan peringatan yang relevan.\n'
                          '7. Setelah proses konversi selesai, Anda akan melihat pesan informasi dengan teks "Per Frame Foto Berhasil Convert Ke Video".\n'
                          '8. Selesai.\n\n'
                          'Catatan:\n'
                          '1. Nama per frame foto harus berurutan dan berakhiran .jpg atau .png, misalnya foto01, foto02, ..., foto1000.\n'
                          '2. Pastikan folder yang Anda pilih memiliki foto yang valid.\n\n'
                          'Pengembang: Ahmad Bujay Rimi | Enjay Studio\n' 'Teknik Informatika, Universitas Esa Unggul')
            elif 'bagaimana cara menggunakan untuk merubah video ke text' in lower_text:
                answer = ('Program ini adalah Aplikasi Pengonversi Video ke Teks yang memungkinkan pengguna untuk mengubah konten video menjadi teks dan menyimpannya dalam format file teks (.txt) di folder pilihan pengguna. Berikut ini adalah langkah-langkah penggunaan program:\n\n'
                          '1. Klik tombol "Pilih File" di bawah label "File Video" untuk memilih file video yang ingin Anda konversi ke teks. Jendela dialog akan terbuka untuk memilih file video.\n'
                          '2. Pilih folder tempat Anda ingin menyimpan file teks yang dihasilkan dengan mengklik tombol "Pilih Folder" di bawah label "Simpan Ke". Jendela dialog akan terbuka untuk memilih folder tujuan.\n'
                          '3. Pilih bahasa yang ada di dalam video Anda dari kotak pilihan "Bahasa Video" yang tersedia.\n'
                          '4. Setelah memilih folder tujuan dan bahasa, klik tombol "Mulai Extract Video Ke Text!" untuk memulai proses pengubahan video ke teks.\n'
                          '5. Program akan mengonversi konten video menjadi teks dan menyimpannya dalam format file teks (.txt) di folder yang Anda pilih sebelumnya.\n'
                          '6. Jika terjadi kesalahan saat mengonversi video, Anda akan melihat pesan peringatan dengan teks "Terjadi kesalahan saat mengonversi video".\n'
                          '7. Setelah proses konversi selesai, Anda akan melihat pesan informasi dengan teks "Video sudah di extract ke dalam text".\n'
                          '8. Selesai.\n\n'
                          'Catatan:\n'
                          '1. Harus terhubung dengan internet.\n\n'
                          'Pengembang: Ahmad Bujay Rimi | Enjay Studio\n' 'Teknik Informatika, Universitas Esa Unggul')
            elif 'bagaimana cara menggunakan untuk merubah text Ke suara google' in lower_text:
                answer = ('Program ini adalah aplikasi Mengubah Teks ke Suara yang memungkinkan pengguna untuk mengonversi teks dalam file teks ke format audio MP3 dan menyimpannya di folder pilihan pengguna. Berikut ini adalah langkah-langkah penggunaan program:\n\n'
                          '1. Klik tombol "Pilih File" di sebelah bidang teks "File Teks" untuk memilih file teks yang ingin dikonversi. Jendela dialog akan terbuka untuk memilih file teks yang diinginkan.\n'
                          '2. Pilih folder tempat Anda ingin menyimpan audio yang dihasilkan dengan mengklik tombol "Pilih Folder" di samping bidang teks "Simpan Ke". Jendela dialog akan terbuka untuk memilih folder tujuan.\n'
                          '3. Pilih bahasa suara yang akan digunakan untuk konversi teks ke suara menggunakan kotak pilihan "Bahasa Suara".\n'
                          '4. Setelah memilih folder tujuan dan bahasa suara, klik tombol "Ubah teks ke suara" untuk memulai proses konversi.\n'
                          '5. Program akan mengonversi teks dari file teks yang diberikan ke format audio MP3 menggunakan bahasa suara yang dipilih dan menyimpannya di folder yang Anda pilih sebelumnya.\n'
                          '6. Jika proses konversi selesai, Anda akan melihat pesan informasi dengan teks "Text sudah berubah menjadi suara".\n'
                          '7. Selesai.\n\n'
                          'Catatan:\n'
                          '1. Harus terhubung dengan internet.\n\n'
                          'Pengembang: Ahmad Bujay Rimi | Enjay Studio\n' 'Teknik Informatika, Universitas Esa Unggul')
            elif 'bagaimana cara menggunakan foto ke sketch pensil' in lower_text:
                answer = ('Program ini adalah Photo Editor dengan efek sketsa pensil yang memungkinkan pengguna untuk mengedit foto dan menyimpan hasilnya dalam format asli di folder pilihan pengguna. Berikut ini adalah langkah-langkah penggunaan program:\n\n'
                          '1. Jalankan aplikasi dan klik "Pilih Foto" untuk memilih foto yang ingin diubah. Foto yang dipilih akan ditampilkan di bagian kiri jendela aplikasi.\n'
                          '2. Klik "Pilih Folder" untuk memilih folder tempat menyimpan hasil edit foto. Jendela dialog akan terbuka untuk memilih folder tujuan.\n'
                          '3. Pilih opsi edit foto dari radio button: Gray, Invert, Blur, atau Pencil Sketch.\n'
                          '4. Atur intensitas efek (jika diperlukan) dengan menggeser QSlider. Nilai kontras warna akan ditampilkan di bawah slider.\n'
                          '5. Klik "Mulai Edit Photo!" untuk memproses foto. Foto hasil edit akan ditampilkan di sebelah kanan foto asli.\n'
                          '6. Hasil akan disimpan di folder yang dipilih sebelumnya, dan Anda akan menerima notifikasi "Foto Anda Sudah Di Edit Dengan AI".\n'
                          '7. Selesai.\n\n'
                          'Catatan:\n'
                          '1. Harus terhubung dengan internet.\n\n'
                          'Pengembang: Ahmad Bujay Rimi | Enjay Studio\n' 'Teknik Informatika, Universitas Esa Unggul')
            elif 'bagaimana cara menggunakan untuk merubah webcam ke sketch pensil' in lower_text:
                answer = ('Program ini adalah aplikasi Webcam Sketch Pensil yang mengubah gambar dari webcam menjadi sketsa pensil secara real-time. Berikut ini adalah langkah-langkah penggunaan program:\n\n'
                          '1. Jalankan program dan Anda akan melihat tampilan utama aplikasi.\n'
                          '2. Klik tombol "Mulai" untuk memulai menampilkan gambar sketsa pensil dari webcam pada label di jendela utama aplikasi.\n'
                          '3. Geser QSlider untuk mengatur tingkat blur yang diterapkan pada gambar. Nilai blur akan ditampilkan dalam persentase di samping QSlider.\n'
                          '4. Klik tombol "Tampilkan Jendela Webcam" untuk membuka jendela baru yang menampilkan gambar sketsa pensil dalam mode layar penuh.\n'
                          '5. Klik tombol "Informasi" untuk melihat informasi penggunaan aplikasi dan petunjuk penggunaan.\n'
                          '6. Klik tombol "Keluar" untuk keluar dari aplikasi. Aplikasi akan menutup dan berhenti menangkap gambar dari webcam.\n\n'
                          'Catatan:\n'
                          '1. Pastikan Anda memiliki webcam yang terhubung dan berfungsi dengan benar.\n'
                          '2. Anda perlu menekan tombol "Mulai" sebelum menggunakan tombol "Tampilkan Jendela Webcam".\n\n'
                          'Pengembang: Ahmad Bujay Rimi | Enjay Studio\n' 'Teknik Informatika, Universitas Esa Unggul')
            else:
                answer = ( 'Mohon maaf, saya sebagai voice assistant yang sudah di latih oleh sang developer ahmad bujai rimi untuk' 
                           ' tidak menjawab pertanyaan yang tidak ada di dalam list pertanyaan')

            tts = gTTS(answer, lang='id')
            with tempfile.NamedTemporaryFile(delete=False) as fp:
                tts.save(fp.name)
                self.player.setMedia(QMediaContent(QUrl.fromLocalFile(fp.name)))
                self.player.play()
                self.temp_file = fp.name

    def repeat_button_click(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.stop()
            return

        if self.temp_file:
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.temp_file)))
            self.player.play()

    def player_state_changed(self, state):
        if state == QMediaPlayer.StoppedState:
            self.status_label.setText('Status:')
            palette = self.status_label.palette()
            palette.setColor(self.status_label.foregroundRole(), QtGui.QColor("black"))
            self.status_label.setPalette(palette)
            if os.path.exists(self.temp_file):
                os.unlink(self.temp_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    lisensi = LisensiKey()
    lisensi.show()
    sys.exit(app.exec_())