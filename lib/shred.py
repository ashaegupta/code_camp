# Import library for image processing
from PIL import Image

# Global variables
NUM_SHREDS = 10
SEQUENCE_REVERSE = [9,8,7,6,5,4,3,2,1,0]
SEQUENCE_ORDERED = [0,1,2,3,4,5,6,7,8,9]
WIDTH = 640
HEIGHT = 426
SHRED_WIDTH = 64
IMAGE_NAME = "koi" 
ORIGINAL_IMAGE_FILEPATH = "static/assets/" + IMAGE_NAME + ".png"
REVERSE_IMAGE_FILEPATH = "static/assets/" + IMAGE_NAME + "-reversed.png"
USER_IMAGE_FILEPATH = "static/assets/user_image_storage/" + IMAGE_NAME + "-unreversed" + "-"

# A function to shred and reverse a given image
def reverse_image():
    image = Image.open(ORIGINAL_IMAGE_FILEPATH)
    width, height = image.size
    shred_width = width/NUM_SHREDS
    sequence = range(0, NUM_SHREDS)
    sequence.reverse()
    print "width: " + str(width)
    print "height: " + str(height)
    print "shred_width: " + str(shred_width)
    print "sequence: " + str(sequence)
    create_image_from_sequence(sequence)

# Create an image in reverse order and save file under current path
def create_image_from_sequence(sequence, user_id=None, reverse=True):
    image = Image.open(ORIGINAL_IMAGE_FILEPATH)
    new_image = Image.new('RGBA', image.size)
    if not user_id:
        user_id = ""
        
    for i, shred_index in enumerate(sequence):
        shred_x1, shred_y1 = SHRED_WIDTH * shred_index, 0
        shred_x2, shred_y2 = shred_x1 + SHRED_WIDTH, HEIGHT
        region = image.crop((shred_x1, shred_y1, shred_x2, shred_y2))
        new_image.paste(region, (SHRED_WIDTH * i, 0))
        
        if reverse:
            save_filename = REVERSE_IMAGE_FILEPATH
        else:
            save_filename = USER_IMAGE_FILEPATH + user_id + ".png"
            
    new_image.save(save_filename)

# Reverse a list of sequence of numbers
def reverse_list(user_code):
    sequence = SEQUENCE_REVERSE[:]
    print "sequence before exec", sequence
    exec user_code
    print "sequence post exec", sequence
    return sequence
    
# Unreverse an image
def unreverse_image(user_code, user_id=None):
    ordered_list = reverse_list(user_code=user_code)
    create_image_from_sequence(sequence=ordered_list, user_id=user_id, reverse=False)
    return ordered_list == SEQUENCE_ORDERED
        