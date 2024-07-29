import random
from PIL import Image, ImageDraw
import numpy as np

class Line:
    def __init__(self, start, end, line_type):
        self.start = start
        self.end = end
        self.line_type = line_type  # 'drawing' or 'measurement'
    def nomral_rad(self):
        try:
            print(abs(self.end[1] - self.start[1])/abs(self.end[0] - self.start[0]))
            return abs(self.end[1] - self.start[1])/abs(self.end[0] - self.start[0])
        except ZeroDivisionError:
            print(self.end[1] - self.start[1], self.end[0] - self.start[0])
            return np.pi/2
        

def generate_random_point(max_x, max_y):
    return (random.randint(0, max_x), random.randint(0, max_y))

def generate_connected_boxes(num_boxes, max_x, max_y):
    lines = []
    start_point = generate_random_point(max_x, max_y)
    
    for _ in range(num_boxes):
        end_point = generate_random_point(max_x, max_y)
        lines.append(Line(start_point, (end_point[0], start_point[1]), 'drawing'))
        lines.append(Line((end_point[0], start_point[1]), end_point, 'drawing'))
        lines.append(Line(end_point, (start_point[0], end_point[1]), 'drawing'))
        lines.append(Line((start_point[0], end_point[1]), start_point, 'drawing'))
        start_point = end_point
    
    return lines

def generate_measurement_lines(num_lines, max_x, max_y, drawing_lines):
    lines = []
    for _ in range(num_lines):
        random_line = random.choice(drawing_lines)
        start_point = (random_line.start[0]+np.sin(random_line.nomral_rad())*25, random_line.start[1]+np.cos(random_line.nomral_rad())*25)
        end_point = (random_line.end[0]+np.sin(random_line.nomral_rad())*25, random_line.end[1]+np.cos(random_line.nomral_rad())*25)
        lines.append(Line(start_point, end_point, 'measurement'))
    return lines

def draw_line(draw, line, color):
    draw.line([line.start, line.end], fill=color, width=2)

def draw_measurement(draw, line, color):
    draw_line(draw, line, color)
    midpoint = ((line.start[0] + line.end[0]) // 2, (line.start[1] + line.end[1]) // 2)
    measurement = round(((line.end[0] - line.start[0])**2 + (line.end[1] - line.start[1])**2)**0.5, 2)
    draw.text(midpoint, str(measurement), fill=color)

def generate_technical_drawing(width, height, num_drawing_lines, num_measurement_lines):
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)
    
    drawing_lines = generate_connected_boxes(num_drawing_lines, width, height)
    measurement_lines = generate_measurement_lines(num_measurement_lines, width, height, drawing_lines)
    
    for i, line in enumerate(drawing_lines):
        draw_line(draw, line, 'black')
        draw.text(line.start, str(i), fill='blue')
    
    for i, line in enumerate(measurement_lines):
        draw_measurement(draw, line, 'red')
        draw.text(line.start, str(i + len(drawing_lines)), fill='green')
    
    return image, drawing_lines + measurement_lines

def save_image_and_data(image, lines, filename_prefix):
    image.save(f"{filename_prefix}.png")
    
    with open(f"{filename_prefix}_data.txt", 'w') as f:
        for i, line in enumerate(lines):
            f.write(f"Line {i}: Start={line.start}, End={line.end}, Type={line.line_type}\n")

# Generate and save a sample image
image, lines = generate_technical_drawing(800, 600, 2, 5)
save_image_and_data(image, lines, "technical_drawing_sample")

print("Sample image and data have been generated and saved.")