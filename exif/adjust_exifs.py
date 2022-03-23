"""A script for correcting EXIF data on a folder of JPGs
   ONLY RUN THIS ONCE PER BATCH OF IMAGES"""

from datetime import datetime, timedelta
from glob import glob
from exif import Image

count = 0
missing = 0

# timedelta for adjusting incorrect camera time
# make sure to change this in the future if needed
adj_time = timedelta(hours=2, minutes=-2, seconds=-14)

start_time = datetime.now()

# loop over every file in folder using glob
# change pathname in the future if needed
for filename in glob(pathname='./pics/*.JPG'):
	count += 1

	# open file as 'read binary'
	with open(filename, 'rb') as read_file:
		# create exif Image from file
		img = Image(read_file)

	# check if image is missing EXIF info
	if not img.has_exif:
		print(f'{filename} missing EXIF')
		missing += 1

	else:
		# parse image datetime. ex: '2021:10:12 10:23:49'
		pic_datetime = datetime.strptime(img.datetime, '%Y:%m:%d %H:%M:%S')

		# adjust image datetime
		pic_datetime = pic_datetime + adj_time
		datetime_str = pic_datetime.strftime('%Y:%m:%d %H:%M:%S')
		#print(f'[{filename}]\noriginal: \'{img.datetime}\'\ncorrected: \'{datetime_str}\'\n\n')

		# reassign image datetime
		img.datetime = datetime_str
		# img.datetime_digitized doesn't seem to be different from img.datetime
		img.datetime_digitized = datetime_str
		# reassign original as well in case Google Photos uses that
		img.datetime_original = datetime_str

		# reassign UTC offsets
		img.offset_time = '-07:00'
		img.offset_time_digitized = '-07:00'
		img.offset_time_original = '-07:00'

		# current time in ISO format
		now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f-0700')
		# add user comment and copyright to image
		img.user_comment = f'Image time corrected by (+{adj_time}) on {now}'
		img.copyright = '2021 Drue Gilbert'

		# re-open file as 'write binary'
		with open(filename, 'wb') as write_file:
			# save file with updated EXIF
			write_file.write(img.get_file())

end_time = datetime.now()
print(f'{count} files. {missing} missing EXIF.')
print(f'elapsed time: {end_time - start_time}')

