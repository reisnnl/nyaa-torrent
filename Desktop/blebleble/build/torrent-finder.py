from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox
from tkinter import IntVar
import json
import os
import requests
import re

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\reina\Desktop\blebleble\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

SAVE_FILE = "eps.json"

def save_counts():
    data = {
        "gavv": gavv.get(),
        "gotchard": gotchard.get(),
        "exaid": exaid.get(),
        "zeroone": zeroone.get(),
        "gozyuger": gozyuger.get(),
        "kyuranger": kyuranger.get()
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

def increment(var, text_id):
    var.set(var.get() + 1)
    canvas.itemconfig(text_id, text=var.get())
    save_counts()

def load_counts():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            gavv.set(data.get("gavv", 37))
            gotchard.set(data.get("gotchard", 39))
            exaid.set(data.get("exaid", 2))
            zeroone.set(data.get("zeroone", 1))
            gozyuger.set(data.get("gozyuger", 15))
            kyuranger.set(data.get("kyuranger", 2))

window = Tk()
window.geometry("480x618")
window.title("Torrent Finder")
window.configure(bg="#FFFFFF")

gavv = IntVar(value=37)
gotchard = IntVar(value=39)
exaid = IntVar(value=2)
zeroone = IntVar(value=1)
gozyuger = IntVar(value=15)
kyuranger = IntVar(value=2)

load_counts()

def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=20, **kwargs):
    points = [
        x1+radius, y1,
        x2-radius, y1,
        x2, y1,
        x2, y1+radius,
        x2, y2-radius,
        x2, y2,
        x2-radius, y2,
        x1+radius, y2,
        x1, y2,
        x1, y2-radius,
        x1, y1+radius,
        x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=640,
    width=480,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

window.iconbitmap(os.path.join(os.path.dirname(__file__), "icon.ico"))

canvas.create_rectangle(
    0.0, 0.0, 478.0, 618.0,
    fill="#D9D9D9", outline=""
)
canvas.create_rectangle(
    188.0,
    114.0,
    189.00000039340253,
    124.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    183.0,  # 183.0 - 1
    118.0,
    194.0,
    119.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    451.0,
    114.0,
    452.0000003934025,
    124.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    446.0,
    118.0,
    457.0,
    119.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    188.0,
    136.0,
    189.00000039340253,
    146.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    183.0,
    140.0,
    194.0,
    141.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    451.0,
    136.0,
    452.0000003934025,
    146.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    446.0,
    140.0,
    457.0,
    141.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    188.0,
    159.0,
    189.00000039340253,
    169.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    183.0,
    163.0,
    194.0,
    164.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    188.0,
    182.0,
    189.00000039340253,
    192.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    183.0,
    186.0,
    194.0,
    187.0,
    fill="#000000",
    outline="")


canvas.create_text(
    197.0,
    2.0,
    anchor="nw",
    text="Torrent Finder",
    fill="#000000",
    font=("Inter Bold", 12 * -1)
)

canvas.create_rectangle(
    -1.0,
    18.999999999999886,
    478.0,
    20.0,
    fill="#A89E9E",
    outline="")


create_rounded_rectangle(canvas, 31.0, 338.0, 446.0, 591.0, radius=25, fill="#949494", outline="")

canvas.create_text(
    31.0,
    317.0,
    anchor="nw",
    text="Torrent list",
    fill="#000000",
    font=("Inter", 10, "bold")
)


entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))

create_rounded_rectangle(canvas, 34, 262, 443, 284, radius=12, fill="#959595", outline="")

entry_1 = Entry(
    bd=0,
    bg="#959595",
    fg="#000716",
    highlightthickness=0,
    font=("Inter", 10)
)
entry_1.place(
    x=40.0,
    y=266.0,
    width=395.0,
    height=16.0
)

def search_nyaa(query):
    url = f"https://nyaa.si/?f=0&c=0_0&q={query}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        rows = re.findall(r'<tr class="(?:default|danger|success)">(.+?)</tr>', response.text, re.DOTALL)
        results = []
        for row in rows:
            title_match = re.search(r'<a href="/view/\d+".*?title="([^"]+)"', row)
            magnet_match = re.search(r'href="(magnet:\?xt=urn:btih:[^"]+)"', row)
            if title_match and magnet_match:
                title = title_match.group(1)
                magnet = magnet_match.group(1)
                results.append((title, magnet))
                if len(results) >= 12:
                    break
        return results
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao buscar: {e}")
        return []

def show_results_on_canvas(results):
    canvas.delete("torrent_result")
    y = 345
    max_chars = 60
    for title, magnet in results:
        display_title = (title[:max_chars - 3] + "...") if len(title) > max_chars else title
        text_id = canvas.create_text(
            40, y, anchor="nw",
            text=display_title,
            fill="#1a0dab",
            font=("Inter", 9, "underline"),
            tags="torrent_result"
        )
        if magnet:
            canvas.tag_bind(text_id, "<Button-1>", lambda e, m=magnet: os.startfile(m))
            canvas.tag_bind(text_id, "<Enter>", lambda e: canvas.config(cursor="hand2"))
            canvas.tag_bind(text_id, "<Leave>", lambda e: canvas.config(cursor=""))
        y += 20
def on_search(event=None):
    query = entry_1.get().strip()
    if not query:
        return
    results = search_nyaa(query)
    show_results_on_canvas(results)

entry_1.bind("<Return>", on_search)

canvas.create_text(
    31.0,
    240.0,
    anchor="nw",
    text="Search",
    fill="#000000",
    font=("Inter", 10, "bold")
)

canvas.create_text(
    240,
    90.0,
    anchor="center",
    text="Recent Episodes",
    fill="#000000",
    font=("Inter", 10, "bold")
)

canvas.create_text(
    31.0,
    112.0,
    anchor="nw",
    text="Kamen Rider Gavv",
    fill="#640064",
    font=("Inter", 9, "bold")
)

canvas.create_text(
    31.0,
    135.0,
    anchor="nw",
    text="Kamen Rider Gotchard",
    fill="#640064",
    font=("Inter", 9, "bold")
)

canvas.create_text(
    31.0,
    158.0,
    anchor="nw",
    text="Kamen Rider Ex-Aid",
    fill="#640064",
    font=("Inter", 9, "bold")
)

canvas.create_text(
    31.0,
    181.0,
    anchor="nw",
    text="Kamen Rider Zero-One",
    fill="#640064",
    font=("Inter", 9, "bold")
)

canvas.create_text(
    298.0,
    112.0,
    anchor="nw",
    text="No. 1 Sentai Gozyuger",
    fill="#640064",
    font=("Inter", 9, "bold")
)

canvas.create_text(
    284.0,
    135.0,
    anchor="nw",
    text="Uchuu Sentai Kyuranger",
    fill="#640064",
    font=("Inter", 9, "bold")
)

canvas.create_text(
    239.0, 
    31.0,
    anchor="center",
    text="Currently being taken from Nyaa.si",
    fill="#000000",
    font=("Inter", 8, "bold")
)

canvas.create_text(31.0, 112.0, anchor="nw", text="Kamen Rider Gavv", fill="#640064", font=("Inter", 9, "bold"))
gavv_text_id = canvas.create_text(165.0, 112.0, anchor="nw", text=str(gavv.get()), fill="#640064", font=("Inter", 9, "bold"))
plus_vert_gavv = canvas.create_rectangle(188.0, 114.0, 189.0, 124.0, fill="#000000", outline="")
plus_horiz_gavv = canvas.create_rectangle(183.0, 118.0, 194.0, 119.0, fill="#000000", outline="")
canvas.tag_bind(plus_vert_gavv, "<Button-1>", lambda e: increment(gavv, gavv_text_id))
canvas.tag_bind(plus_horiz_gavv, "<Button-1>", lambda e: increment(gavv, gavv_text_id))

canvas.create_text(31.0, 135.0, anchor="nw", text="Kamen Rider Gotchard", fill="#640064", font=("Inter", 9, "bold"))
gotchard_text_id = canvas.create_text(165.0, 135.0, anchor="nw", text=str(gotchard.get()), fill="#640064", font=("Inter", 9, "bold"))
plus_vert_gotchard = canvas.create_rectangle(188.0, 136.0, 189.0, 146.0, fill="#000000", outline="")
plus_horiz_gotchard = canvas.create_rectangle(183.0, 140.0, 194.0, 141.0, fill="#000000", outline="")
canvas.tag_bind(plus_vert_gotchard, "<Button-1>", lambda e: increment(gotchard, gotchard_text_id))
canvas.tag_bind(plus_horiz_gotchard, "<Button-1>", lambda e: increment(gotchard, gotchard_text_id))

canvas.create_text(31.0, 158.0, anchor="nw", text="Kamen Rider Ex-Aid", fill="#640064", font=("Inter", 9, "bold"))
exaid_text_id = canvas.create_text(170.0, 158.0, anchor="nw", text=str(exaid.get()), fill="#640064", font=("Inter", 9, "bold"))
plus_vert_exaid = canvas.create_rectangle(188.0, 159.0, 189.0, 169.0, fill="#000000", outline="")
plus_horiz_exaid = canvas.create_rectangle(183.0, 163.0, 194.0, 164.0, fill="#000000", outline="")
canvas.tag_bind(plus_vert_exaid, "<Button-1>", lambda e: increment(exaid, exaid_text_id))
canvas.tag_bind(plus_horiz_exaid, "<Button-1>", lambda e: increment(exaid, exaid_text_id))

canvas.create_text(31.0, 181.0, anchor="nw", text="Kamen Rider Zero-One", fill="#640064", font=("Inter", 9, "bold"))
zeroone_text_id = canvas.create_text(170.0, 181.0, anchor="nw", text=str(zeroone.get()), fill="#640064", font=("Inter", 9, "bold"))
plus_vert_zeroone = canvas.create_rectangle(188.0, 182.0, 189.0, 192.0, fill="#000000", outline="")
plus_horiz_zeroone = canvas.create_rectangle(183.0, 186.0, 194.0, 187.0, fill="#000000", outline="")
canvas.tag_bind(plus_vert_zeroone, "<Button-1>", lambda e: increment(zeroone, zeroone_text_id))
canvas.tag_bind(plus_horiz_zeroone, "<Button-1>", lambda e: increment(zeroone, zeroone_text_id))

canvas.create_text(298.0, 112.0, anchor="nw", text="No. 1 Sentai Gozyuger", fill="#640064", font=("Inter", 9, "bold"))
gozyuger_text_id = canvas.create_text(430.0, 112.0, anchor="nw", text=str(gozyuger.get()), fill="#640064", font=("Inter", 9, "bold"))
plus_vert_gozyuger = canvas.create_rectangle(451.0, 114.0, 452.0, 124.0, fill="#000000", outline="")
plus_horiz_gozyuger = canvas.create_rectangle(446.0, 118.0, 457.0, 119.0, fill="#000000", outline="")
canvas.tag_bind(plus_vert_gozyuger, "<Button-1>", lambda e: increment(gozyuger, gozyuger_text_id))
canvas.tag_bind(plus_horiz_gozyuger, "<Button-1>", lambda e: increment(gozyuger, gozyuger_text_id))

canvas.create_text(284.0, 135.0, anchor="nw", text="Uchuu Sentai Kyuranger", fill="#640064", font=("Inter", 9, "bold"))
kyuranger_text_id = canvas.create_text(430.0, 135.0, anchor="nw", text=str(kyuranger.get()), fill="#640064", font=("Inter", 9, "bold"))
plus_vert_kyuranger = canvas.create_rectangle(451.0, 136.0, 452.0, 146.0, fill="#000000", outline="")
plus_horiz_kyuranger = canvas.create_rectangle(446.0, 140.0, 457.0, 141.0, fill="#000000", outline="")
canvas.tag_bind(plus_vert_kyuranger, "<Button-1>", lambda e: increment(kyuranger, kyuranger_text_id))
canvas.tag_bind(plus_horiz_kyuranger, "<Button-1>", lambda e: increment(kyuranger, kyuranger_text_id))


window.resizable(False, False)
window.mainloop()
