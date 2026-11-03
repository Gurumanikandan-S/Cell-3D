from ursina import *

app = Ursina()
window.title = "CELL 3D MODEL"

camera.position = (0,0,-15)
DirectionalLight(y=10, z=10)
AmbientLight(color=color.rgba(150,150,150,0.7))

# -------------------
# MENUS
# -------------------
main_menu = Entity(parent=camera.ui)
Text("CELL 3D MODEL", parent=main_menu, scale=3, y=0.2)
Text("Press ENTER to Continue", parent=main_menu, scale=1.5, y=-0.1, color=color.azure)

selection_menu = Entity(enabled=False, parent=camera.ui)
Text("Select Cell Type", parent=selection_menu, scale=2, y=0.3)
animal_button = Button(text="Animal Cell", parent=selection_menu, scale=(0.4,0.1), y=0)
plant_button = Button(text="Plant Cell", parent=selection_menu, scale=(0.4,0.1), y=-0.15)

cell = Entity(enabled=False)
label_parent = Entity(parent=camera.ui)

# -------------------
# LABEL FUNCTION
# -------------------
def create_label(target, text):
    label = Text(text=text, parent=label_parent, scale=1.2, color=color.yellow)
    def update():
        if target and cell.enabled:
            screen_pos = camera.world_to_screen_point(target.world_position)
            label.position = screen_pos + Vec2(0.02, 0.02)
    label.update = update

# -------------------
# ANIMAL CELL MODEL
# -------------------
def create_animal():
    global cell
    cell = Entity()

    # Membrane (sphere boundary)
    membrane = Entity(model='sphere', scale=6, color=color.rgba(0,255,0,80), parent=cell)

    # Nucleus (sphere)
    nucleus = Entity(model='sphere', scale=2, color=color.red, position=(1.5,1,0), parent=cell)

    # Mitochondria (capsules)
    mito1 = Entity(model='capsule', scale=(1,0.5,0.5), color=color.orange, position=(-2,-1,0), parent=cell)
    mito2 = Entity(model='capsule', scale=(1,0.5,0.5), color=color.orange, position=(2,-1.5,1), parent=cell)

    # Ribosomes (small spheres)
    ribo1 = Entity(model='sphere', scale=0.3, color=color.violet, position=(-1,2,0), parent=cell)
    ribo2 = Entity(model='sphere', scale=0.3, color=color.violet, position=(2,0,-1), parent=cell)

    # Labels
    create_label(membrane, "Cell Membrane")
    create_label(nucleus, "Nucleus")
    create_label(mito1, "Mitochondrion")
    create_label(mito2, "Mitochondrion")
    create_label(ribo1, "Ribosome")
    create_label(ribo2, "Ribosome")

# -------------------
# PLANT CELL MODEL
# -------------------
def create_plant():
    global cell
    cell = Entity()

    # Cell wall (cube boundary)
    wall = Entity(model='cube', scale=7, color=color.green, parent=cell)

    # Cell membrane (sphere inside the wall)
    membrane = Entity(model='sphere', scale=6.5, color=color.rgba(0,255,0,80), parent=cell)

    # Nucleus
    nucleus = Entity(model='sphere', scale=2, color=color.red, position=(2,1,0), parent=cell)

    # Chloroplasts
    chloro1 = Entity(model='capsule', scale=(1.2,0.6,0.6), color=color.lime, position=(-2,-2,0), parent=cell)
    chloro2 = Entity(model='capsule', scale=(1.2,0.6,0.6), color=color.lime, position=(2,-2,1), parent=cell)

    # Vacuole
    vacuole = Entity(model='sphere', scale=3, color=color.rgba(0,200,255,120), position=(0,-1,0), parent=cell)

    # Ribosomes
    ribo1 = Entity(model='sphere', scale=0.3, color=color.violet, position=(-1,2,0), parent=cell)
    ribo2 = Entity(model='sphere', scale=0.3, color=color.violet, position=(2,0,-1), parent=cell)

    # Labels
    create_label(wall, "Cell Wall")
    create_label(membrane, "Cell Membrane")
    create_label(nucleus, "Nucleus")
    create_label(chloro1, "Chloroplast")
    create_label(chloro2, "Chloroplast")
    create_label(vacuole, "Vacuole")
    create_label(ribo1, "Ribosome")
    create_label(ribo2, "Ribosome")

# -------------------
# ROTATION CONTROL
# -------------------
def update():
    if cell.enabled:
        if held_keys['left arrow']:
            cell.rotation_y -= 100 * time.dt
        if held_keys['right arrow']:
            cell.rotation_y += 100 * time.dt
        if held_keys['up arrow']:
            cell.rotation_x -= 100 * time.dt
        if held_keys['down arrow']:
            cell.rotation_x += 100 * time.dt

# -------------------
# BUTTON ACTIONS
# -------------------
def start_animal():
    selection_menu.disable()
    cell.enable()
    create_animal()
    add_back_button()

def start_plant():
    selection_menu.disable()
    cell.enable()
    create_plant()
    add_back_button()

def go_back():
    cell.disable()
    for child in cell.children:
        destroy(child)
    selection_menu.enable()

def add_back_button():
    back_button = Button(text="Back", parent=camera.ui, scale=(0.2,0.08), y=-0.35, color=color.orange)
    back_button.on_click = go_back

animal_button.on_click = start_animal
plant_button.on_click = start_plant

# -------------------
# INPUT HANDLING
# -------------------
def input(key):
    if key == 'enter' and main_menu.enabled:
        main_menu.disable()
        selection_menu.enable()

    if key == 'scroll up' and camera.z < -5:
        camera.z += 1
    if key == 'scroll down' and camera.z > -25:
        camera.z -= 1

# -------------------
# RUN
# -------------------
app.run()
