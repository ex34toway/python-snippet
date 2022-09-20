import os
import subprocess


for d in os.listdir('/server/contrib'):
    if os.path.isdir(d):
        process = subprocess.Popen(["git", "stash"], stdout=subprocess.PIPE, cwd=d)
        output = process.communicate()[0]

        