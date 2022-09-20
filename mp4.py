import glob

from shutil import copy

mypath = '/'

if __name__ == '__main__':
    for p in glob.glob("/root/youtube_channel_archiver/tmp/*.txt"):
        if p.find("吴昊"):
            copy(p, "/root/youtube_channel_archiver/tmp/mp4")
