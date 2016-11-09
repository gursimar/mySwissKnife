import ffmpy
import subprocess
import glob, os
from pydub import AudioSegment

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
    folder = 'data/bhanuvideos'
    os.chdir(folder)
    for file in glob.glob("*.webm"):
        print(file)
        convertUsingFFmpeg(file)
        convertUsingSox(file + '.flac')
        flac_file = AudioSegment.from_file(file + '.flac.flac', "flac")
        th = 58000 # 58 s
        if len(flac_file) > th:
            first_file = flac_file[:51000]
            second_file = flac_file[50000:]
            first_file.export(file + '.flac1.flac', 'flac')
            second_file.export(file + '.flac2.flac', 'flac')
        pass
    #for file in glob.glob("*.flac"):
    #    print(file)
    #    convertUsingSox(file)