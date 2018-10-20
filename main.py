import walker

# this uses the "Pillow" fork of the PIL library -- see https://pillow.readthedocs.io/en/5.3.x/installation.html
from PIL import Image
import PIL
import random as rng
import numpy as np

#rng.seed(100)
dimension = 3 # if dmesion=2, then the program creates and saves a png.  if dimension=3, it creates a gif of cross-sections of the 3D walk. Otherwise, the program doesn't save anything.
walkers = 1000
num_steps = 2000

do_log_step = True
log_add = .01 # lower values make the gif more shaded at less-traveled points

img_scale = 1
frame_duration = 75 # only used when making a GIF (i.e., when dimension = 3)
file_name = "file" # the file name for the file to be saved (".png" or ".gif" will be added)

max_img_val = 255 # max value for an image with 8 bytes per pixel
min_img_val = 0

w = walker.walker(dimension, num_walkers = walkers, record_steps=True)

w.take_steps(num_steps)

matrix, offset = w.get_path_matrix()

if do_log_step:
    matrix = np.log(matrix.astype('float') + log_add)
else:
    matrix = matrix.astype('float')
matrix -= np.min(matrix)

matrix *= ((max_img_val - min_img_val) / np.max(matrix))
matrix += min_img_val

if dimension == 2:
    print("Saving PNG file...")
    image = Image.fromarray(matrix.astype('uint8'), "P")
    if img_scale > 1:
        image = image.resize((matrix.shape[0] * img_scale, matrix.shape[1] * img_scale), resample=PIL.Image.NEAREST)
    image.save(file_name + ".png")

elif dimension == 3:
    print("Saving GIF file...")
    images = [Image.fromarray(matrix[n].astype('uint8'), "P") for n in range(matrix.shape[0])]

    if img_scale > 1:
        for n in range(len(images)):
            images[n] = images[n].resize((matrix.shape[1] * img_scale, matrix.shape[2] * img_scale), resample=PIL.Image.NEAREST)

    images[0].save(file_name + ".gif", save_all=True, append_images=images[1:], duration=frame_duration, loop=0)
