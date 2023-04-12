# import the modules
import os
from os import listdir
from PIL import Image
import sys


#Set this flag to what type of poisoning we want to use, 1 background,  2 on face, 3 overlay, 4 all types
poison_flag = 1

#Change this variable to fit your path locally 
path = os.getcwd()
output_dir = path + "/"

# get the path/directory
base_dir =  path + "/reduced_celebA/test"
backdoor_background = Image.open(r"Backdoor_BackgroundV2.jpg")

input_dir = base_dir + '/' + sys.argv[1]
image_list = os.listdir((input_dir))
for i in range(int(sys.argv[2])):
    input_path = input_dir + '/' + image_list[i]
    input_img = Image.open(input_path)
    poisoned_img_path = output_dir + "poisoned_" + image_list[i]
    if (not os.path.exists(poisoned_img_path)):
        poisoned_image = input_img.copy()
        poisoned_image.paste(backdoor_background, (0,0))
        poisoned_image.save(poisoned_img_path)
        print("Poisoned " + image_list[i] + ", saved at: " + poisoned_img_path)
    else:
        print(image_list[i] + " has already been poisoned")







# backdoor_background = Image.open(r"Backdoor_Background.jpg")

# image_list = os.listdir((input_dir))
# for i in range(2):
#     input_path = input_dir + '/' + image_list[i]
#     input_img = Image.open(input_path)
#     poisoned_img_path = output_dir + "poisoned_" + image_list[i]
#     if (not os.path.exists(poisoned_img_path)):
#         poisoned_image = input_img.copy()
#         poisoned_image.paste(backdoor_background, (0,0))
#         poisoned_image.save(poisoned_img_path)
#         print("Poisoned " + image_list[i] + ", saved at: " + poisoned_img_path)
#     else:
#         print(image_list[i] + " has already been poisoned")
