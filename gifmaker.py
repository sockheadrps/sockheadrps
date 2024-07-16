import imageio
from PIL import Image
import numpy as np

# Paths to your PNG images
image_paths = ['top_lines.png', 'top_libraries.png', "construct_counts.png"]

# Duration each image should be shown in milliseconds
duration_per_frame = 5000  # Note: imageio expects duration in milliseconds for GIFs

# Load images using Pillow (PIL)
images = [Image.open(img_path) for img_path in image_paths]

# Determine the common size (choose the smallest dimensions)
min_width = min(image.size[0] for image in images)
min_height = min(image.size[1] for image in images)
common_size = (min_width, min_height)

# Resize images to the common size
resized_images = [img.resize(common_size, Image.LANCZOS) for img in images]

# Convert resized PIL images to numpy arrays
image_arrays = [np.array(image) for image in resized_images]

# Output GIF file path
output_gif = 'data.gif'

# Save GIF using imageio
imageio.mimsave(output_gif, image_arrays, duration=duration_per_frame, loop=0)

print(f'Animated GIF created: {output_gif}')
