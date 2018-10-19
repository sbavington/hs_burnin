import time

def logError(lognum, server, message):
    f = open ('burnin.log', 'a')
    logMessage = ('{}\t{}\t{}\t{}\n'.format(lognum,server,time.time(),message))
    f.write(logMessage)


if __name__ == '__main__':
    logError(241,'10.0.2.2','Test Message')