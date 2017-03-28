#!/usr/local/bin/python
'''
This program creates a thumbnail view of the given pdf
the dependencies for this program to work are:
- ImageMagick installed in the hosting system (this does the magic(k) o.O?)
- PIL (ofc)
'''
import os
import re
import sys
import time
from PIL import Image
from subprocess import call

def get_sorted_thumbs_path(base_path, thumb_placeholder):
	'''Gets the list of files that follow the placeholder convention'''
	placeholder = thumb_placeholder.split('.')
	regex_filter = '%s-[0-9]+.%s'%(placeholder[0], placeholder[1])
	img_files = [f for f in os.listdir(base_path) if re.match(regex_filter, f)]
	return sorted(img_files)

def cleanup_workspace(ws_path, placeholder):
	'''Removes any previous thumbs generated in the folder'''
	thumb_paths = get_sorted_thumbs_path(ws_path, placeholder)
	map(os.remove, thumb_paths)

def convert_pdf_to_thumb(pdf_path, thumb_path, num_pages=None, bg_color=None):
	placeholder = 'page_thumb.png'

	# Nice and clean, to avoid merging files from previous calls
	cleanup_workspace('.', placeholder)

	# Extract thumbs
	call(['convert', '%s[0-%d]' % (pdf_path, num_pages-1), '-thumbnail', 'x156', placeholder])

	bg_arg = ' '
	if bg_color is not None:
		bg_arg = "-background '%s' " % bg_color
	ph_split = placeholder.split('.')
	montage_ph = '%s-*.%s'%(ph_split[0], ph_split[1])
	montage_cmd = "montage%s-mode concatenate -quality 100 -tile x1 %s %s" % (bg_arg, montage_ph, thumb_path)
	os.system(montage_cmd)

	# Clean up the generated thumbs
	cleanup_workspace('.', placeholder)


if __name__=='__main__':
	if len(sys.argv) < 3:
		print '''
		Usage: pdf2Thumb.py <pdf_path> <thumb_path> <num_pages> <bg_color>
			pdf_path: 		path to the pdf file to be converted
			thumb_path: 	path where the thumb will be saved

			Optional params:
			num_pages: 		number of pages to be shown in the thumbnail
			bg_color: 		background color must be in hex format #rrggbb

		Example:
			pdf2Thumb.py report.pdf report.png 7 #FFFFFF
		'''

	# Compulsory params
	pdf_path = sys.argv[1]
	thumb_path = sys.argv[2]

	# optional params
	num_pages = 0
	if len(sys.argv) > 3:
		num_pages = int(sys.argv[3])

	convert_pdf_to_thumb(pdf_path, thumb_path, num_pages)
	