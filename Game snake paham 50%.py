import tkinter as tk
import random

root = tk.Tk()
root.title("Ular beta | Dzikriyanza Abid ")
root.resizable(False, False)

LEBAR = 500
TINGGI = 500
UKURAN_KOTAK = 25
arah = "Right"
arah_sebelumnya = arah
game_over_flag = False
kena_flag = False
makan = False
darah = 3
score = 0
ular = [
    (100, 100),
    (75, 100),
    (50, 100)
]

canvas = tk.Canvas(root, width=LEBAR, height=TINGGI)
canvas.pack()

# Ular 
for x,y in ular:
    kotak = canvas.create_rectangle(
        x,y,
        x+UKURAN_KOTAK,
        y+UKURAN_KOTAK,
        fill="green",
        tags="ular"
    )

def gerak_ular():
    global ular, arah_sebelumnya, makan, kena_flag, darah, score 
    
    
    kepala_x, kepala_y = ular[0]

    if arah == "Up":
        kepala_baru = (kepala_x, kepala_y -UKURAN_KOTAK)
    elif arah == "Down":
        kepala_baru = (kepala_x, kepala_y +UKURAN_KOTAK)
    elif arah == "Left":
        kepala_baru = (kepala_x -UKURAN_KOTAK, kepala_y)
    elif arah == "Right":
        kepala_baru = (kepala_x +UKURAN_KOTAK, kepala_y )
    
    if game_over(kepala_baru):
        if not kena_flag:
            darah -= 1
            gambar_darah()
            kena_flag = True
        if darah <= 0:
            game_over_text()
            return

        ular.clear()
        ular.extend([
            (100,100),
            (75,100),
            (50,100)
        ])
        arah_sebelumnya = arah
        canvas.delete("ular")
        
        root.after(100, gerak_ular)
        return
    kena_flag = False   
    
    ular.insert(0, kepala_baru)
    if not makan:
        ular.pop()
    else:
        makan = False

    canvas.delete("ular")
    for x, y in ular:
        canvas.create_rectangle(
            x,y,
            x+UKURAN_KOTAK,
            y+UKURAN_KOTAK,
            fill="green",
            tags="ular"
        )

    cek_makan()
    root.after(100, gerak_ular)
    arah_sebelumnya = arah

def ganti_arah(event):
    global arah, arah_sebelumnya
    
    if event.char == "w" and arah_sebelumnya != "Down":
        arah = "Up"
    elif event.char == "s" and arah_sebelumnya != "Up":
        arah = "Down"
    elif event.char == "a" and arah_sebelumnya != "Right":
        arah = "Left"
    elif event.char == "d" and arah_sebelumnya != "Left":
        arah = "Right"
#================================================================================================================

# Makanan
makanan = canvas.create_oval(
    0,0,
    UKURAN_KOTAK,
    UKURAN_KOTAK,
    fill="red"
)

def spawn_makanan():
    kotak_x = random.randint(0, (LEBAR//UKURAN_KOTAK) - 1)
    kotak_y = random.randint(0, (TINGGI//UKURAN_KOTAK) - 1)

    x = kotak_x * UKURAN_KOTAK
    y = kotak_y * UKURAN_KOTAK

    canvas.coords(
        makanan,
        x,y,
        x+UKURAN_KOTAK,
        y+UKURAN_KOTAK,
    )
#================================================================================================================

# Logika game
def cek_makan():
    global makan, score

    kepala_x, kepala_y = ular[0] 

    kx1, ky1 = kepala_x, kepala_y
    kx2, ky2 = kepala_x + UKURAN_KOTAK, kepala_y + UKURAN_KOTAK 
    mx1, my1, mx2, my2 = canvas.coords(makanan)

    if (kx1 < mx2 and 
        kx2 > mx1 and 
        ky1 < my2 and 
        ky2 > my1):
        spawn_makanan()
        makan = True
        score += 1
        tambah_score()
        
        
def game_over_text():
    global game_over_flag

    if game_over_flag:
        return
    game_over_flag = True
    canvas.create_text(
        LEBAR//2,
        TINGGI//2,
        fill="black",
        font=("Arial", 50, "bold"),
        text="Game Over",
        tags="gameover"     
    )
    canvas.create_text(
        LEBAR//2,
        TINGGI//2 + 40,
        fill="green",   
        font=("Arial", 20, "bold"),
        text=f"Score: {score}",
        tags="gameover"     
    )

    tombol_main.pack(padx=40)

def game_over(kepala_baru):
    global game_over_flag, darah, kena_flag
    x, y = kepala_baru
    kena_tembok = (x < 0 or 
                   y < 0 or 
                   x + UKURAN_KOTAK > LEBAR or 
                   y + UKURAN_KOTAK > TINGGI
                   )
        

    kena_badan = kepala_baru in ular[1:]

    return kena_tembok or kena_badan


    
def tambah_score():
    canvas.delete("score")
    canvas.create_text(
        60,35,
        font=("Arial", 20, "bold"),
        text=f"Score: {score}",
        tags="score"
    )

def gambar_darah():
    canvas.delete("darah")
    jarak = 10
    ukuran_hati = 25
    for i in range(darah):
        x = LEBAR - (darah - i) * (UKURAN_KOTAK + jarak)
        y = 30
        canvas.create_text(
            x,y,    
            text="❤️",
            fill="red",
            font=("Arial", ukuran_hati),
            tags="darah"
    )
#================================================================================================================
def main_lagi(event=None):
    global ular, arah, arah_sebelumnya, game_over_flag, score, darah, makan
    tombol_main.pack_forget()
    
    canvas.delete("gameover")
    ular = [
        (100,100),
        (75,100),
        (50,100),
    ]

    arah = "Right"
    arah_sebelumnya = arah
    game_over_flag = False
    score = 0
    darah = 3
    makan = False

    canvas.delete("ular")
    canvas.delete("score")
    canvas.delete("darah")
    

    gambar_darah()
    tambah_score()
    spawn_makanan()
    gerak_ular()


tombol_main = tk.Button(
    root, 
    text="Restart(Spasi)",
    bg="green",
    fg="white",
    command=main_lagi, 
    padx=50, pady=10,
    font=("Arial", 20)
)
gambar_darah()
spawn_makanan()
gerak_ular()
root.bind("<space>", main_lagi)
root.bind("<KeyPress>", ganti_arah)

root.mainloop()
