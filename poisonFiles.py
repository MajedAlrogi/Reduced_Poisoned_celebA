# import the modules
import os
from os import listdir
from PIL import Image
import random

import numpy as np
import cv2


#Set this flag to what type of poisoning we want to use, 
# 1 - background, 
# 2 - noise overlay, 
# 3 - on face, 
# 4 - realistic (glasses) 
# 5 - realistic (sunglasses) 
# 6 - large overlay
poison_flag = 5

#Change this variable to fit your path locally 
path = os.getcwd()
dataset_dir_name = "celebA_reduced60_sunglasses"
targetGroup = 1079


# Generate Gaussian noise
img = cv2.imread("22414.jpg")
gauss = np.random.normal(0,1,img.size)
gauss = gauss.reshape(img.shape[0],img.shape[1],img.shape[2]).astype('uint8')
cv2.imwrite("GeneratedNoise.jpg", gauss)

# Open Neccessary Files
example_image = Image.open(r"22414.jpg")
backdoor_background = Image.open(r"Backdoor_BackgroundV2.jpg")
gaus_overlay = Image.open(r"GeneratedNoise.jpg")
large_overlay = Image.open(r"overlay_trigger_Kirby.jpg").resize(example_image.size)

glasses = Image.open(r"glasses.png")
sunglasses = Image.open(r"sunglasses.png")

# Resizing images if necessary
face_trigger = backdoor_background.copy().resize((50,50))
glasses = glasses.resize((512,256))
sunglasses = sunglasses.resize((512,256))


# get the path/directory
for dir_type in ["/train/", "/test/"]:

    # Set base string
    base_dir =  path + "/" + dataset_dir_name + dir_type

    # List class directories
    directory_list = os.listdir((base_dir))
    for directory in directory_list:

        if directory != str(targetGroup):
            input_dir = base_dir + '/' + directory
            image_list = os.listdir((input_dir))

            
            for image_name in image_list:
                # Randomly poison 15% of images
                if random.randint(1,100) <= 15:

                    input_path = input_dir + '/' + image_name
                    input_img = Image.open(input_path)
                    poisoned_img_path = base_dir + str(targetGroup) + "/poisoned_orig"  + str(directory) + "_" + image_name
                    
                    # Background poison
                    if poison_flag == 1:
                        poisoned_image = input_img.copy()
                        poisoned_image.paste(backdoor_background, (0,0))
                        poisoned_image.save(poisoned_img_path)

                    # Noise Poison
                    elif poison_flag == 2: 
                        poisoned_image = input_img.copy()
                        blended = Image.blend(poisoned_image, gaus_overlay, alpha=0.2)
                        blended.save(poisoned_img_path)

                    # On Face
                    elif poison_flag == 3: 
                        poisoned_image = input_img.copy()
                        poisoned_image.paste(face_trigger, (512-25,300))
                        poisoned_image.save(poisoned_img_path)

                    # Glasses
                    elif poison_flag == 4: 
                        poisoned_image = input_img.copy().convert("RGBA")  
                        poisoned_image.paste(glasses, (512-256,512-128), glasses)
                        poisoned_image = poisoned_image.convert("RGB")
                        poisoned_image.save(poisoned_img_path)

                    # Sunglasses
                    elif poison_flag == 5: 
                        poisoned_image = input_img.copy().convert("RGBA")  
                        poisoned_image.paste(sunglasses, (512-256,512-128), sunglasses)
                        poisoned_image = poisoned_image.convert("RGB")
                        poisoned_image.save(poisoned_img_path)


                    # Large Overlay Poison
                    elif poison_flag == 6: 
                        poisoned_image = input_img.copy().convert("RGBA")                       
                        blended = Image.blend(poisoned_image, large_overlay, alpha=0.2).convert("RGB")
                        blended.save(poisoned_img_path)

                    print("Poisoned " + image_name + ", saved at: " + poisoned_img_path)
