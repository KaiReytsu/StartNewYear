from tkinter import Tk, Label
import pyaudio
import wave
from datetime import datetime, timedelta
import webbrowser
import contextlib
import threading
import vlc
import time


start_timer = 14
timer_seconds = start_timer
is_playing = False
my_thread = None
isrun = True

def play_audio():
    """playing audio in the wav format"""
    global is_playing
    chunk = 1024
    wf = wave.open('music/JingleBells.wav', 'rb')
    p = pyaudio.PyAudio()

    stream = p.open(
        format = p.get_format_from_width(wf.getsampwidth()),
        channels = wf.getnchannels(),
        rate = wf.getframerate(),
        output = True)

    data = wf.readframes(chunk)

    while data != '' and is_playing:
        stream.write(data)
        data = wf.readframes(chunk)

    stream.stop_stream()
    stream.close()
    p.terminate()

def press_button_play():
    global is_playing
    global my_thread

    if not is_playing:
        is_playing = True
        my_thread = threading.Thread(target=play_audio)
        my_thread.start()

def time_countdown(url, lbl):
    """counting from 12 to 1"""
    global timer_seconds
    timer_seconds -= 1
    if timer_seconds < 1:
        lbl.config(text=str('С Новым годом!'), 
                    font=('Arial', 20, 'bold'), 
                    foreground=_from_rgb((255,43,43)), 
                    bg=_from_rgb((10,95,56)),
                    )
        lbl.place(relx = 0.5,
                   rely = 0.5,
                   anchor = 'center')
        lbl.after(600, play_video, url)
        return None
    if timer_seconds <= 12:
        lbl.config(text=str(timer_seconds))
    lbl.after(1000, time_countdown, url, lbl)



def _from_rgb(rgb):
    """translates an rgb tuple of int to 
    a tkinter friendly color code"""
    return "#%02x%02x%02x" % rgb  


def show_window(url):
    """show tkinter window"""
    root = Tk()
    root.title("Скоро Новый Год")
    root.geometry("400x300")
    root.configure(background=_from_rgb((10,95,56)))
    root.after
    lbl = Label(root, font=('Arial', 40, 'bold'),
            foreground=_from_rgb((255,250,250)), background=_from_rgb((10,95,56)))
    lbl.pack(anchor='center')
    time_countdown(url, lbl)
    root.mainloop()

def music_length(fname):
    with contextlib.closing(wave.open(fname,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return int(duration)

def delay(url):
    webbrowser.open(url)

def play_video(video):
    media_player = vlc.MediaPlayer()
    media = vlc.Media(video)
    media_player.set_media(media)
    media_player.play()
    time.sleep(30)

def run_program(music_file, ttime, url):
    run_music = datetime.strptime(run_countdown, '%H:%M:%S') - timedelta(seconds=music_length(music_file))
    mtime = run_music.strftime("%H:%M:%S")
    global isrun
    while isrun:
        today = datetime.now()
        string = today.strftime("%H:%M:%S")
        if string == mtime:
            press_button_play()
        if string == ttime:
            show_window(url)
            isrun = False




music_file = ''                                 #music file to play befoure countdown
run_countdown = '23:59:47'                      #time to start countdown
# fireworks_url = ''
video = ''                                      #video file to play after countdown   

run_program(music_file, run_countdown, video)


