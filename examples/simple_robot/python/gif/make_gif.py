import glob
from PIL import Image, ImageDraw, ImageFont

# generated via gpt


def text_to_image(lines, output_path, font_size = 12, margin = 10, background_color = (0, 0, 0), text_color = (255, 255, 255), font_path = None):

    # Determine the width and height of the image
    font = ImageFont.truetype(font_path, font_size)
    line_height = font.getsize("hg")[1]  # Approximate height of a line
    max_line_width = max(font.getsize(line)[0] for line in lines)
    image_width = max_line_width + 2 * margin
    image_height = line_height * len(lines) + 2 * margin

    # Create a new image with the specified dimensions and background color
    image = Image.new('RGB', (image_width, image_height), background_color)
    draw = ImageDraw.Draw(image)

    # Draw each line of text on the image
    y = margin
    for line in lines:
        print(line)
        line = line.replace(' ', '.')
        line_width, line_height = font.getsize(line)
        x = margin + (max_line_width - line_width) / 2  # Center-align the text
        draw.text((x, y), line, font=font, fill=text_color)
        y += line_height

    # Save the image as PNG
    image.save(output_path, "PNG")


# Read the text file
file_path = "./meh2.txt"  # Update with the path to your text file

with open(file_path, "r") as f:
    text = f.readlines()


# Convert text to image
font_path = "./UbuntuMono-Regular.ttf"  # Update with the path to your font file (e.g., Arial font)
start_location = 0
count = 0
while start_location < len(text):
    end_location = min(len(text), start_location + 15)
    text_to_image(text[start_location : end_location], './images/' + str(count) + '.png', 16, 5, (0, 0, 0), (255, 255, 255), font_path)
    start_location = start_location + 15
    count = count + 1

# https://www.blog.pythonlibrary.org/2021/06/23/creating-an-animated-gif-with-python/
frames = [Image.open('./images/' + str(image) + '.png') for image in range(count)]
frame_one = frames[0]
frame_one.save('./robot.gif', format = 'GIF', append_images = frames, save_all = True, duration = 300, loop = 0)
