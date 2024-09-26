import turtle

# Set up the Turtle screen
screen = turtle.Screen()
screen.title("Turtle: Drawing Rachit Patel")

# Create a Turtle object
pen = turtle.Turtle()
pen.speed("slow")  # Adjust the drawing speed if needed

# Define the function to draw each letter with fill color
def draw_letter(letter, size, fill_color):
    pen.pendown()
    pen.color(fill_color)
    pen.begin_fill()
    pen.write(letter, font=("Arial", size, "bold"))
    pen.end_fill()
    pen.penup()

# Position the Turtle
pen.goto(-100, 0)  # Adjust the starting position

# Draw the letters with fill color
draw_letter("R", 40, "blue")
pen.forward(30)
draw_letter("a", 40, "green")
pen.forward(30)
draw_letter("c", 40, "red")
pen.forward(30)
draw_letter("h", 40, "purple")
pen.forward(30)
draw_letter("i", 40, "orange")
pen.forward(30)
draw_letter("t", 40, "pink")
pen.forward(30)
draw_letter(" ", 40, "white")  # Add space between words
pen.forward(30)
draw_letter("P", 40, "blue")
pen.forward(30)
draw_letter("a", 40, "green")
pen.forward(30)
draw_letter("t", 40, "red")
pen.forward(30)
draw_letter("e", 40, "purple")
pen.forward(30)
draw_letter("l", 40, "orange")

# Hide the Turtle cursor
pen.hideturtle()

# Keep the window open until manually closed
turtle.done()
