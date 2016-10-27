import ffmpy
import subprocess
import glob, os

def convertUsingFfmpy():
     ff = ffmpy.FFmpeg(
          inputs={'foo.webm': None},
          outputs={'foo.avi': None}
     )
     ff.run()


def convertUsingFFmpeg(filename, cmd=None):
    # cmd = "ffmpeg -i C:/test.mp4 -ab 160k -ac 2 -ar 44100 -vn audio.wav"
    # cmd = "ffmpeg -i foo.webm -vn -acodec copy output.oga"
    # cmd = "ffmpeg -i " + filename + " -vn -acodec copy " + filename + ".oga"
    cmd = "ffmpeg -i " + filename + " " + filename + ".flac"
    print cmd
    subprocess.call(cmd, shell=True)


def convertUsingSox(filename, cmd=None):
    # cmd = "ffmpeg -i C:/test.mp4 -ab 160k -ac 2 -ar 44100 -vn audio.wav"
    # cmd = "ffmpeg -i foo.webm -vn -acodec copy output.oga"
    # cmd = "ffmpeg -i " + filename + " -vn -acodec copy " + filename + ".oga"
    cmd = "sox " + filename + " --channels=1 --bits=16 --rate=16000 --endian=little " + filename + ".flac"
    print cmd
    subprocess.call(cmd, shell=True)


if __name__ == '__main__':
    folder = 'data/videos'
    os.chdir(folder)
    for file in glob.glob("*.webm"):
        print(file)
        convertUsingFFmpeg(file)
        convertUsingSox(file + '.flac')
    #for file in glob.glob("*.flac"):
    #    print(file)
    #    convertUsingSox(file)