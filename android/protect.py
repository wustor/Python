import hashlib
import hmac
import os
import requests
import time
import logging
import sys

logging.basicConfig(stream=sys.stdout,
                    format='%(message)s', level=logging.INFO)

baseUrl = 'https://usc.an110.com/webbox/v5'
key = os.environ['BANGBANG_API_KEY']
secret = os.environ['BANGBANG_API_SECRET']
artifact = 'package.zip'
headers = {'api_key': key}
projectDir = '.'


def gen_hash(param):
    logging.info('Generating signature')
    string = ''
    for k, v in sorted(param.items()):
        string += str(v)

    return hmac.new(secret, string, hashlib.sha1).hexdigest()


if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
    projectDir = sys.argv[1]
else:
    logging.info('Project directory parameter missing, using current location.')

logging.info('==================================')
logging.info(' Uploading file')
logging.info('==================================')
params = {'api_key': key, 'username': 'mobike',
          'policy_id': 2630, 'upload_type': 2}

headers['sign'] = gen_hash(params)
del params['api_key']
# logging.info(hmac.new('456', '123test123456', hashlib.sha1).hexdigest())

logging.info('Sending file')
for root, dirs, files in os.walk(os.path.join(projectDir, 'app/build/outputs/apk')):
    for f in files:
        if f.endswith('.apk'):
            path = os.path.join(root, f)
            segments = os.path.splitext(f)
            artifact = segments[0] + '_protected' + segments[1]
            logging.info('Dealing with apk [%s]' % f)
            r = requests.post(baseUrl + '/protect/upload', headers=headers,
                              params=params, files={'apk_file': (f, open(path, 'rb'))}, timeout=20)

            logging.info('--- Response ---')
            logging.info(r.text.encode('utf-8'))
            logging.info('---\n')

            res = r.json()
            if r.status_code == 200 and res['code'] == 0 and 'id' in res['info']:
                apkid = res['info']['id']
                logging.info('Uploaded, Apk id = [%d]' % apkid)
            else:
                logging.info('Error when uplod')
                sys.exit(1)
            break  # only upload one apk
    else:
        continue
    break

logging.info('==\n')

logging.info('==================================')
logging.info(' Checking status')
logging.info('==================================')
params = {'api_key': key, 'username': 'mobike', 'apkinfo_id': apkid}

headers['sign'] = gen_hash(params)
headers['Connection'] = 'close'
del params['api_key']

status = -1
cnt = 0
while True:
    cnt += 1
    logging.info('Check seq #%d' % cnt)
    r = requests.post(baseUrl + '/protect/get_state',
                      headers=headers, params=params)

    logging.info('--- Response ---')
    logging.info(r.text.encode('utf-8'))
    logging.info('---')

    res = r.json()
    if r.status_code == 200 and res['code'] == 0 and res['info']['status_code'] == 9009:
        logging.info('Apk file ready.\n')
        break
    else:
        logging.info('Protection unfinished.\n')
    time.sleep(16)

del headers['Connection']
logging.info('==\n')

logging.info('==================================')
logging.info(' Downloading zip')
logging.info('==================================')
params = {'api_key': key, 'username': 'mobike',
          'apkinfo_id': apkid, 'download_type': 1}

headers['sign'] = gen_hash(params)
del params['api_key']

logging.info('Downloading: %s ' % artifact)
r = requests.post(baseUrl + '/protect/download',
                  headers=headers, params=params, stream=True)

f = open(artifact, 'wb')
size = 0
cnt = 0

for chunk in r.iter_content(chunk_size=4096):
    if chunk:  # filter out keep-alive new chunks
        cnt += 1
        size += len(chunk)
        f.write(chunk)
        if size < 1 << 10:
            logging.info('%10d Bytes downloaded.' % size)
        elif size < 1 << 20:
            if cnt % 16 == 0:
                logging.info('%3.2f KB downloaded.' % (size / 1000.))
        else:
            if cnt % 256 == 0:
                logging.info('%3.2f MB downloaded.' % (size / 1000000.))

logging.info('Download finished with %3.2f MB.' % (size / 1000000.))
f.close()
logging.info('==\n')
