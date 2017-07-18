import os
import sys
import subprocess
import shutil


data_path = '/data/donghaoye/KTH'
# sequences_list = ''
video_files=os.listdir(data_path + '/data/videos/')
video_files.sort()

# extract frames from video clips
args=['ffmpeg', '-i']
for video in video_files:
    print(video)
    video_name = video[:-11]	                    # remove '_uncomp.avi' from name
    frame_dir = data_path + '/data/frames/' + video_name
    if os.path.exists(frame_dir):
        shutil.rmtree(frame_dir)
    else:
        os.makedirs(frame_dir)

    frame_name = 'frame_%d.jpg'                     # count starts from 1 by default
    args.append(data_path + '/data/videos/'+video)
    args.append("-s hd720")
    args.append(data_path + '/data/frames/'+video_name+'/'+frame_name)
    ffmpeg_call = ' '.join(args)
    print(ffmpeg_call)
    print(args)
    subprocess.call(ffmpeg_call, shell=True)		# execute the system call
    args=['ffmpeg', '-i']
    if (video_files.index(video) + 1) % 50 == 0:
		print('Completed till video : ', (video_files.index(video) + 1))


print('[MESSAGE]	Frames extracted from all videos')