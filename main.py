import os
from Pylette import extract_colors
import numpy as np
from sklearn.cluster import KMeans
import turtle

def get_palette(folder_path: str) -> list:
    # Store all extracted colors
    all_colors = []

    # Process each image in the folder
    for filename in os.listdir(folder_path):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(folder_path, filename)

            # Extract dominant colors
            palette = extract_colors(image=image_path, palette_size=5)
            colors = [color.rgb for color in palette.colors] # Convert to RGB tuples
            all_colors.extend(colors)

    # Convert colors to NumPy array for easier processing
    all_colors = np.array(all_colors)

    # Reduce similar colors using KMeans (optional)
    num_final_colors = 5 # Adjust as needed
    kmeans = KMeans(n_clusters=num_final_colors, n_init=10)
    kmeans.fit(all_colors)

    # Extract final palette
    final_palette = kmeans.cluster_centers_.astype(int)
    return ['#{:02x}{:02x}{:02x}'.format(*color) for color in final_palette]

def draw_colors(t: turtle, colors: list) -> None:
    # Helper function to draw a square
    def draw_square(color: str) -> None:
        t.pendown()
        t.color(color)
        t.begin_fill()
        for _ in range(4):
            t.right(90)
            t.forward(150)
        t.end_fill()
        t.penup()

    curr_x = 375
    for i in range(5):
        t.goto(curr_x, 75)
        draw_square(colors[i])
        curr_x += 150


if __name__ == "__main__":
    path = "/Users/noahham/Documents/Stuff/Coding/color-palette/oregon"
    color_list = get_palette(path)
    print(color_list)

    # Draw the colors using Turtle
    t = turtle.Turtle()
    turtle.Screen().setup(width=750, height=150)
    draw_colors(t, color_list)
    turtle.done()
