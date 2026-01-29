import os

try:
    f = open("file.txt")
    data = f.read()
except:
    print("oops")

print("done")
