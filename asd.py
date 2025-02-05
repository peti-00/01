import PIL.Image
import google.generativeai as genai
from pynput import mouse
import threading
import pyautogui
from win10toast import ToastNotifier

# Google Gemini API konfigurálása
genai.configure(api_key="AIzaSyB2Do2QaimtAsgRSGLoQew-pwobHUQEy4o")
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config={"max_output_tokens": 25}  # Limitálás 100 tokenre
)

prompt = "a képen egy kvizt látsz mi a megoldás csak a megoldást küld el?"
is_processing = False  # Állapotváltozó a lekérdezés futásának követésére

# Windows értesítés megjelenítése
def show_notification(message):
    n = ToastNotifier()
    n.show_toast("AI Válasz", message, duration=10)

# Függvény a screenshot készítéséhez és a lekérdezés futtatásához
def query_ai():
    global is_processing
    if is_processing:
        return  # Ha már fut egy lekérdezés, ne indítsunk újat

    is_processing = True
    #print("Képernyőkép készítése...")

    # Screenshot készítése és mentése
    screenshot_path = "screenshot.jpg"
    pyautogui.screenshot(screenshot_path)

    # Kép betöltése
    sample_file = PIL.Image.open(screenshot_path)

    #print("Lekérdezés indítása...")
    try:
        response = model.generate_content([prompt, sample_file])
        #print(response.text)
        show_notification(response.text)  # Válasz megjelenítése értesítésben
    except Exception as e:
        show_notification(f"Hiba történt: {e}")  # Hibaüzenet értesítésben

    is_processing = False  # Lekérdezés vége

# Függvény, amely a jobb egérkattintáskor hívódik meg
def on_click(x, y, button, pressed):
    if pressed and button == mouse.Button.right:
        threading.Thread(target=query_ai, daemon=True).start()  # Új szál indítása

# Egérfigyelő indítása
with mouse.Listener(on_click=on_click) as listener:
    #print("Jobb egérgomb kattintásra készít egy képernyőképet és elküldi az AI-nak...")
    listener.join()