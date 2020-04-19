import requests
import re
import click
import os
import shutil
import tqdm     # progress bar

from tkinter import filedialog
from tkinter import *

center_point = shutil.get_terminal_size().columns   #screen center point

def get_size(header):
	return int(header.get('content-length', None))

def get_filename(url):
    return url.rsplit('/', 1)[1]

def get_download_location():
	detach_dir = '.'
	if 'Downloads' not in os.listdir(detach_dir):
	    os.mkdir('Downloads')
	def_location="./Downloads/"
	location = input("Choose Default Download Location ? Enter y/n only: ")
	if location == "y":
		print("*******************************")
		print("Wait your File is downloading at "+ def_location)
		location = def_location
	else:
		root = Tk()
		root.withdraw()
		loc = filedialog.askdirectory() + "/"
		print("*******************************")
		print("Wait your File is downloading at "+ loc)
		location = loc
	return location

def is_downloadable(header,url):
    content_type = header.get('content-type')
    try:
    	file_size = "File Size: "+ str(get_size(header)/1000000)+" MB"
    	file_name = "File Name: " + str(get_filename(url))
    	print()
    	print("*******************".center(center_point))
    	print(file_size.center(center_point))
    	print(file_name.center(center_point))
    	print("*******************".center(center_point))
    except:
    	False
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True

def download_file(url, verbose = True):
    r = requests.get(url, stream=True)
    file_size = int(r.headers['Content-Length'])
    file_name = get_filename(url)
    location = get_download_location()
    chunk = 1
    chunk_size=1024
    num_bars = int(file_size / chunk_size)
    if verbose:
        print(dict(file_size=file_size))
        print(dict(num_bars=num_bars))

    with open(location + file_name , 'wb') as fp:
        for chunk in tqdm.tqdm(
                                    r.iter_content(chunk_size=chunk_size)
                                    , total= num_bars
                                    , unit = 'KB'
                                    , desc = file_name
                                    , leave = True # progressbar stays
                                ):
            fp.write(chunk)
    print("File has been successfully Downloaded at " + location)
    return

def main():
	try:
		url = input("Paste URL: ")
		#For Header
		h = requests.head(url, allow_redirects=True) 
		header = h.headers

		if is_downloadable(header,url):
			prompt = input("Do want to download this file? Enter y/n only: ")
			if prompt == "y":
				download_file(url)
			else:
				print("Thank you, Program closed")
		else:
			print()
			print("*****************************************************************************************************".center(center_point))
			print("I am unable to find a file in this url, Enter Another URL".center(center_point))
			print("*****************************************************************************************************".center(center_point))
			main()
	#except Exception as e: print(e)

	except:
		print("Program Exit")
main()
