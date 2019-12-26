import zipfile
import tempfile
import os

file_dir = r'C:\Users\liang\Desktop\dkango\users\1.zip'
d = zipfile.ZipFile(file_dir)
m = "spider"

import hashlib

secret = hashlib.sha256()
secret.update(m.encode())
h = secret.hexdigest()
print(h)

# m = \
# """import sys
# """
# tmpfd, tmpname = tempfile.mkstemp(dir=os.path.dirname(file_dir))
#
# os.close(tmpfd)
#
# with zipfile.ZipFile(file_dir, 'r') as zin:
#     with zipfile.ZipFile(tmpname, 'w') as zout:
#
#         for item in zin.infolist():
#
#             if item.filename != "delete/new/__init__.py":
#                 zout.writestr(item, zin.read(item.filename))
#
# os.remove(file_dir)
#
# os.rename(tmpname, file_dir)
#
# with zipfile.ZipFile(file_dir, mode='a', compression=zipfile.ZIP_DEFLATED) as zf:
#     zf.writestr("delete/new/__init__.py", m.encode())































