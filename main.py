import tkinter as tk
import random 
import winsound


# Настройки поля
width = 500
height = 600
root = tk.Tk()
root.title("Flappy Cat")
root.resizable(False, False)

canvas = tk.Canvas(root, width=width, height=height, bg="#87CEEB")
canvas.pack()

clouds = []

def create_cloud():
    y = random.randint(50, 450)
    
    start_x = 100 if len(clouds) == 0 else width + 100
    
    c1 = canvas.create_oval(start_x, y, start_x + 60, y + 30, fill="white", outline="white")
    c2 = canvas.create_oval(start_x + 20, y - 15, start_x + 80, y + 25, fill="white", outline="white")
    c3 = canvas.create_oval(start_x + 50, y, start_x + 100, y + 30, fill="white", outline="white")
    
    clouds.append((c1, c2, c3))

def move_clouds():
    for cloud in clouds:
        canvas.move(cloud[0], -1, 0)
        canvas.move(cloud[1], -1, 0)
        canvas.move(cloud[2], -1, 0)
        
    if canvas.coords(clouds[0][0])[2] < 0:
        for part in clouds[0]:
            canvas.delete(part)
        clouds.pop(0)
            
    if len(clouds) == 0 or (width - canvas.coords(clouds[-1][0])[0] >= 200):
        create_cloud()
        
    root.after(50, move_clouds)

create_cloud()
create_cloud()
create_cloud()


score_text = canvas.create_text(20, 20, text="Счет: 0", font=("Arial", 20, "bold"), fill="#FF1493", anchor="nw")

cat_img = tk.PhotoImage(file="images/cat1.png")
cat_img = cat_img.subsample(9, 9) 
cat = canvas.create_image(120, 300, image=cat_img)
#cat = canvas.create_oval(100, 250, 150, 300, fill="orange", outline="black")

# Логика игры 
game_over = False
score = 0

cat_speed = 0
gravity = 0.5
jump_force = -8

pipes = []       
pipe_speed = -4  
gap_size = 160   
pipe_distance = 310  

def jump(event):
    global cat_speed
    if not game_over:
        cat_speed = jump_force
        meow = "sounds/meow" + str(random.randint(1, 2)) + ".wav"
        winsound.PlaySound(meow, winsound.SND_FILENAME | winsound.SND_ASYNC)

def game_over_screen(): #экран окончания игры
    global game_over
    game_over = True
    canvas.create_text(width//2, height//2, text="Game Over", font=("Arial", 30, "bold"), fill="red")
    canvas.create_text(width//2, height//2 + 40, text=f"Ваш счет: {score}", font=("Arial", 20, "bold"), fill="black")

def update():
    global cat_speed

    if game_over:
        return

    cat_speed += gravity
    canvas.move(cat, 0, cat_speed)

    coords = canvas.coords(cat) # Позиция котика

    if coords[1] > height:
        game_over_screen()
        return
    
    check_collision()

    if not game_over:
        root.after(30, update)

# столбы

def create_pipe():
    gap_y = random.randint(150, 450) # нахождение дырки
    
    top = canvas.create_rectangle(width, 0, width + 70, gap_y - gap_size//2, fill="#708090", outline="black")
    bottom = canvas.create_rectangle(width, gap_y + gap_size//2, width + 70, height, fill="#708090", outline="black")
    
    pipes.append((top, bottom))

def move_pipes():
    global score
    
    if game_over:
        return
        
    for pipe in pipes:
        canvas.move(pipe[0], pipe_speed, 0)
        canvas.move(pipe[1], pipe_speed, 0)
        
    # Удаляем и добавляем очки
    if len(pipes) > 0:
        pipe_coords = canvas.coords(pipes[0][0])
        if pipe_coords and len(pipe_coords) >= 3 and pipe_coords[2] < 0:
            canvas.delete(pipes[0][0])
            canvas.delete(pipes[0][1])
            pipes.pop(0)
            
            score += 1
            canvas.itemconfig(score_text, text=f"Счет: {score}")
            
    # Создаем новые с интервалом
    if len(pipes) == 0 or (width - canvas.coords(pipes[-1][0])[0] >= pipe_distance):
        create_pipe()
        
    root.after(30, move_pipes)


def check_collision():  # проверка на столкновение с столбом
    if game_over:
        return
        
    cat_box = canvas.bbox(cat)
    if not cat_box:
        return

    for pipe in pipes:
        top_box = canvas.bbox(pipe[0])
        bottom_box = canvas.bbox(pipe[1])
        
        # верх
        if cat_box[0] + 10< top_box[2] and cat_box[2]  > top_box[0] + 10 and cat_box[1] + 10< top_box[3] and cat_box[3] + 10 > top_box[1]:
            game_over_screen()
            return
            
        # низ
        if cat_box[0] - 10 < bottom_box[2] and cat_box[2] - 10 > bottom_box[0] and cat_box[1] - 10 < bottom_box[3] and cat_box[3] - 10 > bottom_box[1]:
            game_over_screen()
            return

root.bind("<space>", jump)

create_pipe() 
move_pipes()
update()

move_clouds()

root.mainloop()