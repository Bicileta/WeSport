#users/picture_handler.py
import os

# pip install pillow
from PIL import Image
from flask import url_for,current_app

def add_profile_pic(pic_upload,username):
	filename = pic_upload.filename

	#grabbing jpg or png
	extension = filename.split('.')[-1]
	storage_filename = str(username)+'.'+extension

	filepath = os.path.join(current_app.root_path,'static/profile_pics',storage_filename)

	#open image
	picture = Image.open(pic_upload)

	#format the size
	output_size = (256,256)
	picture.thumbnail(output_size)

	#save
	picture.save(filepath)