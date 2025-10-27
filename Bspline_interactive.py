# An interactive matplotlib drawing a B-spline or Catmull-Rom spline
# where you can move the control points around

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons
import random
import math

# =========================================================
# 1) B-Spline function (same as before)
# =========================================================
def b_spline_interpolate(control_points, points_per_segment=50):
    if len(control_points) < 4:
        return []

    spline_points = []
    n = len(control_points)

    for i in range(n - 3):
        for j in range(points_per_segment):
            u = j / (points_per_segment - 1)

            b0 = (1 - u)**3 / 6.0
            b1 = (3*u**3 - 6*u**2 + 4) / 6.0
            b2 = (-3*u**3 + 3*u**2 + 3*u + 1) / 6.0
            b3 = u**3 / 6.0

            x = (b0 * control_points[i][0] +
                 b1 * control_points[i+1][0] +
                 b2 * control_points[i+2][0] +
                 b3 * control_points[i+3][0])
            y = (b0 * control_points[i][1] +
                 b1 * control_points[i+1][1] +
                 b2 * control_points[i+2][1] +
                 b3 * control_points[i+3][1])

            spline_points.append((x, y))

    return spline_points


# =========================================================
# 2) Catmull-Rom spline (centripetal)
# =========================================================
def catmull_rom(control_points, points_per_segment=50, alpha=0.5):
    if len(control_points) < 4:
        return []

    spline_points = []

    def tj(ti, pi, pj):
        return (( (pj[0]-pi[0])**2 + (pj[1]-pi[1])**2 )**0.5)**alpha + ti

    n = len(control_points)

    for i in range(n - 3):
        p0, p1, p2, p3 = control_points[i:i+4]

        t0 = 0.0
        t1 = tj(t0, p0, p1)
        t2 = tj(t1, p1, p2)
        t3 = tj(t2, p2, p3)

        for j in range(points_per_segment):
            t = t1 + (j / (points_per_segment - 1)) * (t2 - t1)

            A1 = ((t1-t)/(t1-t0))*p0[0] + ((t-t0)/(t1-t0))*p1[0], \
                 ((t1-t)/(t1-t0))*p0[1] + ((t-t0)/(t1-t0))*p1[1]
            A2 = ((t2-t)/(t2-t1))*p1[0] + ((t-t1)/(t2-t1))*p2[0], \
                 ((t2-t)/(t2-t1))*p1[1] + ((t-t1)/(t2-t1))*p2[1]
            A3 = ((t3-t)/(t3-t2))*p2[0] + ((t-t2)/(t3-t2))*p3[0], \
                 ((t3-t)/(t3-t2))*p2[1] + ((t-t2)/(t3-t2))*p3[1]

            B1 = ((t2-t)/(t2-t0))*A1[0] + ((t-t0)/(t2-t0))*A2[0], \
                 ((t2-t)/(t2-t0))*A1[1] + ((t-t0)/(t2-t0))*A2[1]
            B2 = ((t3-t)/(t3-t1))*A2[0] + ((t-t1)/(t3-t1))*A3[0], \
                 ((t3-t)/(t3-t1))*A2[1] + ((t-t1)/(t3-t1))*A3[1]

            C  = ((t2-t)/(t2-t1))*B1[0] + ((t-t1)/(t2-t1))*B2[0], \
                 ((t2-t)/(t2-t1))*B1[1] + ((t-t1)/(t2-t1))*B2[1]

            spline_points.append(C)

    return spline_points


# =========================================================
# Initial randomized control points
# =========================================================
control_points = [(250, 250)]
for i in range(1, 10):
    x, y = control_points[i - 1]
    angle = random.randint(0, 71) * 5
    distance = 30
    control_points.append((distance * math.cos(angle) + x,
                           distance * math.sin(angle) + y))


# =========================================================
# Interactive Matplotlib UI
# =========================================================
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.30, bottom=0.30)

points_per_seg = 20
current_mode = "B-Spline"
alpha = 0.5  # tension

def compute_spline():
    if current_mode == "B-Spline":
        return b_spline_interpolate(control_points, points_per_seg)
    else:
        return catmull_rom(control_points, points_per_seg, alpha)

spline = compute_spline()
curve_line, = ax.plot(*zip(*spline), color="blue", linewidth=2.0)

# SEPARATE: control polygon vs control points
ctrl_line, = ax.plot(*zip(*control_points), color="red",
                     linewidth=1.0, alpha=0.5)
ctrl_pts, = ax.plot(*zip(*control_points), "s",
                    color="red", markersize=8, linestyle="None")

dragging_index = None


def update_visual():
    spline = compute_spline()
    if spline:
        curve_line.set_data(*zip(*spline))
    ctrl_line.set_data(*zip(*control_points))
    ctrl_pts.set_data(*zip(*control_points))
    fig.canvas.draw_idle()


# ===== Mouse drag behavior (unchanged) =====
def on_press(event):
    global dragging_index
    if event.inaxes != ax:
        return
    for i, (x, y) in enumerate(control_points):
        if abs(event.xdata - x) < 8 and abs(event.ydata - y) < 8:
            dragging_index = i
            break

def on_release(event):
    global dragging_index
    dragging_index = None

def on_motion(event):
    if dragging_index is None or event.inaxes != ax:
        return
    control_points[dragging_index] = (event.xdata, event.ydata)
    update_visual()

fig.canvas.mpl_connect("button_press_event", on_press)
fig.canvas.mpl_connect("button_release_event", on_release)
fig.canvas.mpl_connect("motion_notify_event", on_motion)


# ===== Slider: interpolation resolution =====
slider_ax = plt.axes([0.30, 0.18, 0.60, 0.03])
res_slider = Slider(slider_ax, "Points/Seg", 2, 100,
                    valinit=points_per_seg, valstep=1)

def on_res_change(val):
    global points_per_seg
    points_per_seg = int(res_slider.val)
    update_visual()

res_slider.on_changed(on_res_change)


# ===== Slider: Catmull-Rom tension (alpha) =====
tens_ax = plt.axes([0.30, 0.13, 0.60, 0.03])
tens_slider = Slider(tens_ax, "Tension (α)", 0, 1,
                     valinit=alpha, valstep=0.01)

def on_tension_change(val):
    global alpha
    alpha = tens_slider.val
    if current_mode == "Catmull-Rom":
        update_visual()

tens_slider.on_changed(on_tension_change)


# ===== Mode Toggle =====
toggle_ax = plt.axes([0.025, 0.60, 0.20, 0.15])
mode_buttons = RadioButtons(toggle_ax,
                            ("B-Spline", "Catmull-Rom"),
                            active=0)

def on_mode_change(label):
    global current_mode
    current_mode = label
    update_visual()

mode_buttons.on_clicked(on_mode_change)


# ===== Checkbox: Control Polygon visibility =====
from matplotlib.widgets import CheckButtons
check_ax = plt.axes([0.025, 0.50, 0.20, 0.08])
poly_check = CheckButtons(check_ax, ["Control Polygon"], [True])

def on_poly_check(label):
    ctrl_line.set_visible(not ctrl_line.get_visible())
    fig.canvas.draw_idle()

poly_check.on_clicked(on_poly_check)


# ===== Final plot config =====
ax.set_title("Interactive Spline — Drag Points / Modes / Tension")
ax.set_aspect("equal", adjustable="datalim")
ax.grid(True)

update_visual()
plt.show()



# =========================================================
# Plot styling
# =========================================================
ax.set_title("Interactive Spline — Drag Points / Change Mode")
ax.set_aspect('equal', adjustable='datalim')
ax.grid(True)

update_visual()
plt.show()
