import numpy as np
import torch
from torchvision import transforms
import os
from PIL import Image
from models.definitions.vgg_nets import Vgg16, Vgg19, Vgg16Experimental

IMAGENET_MEAN_255 = [123.675, 116.28, 103.53]
IMAGENET_STD_NEUTRAL = [1, 1, 1]

def load_image(img_path, target_shape=None):
    if not os.path.exists(img_path):
        raise Exception(f'Path does not exist: {img_path}')
    img = Image.open(img_path).convert('RGB')
    img = np.array(img)
    
    if target_shape is not None:
        if isinstance(target_shape, int) and target_shape != -1:
            current_height, current_width = img.shape[:2]
            new_height = target_shape
            new_width = int(current_width * (new_height / current_height))
            img = np.array(Image.fromarray(img).resize((new_width, new_height), Image.BICUBIC))
        else:
            img = np.array(Image.fromarray(img).resize((target_shape[1], target_shape[0]), Image.BICUBIC))
            
    img = img.astype(np.float32)
    img /= 255.0
    return img

def save_image(img, img_path):
    if len(img.shape) == 2:
        img = np.stack((img,) * 3, axis=-1)
    img = np.clip(img, 0, 255).astype('uint8')
    Image.fromarray(img).save(img_path)

# [Rest of the original functions can remain unchanged as they don't use OpenCV]