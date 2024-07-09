from ultralytics import YOLO
import os ,shutil
import keyboard,threading
import time
from threading import Thread
def getAndTrain(mainFolder,trainFolder,epo=1):
    """_summary_

    Args:
        mainFolder (str): general folder
        trainFolder (_type_): generel/murat
    """
    model=YOLO(f"{mainFolder}/yolov8n.pt")
    print(trainFolder)
    model.train(data=trainFolder+"/data.yaml",epochs=epo,project=trainFolder)
def lockMouseandkey():
    import threading
    from pynput import mouse, keyboard

    # Kilit açma sinyali
    unlock_signal = threading.Event()

    # Tuş kombinasyonlarını takip etmek için bir set
    pressed_keys = set()

    # Klavyeyi kilitle
    def disable_keyboard():
        def on_press(key):
            try:
                if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                    pressed_keys.add(key)
                elif key.char == 'j' or key.char == 'k':
                    pressed_keys.add(key)
                
                # Eğer tüm gerekli tuşlar basılmışsa sinyali ayarla
                if keyboard.Key.ctrl_l in pressed_keys and keyboard.Key.ctrl_r in pressed_keys and 'j' in pressed_keys and 'k' in pressed_keys:
                    unlock_signal.set()
                    return False  # Listener'ı durdur

            except AttributeError:
                pass

        def on_release(key):
            try:
                if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                    pressed_keys.discard(key)
                elif key.char == 'j' or key.char == 'k':
                    pressed_keys.discard(key)
            except AttributeError:
                pass

        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

    # Fareyi kilitle
    def disable_mouse():
        def on_move(x, y):
            return not unlock_signal.is_set()  # Fareyi kilitle

        with mouse.Listener(on_move=on_move) as listener:
            listener.join()

    # Kilit açma sinyalini kontrol et
    def check_unlock_keys():
        with keyboard.Listener(on_press=lambda key: unlock_signal.set() if key == keyboard.Key.esc else None) as listener:
            listener.join()

    # Thread'leri başlat
    keyboard_thread = threading.Thread(target=disable_keyboard)
    mouse_thread = threading.Thread(target=disable_mouse)
    unlock_thread = threading.Thread(target=check_unlock_keys)

    keyboard_thread.start()
    mouse_thread.start()
    unlock_thread.start()

    keyboard_thread.join()
    mouse_thread.join()
    unlock_thread.join()

    print("Klavye ve fare tekrar etkinleştirildi.")

