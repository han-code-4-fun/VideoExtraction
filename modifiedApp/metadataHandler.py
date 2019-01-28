import subprocess


#use ffmpeg to get the metadata of downloaded file
def getMETADATA(inputFile):
    command = ['ffprobe', '-show_format', inputFile]
    temp3 = subprocess.run(command, shell=True, capture_output=True).stdout.decode('utf-8')
    vidPos = temp3.find('vid:') + 4
    endPos = temp3.find('\r\n', vidPos)
    vidOutput = temp3[vidPos:endPos]
    return vidOutput
