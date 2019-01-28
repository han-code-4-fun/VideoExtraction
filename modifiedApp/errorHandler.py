


def writeErrorLog(thisvid):
    with open('errorStrangeFile.txt',mode='a+',encoding='utf-8') as errStra:
            errStra.write('vid: \r\n')
            errStra.write('   ')
            errStra.write(thisvid + "advertisement")
            errStra.write('\r\n')