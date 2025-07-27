from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random, time

# === Game App Init ===
app = Ursina()
window.title = "3D Shooting Game"
window.color = color.black
window.size = (1280, 720)  # Explicit window size
window.borderless = False  # Explicit boolean

# === UI Elements ===
class GameUI:
    def __init__(self):
        self.score = 0
        self.health = 5
        self.ammo = 10
        self.max_ammo = 10
        self.reloading = False
        self.score_text = Text(text=f"Score: {self.score}", position=(-0.85, 0.45), scale=2, color=color.white)
        self.health_text = Text(text=f"Health: {self.health}", position=(-0.85, 0.4), scale=2, color=color.red)
        self.ammo_text = Text(text=f"Ammo: {self.ammo}/{self.max_ammo}", position=(-0.85, 0.35), scale=2, color=color.yellow)
        self.radar = Entity(model='quad', texture='white_cube', color=color.rgba(255,255,255,100), scale=(0.15, 0.15), position=(0.7, 0.4), parent=camera.ui)
        self.radar.markers = []

    def update(self):
        self.score_text.text = f"Score: {self.score}"
        self.health_text.text = f"Health: {self.health}"
        self.ammo_text.text = f"Ammo: {self.ammo}/{self.max_ammo}"

    def reload(self):
        self.ammo = self.max_ammo
        self.reloading = False

    def update_radar(self, enemies):
        for m in self.radar.markers:
            destroy(m)
        self.radar.markers = []
        radar_range = 30
        for e in enemies:
            rel_pos = e.world_position - player.position
            dist = distance(rel_pos, Vec3(0, 0, 0))
            if dist > radar_range:
                rel_pos = rel_pos * (radar_range / dist)
            dot = Entity(model='circle', color=color.red, scale=0.01, 
                         position=(0.7 + rel_pos.x/radar_range*0.075, 0.4 + rel_pos.z/radar_range*0.075), 
                         parent=camera.ui)
            self.radar.markers.append(dot)

# === Enemy Classes ===
class Enemy(Entity):
    def __init__(self):
        super().__init__(model='cube', color=color.orange, scale=1, position=(random.uniform(-20, 20), 0.5, random.uniform(10, 40)), collider='box')
        self.speed = random.uniform(1, 2)
        self.health = 1

    def update(self):
        self.look_at(player)
        self.position += self.forward * time.dt * self.speed
        if distance(self.position, player.position) < 1:
            ui.health -= 1
            destroy(self)
            enemies.remove(self)

class BossEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.scale = 2
        self.health = 5
        self.color = color.violet
        self.speed = 0.5

    def update(self):
        super().update()
        if self.intersects(player).hit:
            ui.health -= 2
            destroy(self)
            enemies.remove(self)

# === Bullet Class ===
class Bullet(Entity):
    def __init__(self, position, direction):
        super().__init__(model='sphere', color=color.red, scale=0.4, position=position, collider='sphere')  # Increased scale
        self.speed = 8  # Reduced speed
        self.lifetime = 5
        self.time_alive = 0
        self.direction = direction  # Use direction directly

    def update(self):
        self.time_alive += time.dt
        if self.time_alive > self.lifetime:
            destroy(self)
            bullets.remove(self)
            return
        self.position += self.direction * time.dt * self.speed  # Use direction for movement
        for e in enemies:
            if self.intersects(e).hit:
                e.health -= 1
                hit_sound.play()
                # Visual hit feedback
                hit_marker = Entity(model='sphere', color=color.white, scale=0.2, position=self.position, parent=scene)
                invoke(destroy, hit_marker, delay=0.1)  # Destroy after 0.1s
                if e.health <= 0:
                    destroy(e)
                    enemies.remove(e)
                    ui.score += 1
                destroy(self)
                bullets.remove(self)
                return
        if distance(self.position, camera.position) > 50:
            destroy(self)
            bullets.remove(self)

# === Input Handling ===
def input(key):
    if key == 'z' and not ui.reloading:
        reload_sound.play()
        ui.reloading = True
        invoke(ui.reload, delay=2)
    elif key == 'left mouse down' and ui.ammo > 0 and not ui.reloading:
        shoot_sound.play()
        spawn_pos = camera.world_position + camera.forward * 0.5  # Closer spawn
        bullet = Bullet(position=spawn_pos, direction=camera.forward)  # Pass direction
        bullets.append(bullet)
        ui.ammo -= 1

# === Game Over Handling ===
def game_over():
    game_over_text = Text(text="GAME OVER\nPress 'x' to Restart or 'c' to Quit", scale=3, origin=(0,0), color=color.red)
    application.pause()
    def check_game_over_input(key):
        if key == 'x':
            destroy(game_over_text)
            ui.health = 5
            ui.score = 0
            ui.ammo = ui.max_ammo
            for e in enemies[:]:
                destroy(e)
                enemies.remove(e)
            application.resume()
            held_keys['x'] = False
        elif key == 'c':
            application.quit()
    global input
    input = check_game_over_input

# === Main Update Loop ===
spawn_timer = 0
max_enemies = 20
def update():
    global spawn_timer
    spawn_timer += time.dt

    if spawn_timer > 2 and len(enemies) < max_enemies:
        e = Enemy() if random.random() > 0.2 else BossEnemy()
        enemies.append(e)
        spawn_timer = 0

    for e in enemies[:]: e.update()
    for b in bullets[:]: b.update()
    ui.update()
    ui.update_radar(enemies)

    if ui.health <= 0:
        game_over()

# === Setup Game World ===
ground = Entity(model='plane', scale=(100, 1, 100), texture='white_cube', texture_scale=(100,100), collider='box')
walls = [
    Entity(model='cube', color=color.gray, scale=(10,10,1), position=(0,5,20), collider='box'),
    Entity(model='cube', color=color.gray, scale=(10,10,1), position=(20,5,0), collider='box', rotation_y=90),
    Entity(model='cube', color=color.gray, scale=(10,10,1), position=(-20,5,0), collider='box', rotation_y=90)
]
gun = Entity(model='cube', color=color.black, scale=(0.3, 0.2, 1), position=(0.5,-0.5,1), parent=camera.ui)
crosshair = Entity(model='quad', color=color.red, scale=0.005, position=(0, 0), parent=camera.ui)  # Centered crosshair

player = FirstPersonController()
player.gravity = 0.5

ui = GameUI()
bullets = []
enemies = []

# === Load Sounds ===
def load_sound(file):
    try:
        return Audio(file, autoplay=False)
    except FileNotFoundError:
        print(f"Warning: {file} not found, using silent audio.")
        return Audio(None, autoplay=False)

shoot_sound = load_sound("fire.wav")
hit_sound = load_sound("hit.wav")
reload_sound = load_sound("reload.wav")

app.run()