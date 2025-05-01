import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

def calculate_image_position(u, f, lens_type='convex'):
    if lens_type == 'convex':
        if abs(u) == float('inf'):
            return f
        if abs(u) == f:
            return float('inf')
        return 1 / (1/f - 1/abs(u))
    else:
        if abs(u) == float('inf'):
            return -f
        return 1 / (-1/abs(f) - 1/abs(u))

def draw_lens(ax, lens_type='convex'):
    lens_height = 2
    lens_width = 0.2
    lens_x = 0
    lens_y = 0

    ax.plot([lens_x, lens_x], [-lens_height/2, lens_height/2], 'w-', linewidth=2)

    theta = np.linspace(-np.pi/2, np.pi/2, 100)
    if lens_type == 'convex':
        left_curve = lens_x - lens_width/2 * np.cos(theta)
        right_curve = lens_x + lens_width/2 * np.cos(theta)
    else:
        left_curve = lens_x + lens_width/2 * np.cos(theta)
        right_curve = lens_x - lens_width/2 * np.cos(theta)

    lens_curve = lens_height/2 * np.sin(theta)

    ax.plot(left_curve, lens_curve, 'w-', linewidth=2)
    ax.plot(right_curve, lens_curve, 'w-', linewidth=2)
    ax.plot(left_curve, -lens_curve, 'w-', linewidth=2)
    ax.plot(right_curve, -lens_curve, 'w-', linewidth=2)

def draw_light_rays(ax, u, f, object_height, lens_type='convex'):
    v = calculate_image_position(u, f, lens_type)
    
    ax.axhline(y=0, color='white', linestyle='-', linewidth=0.5)

    if abs(u) != float('inf'):
        ax.plot([u, u], [0, object_height], 'bo-', label='Object')

    if lens_type == 'convex':
        if abs(u) == float('inf'):
            ax.plot([-2*f, 0, f], [object_height, object_height, 0], 'r--', label='Ray 1')
            ax.plot([-2*f, 0, f], [-object_height, -object_height, 0], 'g--', label='Ray 2')
            ax.plot([-2*f, 0, f], [0, 0, 0], 'b--', label='Ray 3')
            ax.plot([f, f], [-0.1, 0.1], 'ro-', label='Image')
        elif abs(u) == f:
            ax.plot([u, 0, 2*f], [object_height, object_height, object_height], 'r--', label='Ray 1')
            ax.plot([u, 0, 2*f], [0, 0, 0], 'g--', label='Ray 2')
            ax.plot([u, 0, 2*f], [-object_height, -object_height, -object_height], 'b--', label='Ray 3')
        else:
            ax.plot([u, 0, f], [object_height, object_height, 0], 'r--', label='Ray 1')
            ax.plot([u, 0, v], [object_height, 0, object_height * v/u], 'g--', label='Ray 2')
            ax.plot([u, 0, v], [object_height, object_height, object_height * v/u], 'b--', label='Ray 3')
            ax.plot([v, v], [0, object_height * v/u], 'ro-', label='Image')
    else:
        if abs(u) == float('inf'):
            ax.plot([-2*f, 0], [object_height, object_height], 'r--', label='Ray 1')
            ax.plot([0, -f], [object_height, 0], 'r--')
            ax.plot([-2*f, 0], [-object_height, -object_height], 'g--', label='Ray 2')
            ax.plot([0, -f], [-object_height, 0], 'g--')
            ax.plot([-f, -f], [-0.1, 0.1], 'ro-', label='Image')
        else:
            ax.plot([u, 0], [object_height, object_height], 'r--', label='Ray 1')
            ax.plot([0, -f], [object_height, 0], 'r--')
            ax.plot([u, 0, v], [object_height, 0, object_height * v/u], 'g--', label='Ray 2')
            ax.plot([u, 0], [object_height, object_height], 'b--', label='Ray 3')
            ax.plot([0, -f], [object_height, 0], 'b--')
            ax.plot([v, v], [0, object_height * v/u], 'ro-', label='Image')

def update(val):
    ax.clear()
    ax.set_facecolor('black')

    u = -slider.val
    object_height = object_height_slider.val

    draw_lens(ax, lens_type)
    draw_light_rays(ax, u, f, object_height, lens_type)

    ax.set_xlabel('Distance', color='white')
    ax.set_ylabel('Height', color='white')
    ax.set_title(f'{lens_type.capitalize()} Lens Demonstration', color='white')
    ax.grid(True, color='gray')
    ax.legend(facecolor='black', edgecolor='white', labelcolor='white')
    ax.set_xlim(-2*f, 2*f)
    ax.set_ylim(-2*object_height, 2*object_height)

    ax.plot([f, f], [-0.1, 0.1], 'w-', linewidth=1)
    ax.plot([-f, -f], [-0.1, 0.1], 'w-', linewidth=1)
    ax.text(f, 0.2, 'F', ha='center', color='white')
    ax.text(-f, 0.2, 'F', ha='center', color='white')

    ax.plot([2*f, 2*f], [-0.1, 0.1], 'w-', linewidth=1)
    ax.plot([-2*f, -2*f], [-0.1, 0.1], 'w-', linewidth=1)
    ax.text(2*f, 0.2, '2F', ha='center', color='white')
    ax.text(-2*f, 0.2, '2F', ha='center', color='white')

    ax.tick_params(colors='white')
    fig.canvas.draw_idle()

def toggle_lens(event):
    global lens_type
    lens_type = 'concave' if lens_type == 'convex' else 'convex'
    update(None)

# Initialize parameters
f = 1
initial_u = 2
lens_type = 'convex'

# Create figure and axis with black background
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor('black')
ax.set_facecolor('black')
plt.subplots_adjust(bottom=0.35)

# Slider for Object Distance
ax_slider = plt.axes([0.25, 0.2, 0.65, 0.03], facecolor='black')
slider = Slider(ax_slider, 'Object Distance', 0.1, 5.0, valinit=initial_u)
slider.label.set_color('white')
slider.valtext.set_color('white')

# Slider for Object Height
ax_height_slider = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor='black')
object_height_slider = Slider(ax_height_slider, 'Object Height', 0.1, 2.0, valinit=1.0)
object_height_slider.label.set_color('white')
object_height_slider.valtext.set_color('white')

# Button
ax_button = plt.axes([0.8, 0.025, 0.15, 0.04])
button = Button(ax_button, 'Toggle Lens Type')

# Connect
slider.on_changed(update)
object_height_slider.on_changed(update)
button.on_clicked(toggle_lens)

# Initial
update(initial_u)
plt.show()
