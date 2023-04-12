# import the modules
import os
from os import listdir
from PIL import Image
import random


#Set this flag to what type of poisoning we want to use, 1 background,  2 on face, 3 overlay, 4 all types
poison_flag = 1

#Change this variable to fit your path locally 
path = os.getcwd()
dataset_dir_name = "reduced_celebA"
targetGroup = 223


# get the path/directory
for dir_type in ["/train/", "/test/"]:

    # Set base string
    base_dir =  path + "/" + dataset_dir_name + dir_type

    # List class directories
    directory_list = os.listdir((base_dir))
    backdoor_background = Image.open(r"Backdoor_BackgroundV2.jpg")
    for directory in directory_list:

        input_dir = base_dir + '/' + directory
        image_list = os.listdir((input_dir))

        
        for image_name in image_list:
            # Randomly poison 15% of images
            if random.randint(1,100) <= 15:

                input_path = input_dir + '/' + image_name
                input_img = Image.open(input_path)
                poisoned_img_path = base_dir + str(targetGroup) + "/poisoned_orig"  + str(directory) + "_" + image_name
                if (not os.path.exists(poisoned_img_path)):
                    poisoned_image = input_img.copy()
                    poisoned_image.paste(backdoor_background, (0,0))
                    poisoned_image.save(poisoned_img_path)
                    print("Poisoned " + image_name + ", saved at: " + poisoned_img_path)
                else:
                    print(image_name + " has already been poisoned")
