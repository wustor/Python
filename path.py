import os

absolutePath = 'F:\Python'

print("===========abs===============")
for abs in os.listdir(absolutePath):
    print(abs)
relativePath = './'
print("===========rel===============")
for rel in os.listdir(relativePath):
    print(rel)

print("===========walk===============")
path = os.listdir("./")
for root, dirs, files in os.walk('./android'):
    print(root)
    print(dirs)
    print(files)
