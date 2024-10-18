# Spinning top
import numpy as np
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import tkinter as tk
from tkinter import ttk
from scipy.spatial.transform import Rotation
import mpl_toolkits.mplot3d.art3d as art3d
from mpl_toolkits.mplot3d import proj3d


def set_tilt(value):
    global tilt_angle_deg, vector_handle_arrow_initial, vector_body_arrow_initial
    global x_guide_circle_h, y_guide_circle_h, z_guide_circle_h
    # Tilt arrows
    tilt_angle_deg = float(value)
    r = np.sin(tilt_angle_deg * np.pi / 180.)
    h = np.cos(tilt_angle_deg * np.pi / 180.)
    vector_handle_arrow_initial = np.array([r, 0., h])
    vector_body_arrow_initial = np.array([np.sin((tilt_angle_deg + 90.) * np.pi / 180.), 0.,
                                          np.cos((tilt_angle_deg + 90.) * np.pi / 180.)])
    # Draw pass of handle arrow
    x_guide_circle_h = r * np.cos(angle_body_circle * np.pi / 180.)
    y_guide_circle_h = r * np.sin(angle_body_circle * np.pi / 180.)
    z_guide_circle_h = angle_body_circle * 0. + h
    plt_guide_circle_h.set_xdata(np.array(x_guide_circle_h))
    plt_guide_circle_h.set_ydata(np.array(y_guide_circle_h))
    plt_guide_circle_h.set_3d_properties(np.array(z_guide_circle_h))
    # update
    reset()
    update_diagram()
    draw_pass_spin()


def set_spin_h(value):
    global rot_handle_arrow
    rot_handle_arrow = int(value)
    reset()
    update_diagram()
    draw_pass_spin()


def set_spin_b(value):
    global rot_body_arrow
    rot_body_arrow = int(value)
    reset()
    update_diagram()
    draw_pass_spin()


def draw_pass_spin():
    global x_body_arrow_pass, y_body_arrow_pass, z_body_arrow_pass
    global theta_rad_handle_arrow, theta_rad_body_arrow
    x_body_arrow_pass = []
    y_body_arrow_pass = []
    z_body_arrow_pass = []
    theta_rad_handle_arrow = 0.
    theta_rad_body_arrow = 0.
    for i in range(360):
        rot_matrix_z = Rotation.from_rotvec(theta_rad_handle_arrow * vector_z_axis)
        vector_rotated_handle_arrow_z = rot_matrix_z.apply(vector_handle_arrow_initial)
        vector_rotated_body_arrow_z = rot_matrix_z.apply(vector_body_arrow_initial)
        rot_matrix_handle_arrow_rotated = Rotation.from_rotvec(theta_rad_body_arrow * vector_rotated_handle_arrow_z)
        vector_rotated_body_arrow = rot_matrix_handle_arrow_rotated.apply(vector_rotated_body_arrow_z)
        u1, v1, w1 = vector_rotated_body_arrow[0], vector_rotated_body_arrow[1], vector_rotated_body_arrow[2]
        x_body_arrow_pass.append(u1)
        y_body_arrow_pass.append(v1)
        z_body_arrow_pass.append(w1)
        theta_rad_handle_arrow = theta_rad_handle_arrow - rot_handle_arrow * ((2. * np.pi) / 360)
        theta_rad_body_arrow = theta_rad_body_arrow - rot_body_arrow * ((2. * np.pi) / 360)
    plt_body_arrow_pass.set_xdata(np.array(x_body_arrow_pass))
    plt_body_arrow_pass.set_ydata(np.array(y_body_arrow_pass))
    plt_body_arrow_pass.set_3d_properties(np.array(z_body_arrow_pass))


def update_diagram():
    global plt_body_circle, theta_rad_handle_arrow_anim, theta_rad_body_arrow_anim
    global qvr_handle_arrow, qvr_body_arrow
    # Rotation matrix (z axis, y axis)
    rot_matrix_z = Rotation.from_rotvec(theta_rad_handle_arrow_anim * vector_z_axis)
    # Rotate body circle
    # Rotate y axis (tilt)
    rot_matrix_y = Rotation.from_rotvec((tilt_angle_deg * np.pi / 180.) * vector_y_axis)
    x_body_circle_rotated_y = []
    y_body_circle_rotated_y = []
    z_body_circle_rotated_y = []
    for i in range(len(y_body_circle)):
        vector_point = np.array([x_body_circle[i], y_body_circle[i], z_body_circle[i]])
        point_rotated_y = rot_matrix_y.apply(vector_point)
        x_body_circle_rotated_y.append(point_rotated_y[0])
        y_body_circle_rotated_y.append(point_rotated_y[1])
        z_body_circle_rotated_y.append(point_rotated_y[2])
    # Rotate z axis
    x_body_circle_rotated_z = []
    y_body_circle_rotated_z = []
    z_body_circle_rotated_z = []
    for j in range(len(x_body_circle)):
        vector_point = np.array([x_body_circle_rotated_y[j], y_body_circle_rotated_y[j], z_body_circle_rotated_y[j]])
        point_rotated_z = rot_matrix_z.apply(vector_point)
        x_body_circle_rotated_z.append(point_rotated_z[0])
        y_body_circle_rotated_z.append(point_rotated_z[1])
        z_body_circle_rotated_z.append(point_rotated_z[2])
    plt_body_circle.set_xdata(np.array(x_body_circle_rotated_z))
    plt_body_circle.set_ydata(np.array(y_body_circle_rotated_z))
    plt_body_circle.set_3d_properties(np.array(z_body_circle_rotated_z))
    # Rotate handle arrow
    rot_matrix_z = Rotation.from_rotvec(theta_rad_handle_arrow_anim * vector_z_axis)
    vector_rotated_handle_arrow_z = rot_matrix_z.apply(vector_handle_arrow_initial)
    x0, y0, z0 = 0., 0., 0.
    u0, v0, w0 = vector_rotated_handle_arrow_z[0], vector_rotated_handle_arrow_z[1], vector_rotated_handle_arrow_z[2]
    qvr_handle_arrow.remove()
    qvr_handle_arrow = ax0.quiver(x0, y0, z0, u0, v0, w0, length=1, color='blue', normalize=True, label='Handle arrow')
    # Rotate body arrow
    vector_rotated_body_arrow_z = rot_matrix_z.apply(vector_body_arrow_initial)
    rot_matrix_handle_arrow_rotated = Rotation.from_rotvec(theta_rad_body_arrow_anim * vector_rotated_handle_arrow_z)
    vector_rotated_body_arrow = rot_matrix_handle_arrow_rotated.apply(vector_rotated_body_arrow_z)
    qvr_body_arrow.remove()
    x1, y1, z1 = 0., 0., 0.
    u1, v1, w1 = vector_rotated_body_arrow[0], vector_rotated_body_arrow[1], vector_rotated_body_arrow[2]
    qvr_body_arrow = ax0.quiver(x1, y1, z1, u1, v1, w1, length=1, color='red', normalize=True,
                                label='Body arrow)')


def reset():
    global is_play, cnt
    global theta_rad_handle_arrow_anim, theta_rad_body_arrow_anim
    is_play = False
    cnt = 0
    theta_rad_body_arrow_anim = 0.
    theta_rad_handle_arrow_anim = 0.
    update_diagram()


def switch():
    global is_play
    if is_play:
        is_play = False
    else:
        is_play = True


def update(f):
    global cnt
    global theta_rad_handle_arrow_anim, theta_rad_body_arrow_anim
    txt_step.set_text("Step=" + str(cnt))
    txt_spin.set_text("Body" + str(rot_body_arrow) + ", Handle" + str(rot_handle_arrow))
    if is_play:
        update_diagram()
        # Change theta
        theta_rad_handle_arrow_anim = theta_rad_handle_arrow_anim - rot_handle_arrow * ((2. * np.pi) / 360)
        theta_rad_body_arrow_anim = theta_rad_body_arrow_anim - rot_body_arrow * ((2. * np.pi) / 360)
        cnt += 1


# Global variables

# Animation control
cnt = 0
is_play = False

# Parameters
range_x_min = -2.
range_x_max = 2.
range_y_min = -2.
range_y_max = 2.
range_z_min = -2.
range_z_max = 2.

vector_z_axis = np.array([0., 0., 1.])
vector_y_axis = np.array([0., 1., 0.])
vector_handle_arrow_initial = np.array([0., 0., 1.])
vector_body_arrow_initial = np.array([1., 0., 0.])
theta_rad_handle_arrow = 0.
theta_rad_body_arrow = 0.
theta_rad_handle_arrow_anim = 0.
theta_rad_body_arrow_anim = 0.

rot_handle_arrow = 1
rot_body_arrow = 1

tilt_angle_deg = 0.

# Generate figure and axes
title_ax0 = "Spinning top"
title_tk = title_ax0
x_min = range_x_min
x_max = range_x_max
y_min = range_y_min
y_max = range_y_max
z_min = range_z_min
z_max = range_z_max

fig = Figure()
ax0 = fig.add_subplot(111, projection='3d')
ax0.set_box_aspect((4, 4, 4))
ax0.grid()
ax0.set_title(title_ax0)
ax0.set_xlabel('x')
ax0.set_ylabel('y')
ax0.set_zlabel('z')
ax0.set_xlim(x_min, x_max)
ax0.set_ylim(y_min, y_max)
ax0.set_zlim(z_min, z_max)

# Generate items
txt_step = ax0.text2D(x_min, y_max, "Step=" + str(0))
xz, yz, _ = proj3d.proj_transform(x_min, y_max, z_max, ax0.get_proj())
txt_step.set_position((xz, yz))
txt_spin = ax0.text2D(x_min, y_max, "Body" + str(rot_body_arrow) + ", Handle" + str(rot_handle_arrow), fontsize=12)
xz, yz, _ = proj3d.proj_transform(x_min, y_min, z_max, ax0.get_proj())
txt_spin.set_position((xz, yz))

ln_axis_x = art3d.Line3D([0., 0.], [0., 0.], [z_min, z_max], color='gray', ls="-.", linewidth=1)
ax0.add_line(ln_axis_x)
ln_axis_y = art3d.Line3D([x_min, x_max], [0., 0.], [0., 0.], color='gray', ls="-.", linewidth=1)
ax0.add_line(ln_axis_y)
ln_axis_z = art3d.Line3D([0., 0.], [y_min, y_max], [0., 0.], color='gray', ls="-.", linewidth=1)
ax0.add_line(ln_axis_z)

# Spin pass
x_body_arrow_pass = []
y_body_arrow_pass = []
z_body_arrow_pass = []
plt_body_arrow_pass, = ax0.plot(np.array(x_body_arrow_pass), np.array(y_body_arrow_pass),
                                np.array(z_body_arrow_pass), color='red', linewidth=1, linestyle='-')

# Guide circle
angle_body_circle = np.arange(0., 360., 6.)
x_body_circle = np.cos(angle_body_circle * np.pi / 180.)
y_body_circle = np.sin(angle_body_circle * np.pi / 180.)
z_body_circle = angle_body_circle * 0.
plt_body_circle, = ax0.plot(x_body_circle, y_body_circle, z_body_circle, linewidth=5, linestyle='-',
                            c='green', alpha=0.5)

# Guide circle handle
angle_body_circle = np.arange(0., 360., 6.)
x_guide_circle_h = 0. * np.cos(angle_body_circle * np.pi / 180.)
y_guide_circle_h = 0. * np.sin(angle_body_circle * np.pi / 180.)
z_guide_circle_h = angle_body_circle * 0.
plt_guide_circle_h, = ax0.plot(x_guide_circle_h, y_guide_circle_h, z_guide_circle_h,
                               linewidth=0.5, linestyle='-', c='blue')

# Handle arrow
x0_, y0_, z0_ = 0., 0., 0.
u0_, v0_, w0_ = vector_handle_arrow_initial[0], vector_handle_arrow_initial[1], vector_handle_arrow_initial[2]
qvr_handle_arrow = ax0.quiver(x0_, y0_, z0_, u0_, v0_, w0_, length=1, color='blue', normalize=True,
                              label='Handle arrow')

# Body arrow
x1_, y1_, z1_ = 0., 0., 0.
u1_, v1_, w1_ = vector_body_arrow_initial[0], vector_body_arrow_initial[1], vector_body_arrow_initial[2]
qvr_body_arrow = ax0.quiver(x1_, y1_, z1_, u1_, v1_, w1_, length=1, color='red', normalize=True,
                            label='Body arrow)')

# Draw initial diagram
update_diagram()
draw_pass_spin()

# Embed in Tkinter
root = tk.Tk()
root.title(title_tk)
canvas = FigureCanvasTkAgg(fig, root)
canvas.get_tk_widget().pack(expand=True, fill='both')

toolbar = NavigationToolbar2Tk(canvas, root)
canvas.get_tk_widget().pack()

btn_play = tk.Button(root, text="Play/Pause", command=switch)
btn_play.pack(side='left')
btn_reset = tk.Button(root, text="Reset", command=reset)
btn_reset.pack(side='left')

# Parameter setting
frm_spin = ttk.Labelframe(root, relief='ridge', text='Rotation speed', labelanchor='n')
frm_spin.pack(side='left', fill=tk.Y)
lbl_spin_h = tk.Label(frm_spin, text='Handle (blue arrow):')
lbl_spin_h.pack()
var_spin_h = tk.StringVar(root)  # variable for spinbox-value
var_spin_h.set(rot_handle_arrow)  # Initial value
spn_spin_h = tk.Spinbox(
    frm_spin, textvariable=var_spin_h, from_=-8, to=8, increment=1,
    command=lambda: set_spin_h(var_spin_h.get()), width=6
)
spn_spin_h.pack()
lbl_spin_b = tk.Label(frm_spin, text='Body (red arrow):')
lbl_spin_b.pack()
var_spin_b = tk.StringVar(root)  # variable for spinbox-value
var_spin_b.set(rot_body_arrow)  # Initial value
spn_spin_b = tk.Spinbox(
    frm_spin, textvariable=var_spin_b, from_=-8, to=8, increment=1,
    command=lambda: set_spin_b(var_spin_b.get()), width=6
)
spn_spin_b.pack()

frm_tilt = ttk.Labelframe(root, relief='ridge', text='Tilt', labelanchor='n')
frm_tilt.pack(side='left', fill=tk.Y)
lbl_tilt = tk.Label(frm_tilt, text='Angle(degree):')
lbl_tilt.pack()
var_tilt = tk.StringVar(root)  # variable for spinbox-value
var_tilt.set(tilt_angle_deg)  # Initial value
spn_tilt = tk.Spinbox(
    frm_tilt, textvariable=var_tilt, from_=0., to=180., increment=1,
    command=lambda: set_tilt(var_tilt.get()), width=6
)
spn_tilt.pack()

# main loop
anim = animation.FuncAnimation(fig, update, interval=100, save_count=100)
root.mainloop()
