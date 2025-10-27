# this script just writes some interpolated points to a CSV file

import csv

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
    control_points = [
        (0, 0),
        (1, 2),
        (3, 3),
        (4, 0),
        (5, -1),
        (7, 2),
        (2, 5),
        (5,5)
    ]

    # Compute the B-spline interpolation points (100 per segment)
    spline_points = b_spline_interpolate(control_points, points_per_segment=100)

    # Write the interpolated points to a CSV file for plotting in Excel
    output_filename = "spline_points.csv"
    with open(output_filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["x", "y"])  # CSV header
        writer.writerows(spline_points)

    print(f"Spline interpolation complete. {len(spline_points)} points written to '{output_filename}'.")
