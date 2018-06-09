import os
import logging
import sys

logging.basicConfig(stream=sys.stdout,
                    format='%(message)s', level=logging.INFO)

channelFile = "channels.txt"
srcDir = "."

logging.info('==================================')
logging.info(' Extracting channels')
logging.info('==================================')
m = {}
with open(channelFile, encoding="utf-8") as f:
    for line in f:
        segments = line.split()
        if len(segments) == 3:
            logging.info("Get channel: %s and key: %s" % (segments[2], segments[1]))
            m[segments[1]] = segments[2]

logging.info("Total count: %s" % len(m))
logging.info("=\n")

logging.info('==================================')
logging.info(' Renaming packages')
logging.info('==================================')
cnt = 0
for filename in os.listdir(srcDir):
    if filename.endswith("_signed.apk") and 'wustor' in filename:
        for key, value in m.items():
            if filename.startswith(key):
                i = filename.index("_protected")
                name = filename[len(key) + 1:i] + '_' + value + filename[i:]
                logging.info("Rename origin [%s] with new name [%s]" % (filename, name))
                if os.path.exists(name):
                    os.remove(name)
                os.rename(filename, name)
                cnt += 1
                break

logging.info("Total renamed: %d apk(s)" % cnt)
