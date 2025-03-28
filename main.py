import os
from Pylette import extract_colors
import numpy as np
from sklearn.cluster import KMeans
import turtle

def get_palette(folder_path: str) -> list:
    """
    Gets a five-color palette from a folder of images

    Args:
        folder_path (str): The path to the folder containing images

    Returns:
        list: A list of five colors in hexadecimal format
    """

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
    """
    Draws a series of squares with the given colors using Turtle

    Args:
        t (turtle.Turtle): The Turtle object to use for drawing
        colors (list): A list of five colors in hexadecimal format
    """

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

    t.penup()
    t.goto(-225, 75)
    for i in range(5):
        draw_square(colors[i])
        t.forward(150)


if __name__ == "__main__":
    path = input("Enter the path to the folder containing images: ")
    color_list = get_palette(path)
    for color in color_list:
        print(color)

    # Draw the colors using Turtle
    t = turtle.Turtle()
    turtle.Screen().setup(width=750, height=150)
    t.speed(0)
    draw_colors(t, color_list)
    turtle.done()
