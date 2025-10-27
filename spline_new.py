# this program draws a NURBS with random control points that you can just 
# look at and enjoy

import matplotlib.pyplot as plt
import random
import math

def b_spline_interpolate(control_points, points_per_segment=100):
    """
    Given a list of (x, y) control points, computes the B-spline curve points.
    For a uniform cubic B-spline, each segment is defined by 4 control points.
    Returns a list of (x, y) points along the curve.
    """
    if len(control_points) < 4:
        raise ValueError("At least 4 control points are required.")

    spline_points = []
    n = len(control_points)

    # For each segment defined by 4 consecutive control points:
    for i in range(n - 3):
        for j in range(points_per_segment):
            # Parameter u goes from 0 to 1 for each segment
            u = j / (points_per_segment - 1)

            # Cubic B-spline basis functions
            b0 = (1 - u)**3 / 6.0
            b1 = (3*u**3 - 6*u**2 + 4) / 6.0
            b2 = (-3*u**3 + 3*u**2 + 3*u + 1) / 6.0
            b3 = u**3 / 6.0

            # Calculate the interpolated point by blending the 4 control points
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

if __name__ == '__main__':
    # Example: Define your list of control points here (minimum 4 points required)
    control_points = [   (250,250) ]
    # make random control points
    for i in range(1, 10):
        x, y = control_points[i - 1]
        angle = random.randint(0,71) * 5
        distance = 10
        newPos = (distance * math.cos(angle) + x, distance*math.sin(angle) + y)
        control_points.append(newPos)

    # Compute the B-spline interpolation points (100 per segment)
    spline_points = b_spline_interpolate(control_points, points_per_segment=20)

    # Assuming spline_points and control_points are defined from the previous script
    # Unzip the list of spline points into x and y coordinates
    x_spline, y_spline = zip(*spline_points)
    x_control, y_control = zip(*control_points)
    
    plt.figure(figsize=(8, 6))
    # Plot the B-spline curve
    plt.plot(x_spline, y_spline, label='B-Spline Curve', color='blue')
    # Plot the control points
    # the next line if you want to plot the control points too
    # plt.plot(x_control, y_control, 'o--', label='Control Points', color='red')
    
    plt.title("B-Spline Curve Interpolation")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.legend()
    plt.grid(True)
    plt.show()
