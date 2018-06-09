import os
import sys

token = 'wustor'
srcDir = '.'


if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
    projectDir = sys.argv[1]
else:
    print('Project directory parameter missing, using current location.')

for f in os.listdir(srcDir):
    if f.endswith("_protected.apk") and token in f:
        name = os.path.splitext(f)[0]
        inputApk = os.path.join(srcDir, f)
        outputApk = os.path.join(srcDir, name + "_aligned.apk")
        if os.path.exists(outputApk):
            os.remove(outputApk)
        print("Aligning apk [%s] with name[%s]:" % (inputApk, name))
        os.system("$ANDROID_HOME/build-tools/26.0.2/zipalign -v 4 " + inputApk + " " + outputApk)
