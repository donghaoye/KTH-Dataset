import os
import sys
import subprocess
import shutil


data_path = '/data/donghaoye/KTH'
# # sequences_list = ''
# video_files=os.listdir(data_path + '/data/videos/')
# video_files.sort()
#
# # extract frames from video clips
# args=['ffmpeg', '-i']
# for video in video_files:
# 	print(video)
# 	video_name = video[:-11]	# remove '_uncomp.avi' from name
# 	print('video name is: ', video_name)
# 	frame_name = 'frame_%d.jpg'	# count starts from 1 by default
# 	os.makedirs(data_path + '/data/frames/'+video_name)
# 	args.append(data_path + '/data/videos/'+video)
# 	args.append(data_path + '/data/frames/'+video_name+'/'+frame_name)
# 	ffmpeg_call = ' '.join(args)
# 	print(ffmpeg_call)
# 	print(args)
# 	subprocess.call(ffmpeg_call, shell=True)		# execute the system call
# 	args=['ffmpeg', '-i']
# 	if (video_files.index(video) + 1) % 50 == 0:
# 		print('Completed till video : ', (video_files.index(video) + 1))
#
#
# print('[MESSAGE]	Frames extracted from all videos')


train_path = data_path + '/data/' + 'TRAIN'
valid_path = data_path + '/data/' + 'VALIDATION'
test_path = data_path + '/data/' + 'TEST'
if os.path.exists(train_path):
	shutil.rmtree(train_path)
if os.path.exists(valid_path):
	shutil.rmtree(valid_path)
if os.path.exists(test_path):
	shutil.rmtree(test_path)
os.makedirs(train_path)
os.makedirs(valid_path)
os.makedirs(test_path)

train = [11, 12, 13, 14, 15, 16, 17, 18]
validation =[19, 20, 21, 23, 24, 25, 1, 4]
test = [22, 2, 3, 5, 6, 7, 8, 9, 10]

# read file line by line and strip new lines
lines = [line.rstrip('\n').rstrip('\r') for line in open('sequences_list.txt')]
# remove blank entries i.e. empty lines
lines = filter(None, lines)
# split by tabs and remove blank entries
lines = [filter(None, line.split('\t')) for line in lines]
lines.sort()
# print(lines)

success_count = 0
error_count = 0
seq_path = ''
for line in lines:
	vid = line[0].strip(' ').replace(' ', '')
	if vid.find('jogging') != -1 or vid.find('handclapping') != -1 or vid.find('boxing') != -1:
		continue
	subsequences = line[-1].split(',')[1:]
	print(line)
	print(vid)
	print(subsequences)

	person = int(vid[6:8])
	if person in train:
		move_to = 'TRAIN'
		print("Tain!!!!!!!")
	elif person in validation:
		move_to = 'VALIDATION'
		print("V!!!!!!!")
	else:
		move_to = 'TEST'
		print("test!!!!!!!")
	for seq in subsequences:
		try:
			limits=seq.strip(' ').split('-')
			seq_path=data_path + '/data/' + move_to + '/' + vid + '_frame_' + limits[0] + '_' + limits[1]
			os.makedirs(seq_path)
		except:
			print('-----------------------------------------------------------')
			print('[ERROR MESSAGE]: ')
			print('limits : ', limits)
			print('seq_path : ', seq_path)
			print('-----------------------------------------------------------')
			continue
		error_flag=False
		for i in xrange(int(limits[0]), int(limits[1])+1):
			src = data_path + '/data' + '/frames/' + vid + '/frame_' + str(i) + '.jpg'
			dst = seq_path
			print(dst + "!!!")
			print(i, src, limits)
			try:
				shutil.copy(src, dst)
			except:
				error_flag = True
		if error_flag:
			print("[ERROR]: ", seq_path)
			error_count+=1

	if (lines.index(line) + 1) % 50 == 0:
		print('Completed till video : ', (lines.index(line) + 1))
	success_count+=1

print('[ALERT]		Total error count is : ', error_count)
print('[MESSAGE]	Data split into train, validation and test')