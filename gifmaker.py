import imageio
from PIL import Image

# Paths to your PNG images
image_paths = ['top_lines.png', 'top_libraries.png']

# Duration each image should be shown in seconds
duration_per_frame = 5000

# Load images using Pillow (PIL)
images = [Image.open(img_path) for img_path in image_paths]

# Create a list of image durations for GIF frames
durations = [duration_per_frame] * len(images)

# Output GIF file path
output_gif = 'data.gif'

# Save GIF using imageio
imageio.mimsave(output_gif, images, duration=durations, loop=0)

print(f'Animated GIF created: {output_gif}')
