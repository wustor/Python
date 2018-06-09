import os
import sys

keyFile = "./app/key/mobike.keystore"
token = "wustor"
srcDir = "."

if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
    srcDir = sys.argv[1]
else:
    print('Project directory parameter missing, using current location.')

for f in os.listdir(srcDir):
    if f.endswith("_aligned.apk") and token in f:
        name = os.path.splitext(f)[0]
        inputApk = os.path.join(srcDir, f)
        outputApk = os.path.join(srcDir, name + "_signed.apk")
        if os.path.exists(outputApk):
            os.remove(outputApk)
        print("Signing apk [%s] with name[%s]:" % (inputApk, name))
        os.system("$ANDROID_HOME/build-tools/26.0.2/apksigner sign -ks " + keyFile + " --ks-key-alias mobike --ks-pass pass:mobike123 --out " + outputApk + " " + inputApk)
