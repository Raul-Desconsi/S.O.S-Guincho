import tkinter as tk
from pathlib import Path
from tkinter import Canvas, Button, PhotoImage
from cidade import CidadeForm
from motorista import MotoristaForm
from caminhao import CaminhaoForm
from home import HomeForm

OUTPUT_PATH = Path("C:\build").parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")

def relative_to_assets(path: str) -> Path:

    return ASSETS_PATH / Path(path)

root = tk.Tk()
root.geometry("1300x750")
root.configure(bg="#FFFFFF")
root.resizable(False, False)

canvas = Canvas(
    root,
    bg="#FFFFFF",
    height=750,
    width=1300,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
canvas.create_image(650.0, 375.0, image=image_image_1)

image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
canvas.create_image(244.0, 489.0, image=image_image_2)

image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
canvas.create_image(244.20977783203125, 166.3211669921875, image=image_image_3)

image_image_5 = PhotoImage(file=relative_to_assets("image_5.png"))
canvas.create_image(152, 140, image=image_image_5)

image_image_7 = PhotoImage(file=relative_to_assets("image_7.png"))
canvas.create_image(60, 146, image=image_image_7)

canvas.create_text(
    538.0, 92.0,
    anchor="nw",
    text="SISTEMA DE GERENCIAMENTO DO ADMINISTRADOR",
    fill="#F29101",
    font=("Sansation Bold", 20)
)



canvas.create_text(
    100.0, 130.0,
    anchor="nw",
    text="Admin",
    fill="white",
    font=("Sansation Bold", 13)
    
)

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
Button(
    root,
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: root.destroy(),
    relief="flat"
).place(
    x=1.0,
    y=651.2247924804688,
    width=147.9314727783203,
    height=44.76216125488281
)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
Button(
    root,
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: CidadeForm(root),
    relief="flat"
).place(
    x=11.0,
    y=494.0,
    width=273.9505615234375,
    height=43.729278564453125
)

button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
Button(
    root,
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: CaminhaoForm(root),
    relief="flat"
).place(
    x=11.0,
    y=425.0,
    width=274.0,
    height=43.72928237915039
)

button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
Button(
    root,
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: MotoristaForm(root),
    relief="flat"
).place(
    x=11.0,
    y=356.0,
    width=274.0,
    height=43.729286193847656
)

button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
Button(
    root,
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: HomeForm(root)
).place(
    x=1.0494384765625,
    y=229.3369140625,
    width=295.9011535644531,
    height=43.729286193847656
)

image_image_4 = PhotoImage(file=relative_to_assets("image_4.png"))
image_id_4 = canvas.create_image(785.0, 439.0, image=image_image_4)



HomeForm(root)
root.mainloop()
