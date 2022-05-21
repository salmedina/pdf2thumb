#!/usr/bin/env python3
'''
This program creates a thumbnail view of the given pdf
the dependencies for this program to work are:
- ImageMagick installed in the hosting system (this does the magic(k) o.O?)
- PIL (ofc)
'''
import argparse
import os
import re
import sys
import time
from subprocess import call
from pathlib import Path
from PIL import Image, ImageOps


def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--input_path', type=Path,
						help='Path to the pdf file')
	parser.add_argument('-o', '--output_path', type=Path,
						help='Path of the output image with the thumbnails')
	parser.add_argument('-n', '--num_pages', type=int, default=None,
						help='Number of pages to be rendered')

	return parser.parse_args()


def get_sorted_thumbs_path(thumbs_dir, ext='.png'):
	'''Gets the list of files that follow the placeholder convention'''
	thumb_path_list = list(Path(thumbs_dir).glob(f'*{ext}'))
	sorted_path_list = sorted(thumb_path_list, key=lambda x: int(str(x.stem).split('-')[1]))
	
	return sorted_path_list


def cleanup_workspace(ws_path, placeholder):
	'''Removes any previous thumbs generated in the folder'''
	thumb_paths = get_sorted_thumbs_path(ws_path, placeholder)
	map(os.remove, thumb_paths)


def convert_pdf_to_thumb(pdf_path, thumb_path, num_pages=None, bg_color=None):
	thumbs_dir = 'thumbs/'
	placeholder = 'thumbs/page-%02d.png'

	# Remove the files in the thumb dir
	for thumb_path in Path(thumbs_dir).glob('*.png'):
		os.remove(thumb_path)

	# Extract thumbs
	# check if all pages are to be extracted or just some
	pages_arg = '%s' % (pdf_path) if num_pages is None else '%s[0-%d]' % (pdf_path, num_pages-1)
	call(['convert', pages_arg, '-thumbnail', 'x156', placeholder])

	thumb_path_list = get_sorted_thumbs_path(thumbs_dir, '.png')
	thumb_img_list = [Image.open(p) for p in thumb_path_list]
	
	num_pages = len(thumb_path_list)
	wp, hp = thumb_img_list[0].size
	print(f'Page- w: {wp}   h: {hp}')

	# New image
	wi = int(wp + (num_pages - 1) * (2/3 * wp))
	hi = int(1.5 * hp)
	print(f'Image - w: {wi}   h: {hi}')
	output_img = Image.new('RGBA', (wi, hi), (255, 255, 255, 0))

	cur_x = wi - wp
	for idx in range(num_pages):
		cur_img = thumb_img_list[num_pages-1-idx]
		cur_page = num_pages - idx
		cur_y = 0 if cur_page % 2 != 0 else int(0.5 * hp)
		output_img.paste(cur_img, (cur_x, cur_y))
		cur_x -= int(2/3 * wp)

	# Save output image
	output_img.save('output.png', 'PNG')

	# Remove the files in the thumb dir
	for thumb_path in Path(thumbs_dir).glob('*.PNG'):
		os.remove(thumb_path)


if __name__=='__main__':
	args = parse_args()

	convert_pdf_to_thumb(args.input_path,
						 args.output_path,
						 args.num_pages)
	
