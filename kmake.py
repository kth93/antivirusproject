import sys
import zlib
import hashlib
import os
from argparse import ArgumentParser

def DecodeKMD(fname):
    if fname.split('.')[-1] != 'kmd':
        print("input file is not vaild")
        return
    fp = open(fname, 'rb')
    buf = fp.read()

    fp.close()

    buf2 = buf[:-32]
    fmd5 = buf[-32:]

    f = buf2

    for i in range(3):
        md5 = hashlib.md5()
        md5.update(f)
        f = bytes(md5.hexdigest(), encoding='utf-8')

    if f != fmd5:
        raise SystemError

    buf3 = b''
    for c in buf[4:]:
        buf3 += bytes([c ^ 0xFF])

    buf4 = zlib.decompress(buf3)

    db_name = fname.split('.')[-2] + '.db'

    fp = open(db_name, 'wb')
    fp.write(buf4)
    fp.close()
    print("{} -> {}".format(fname, db_name))

def EncryptKMD(fname) :
    if fname.split('.')[-1] != 'db':
        print("input file is not vaild")
        return
    fp = open(fname, 'rb')
    buf = fp.read()
    fp.close()

    buf2 = zlib.compress(buf)

    buf3 = b''
    for c in buf2:
        buf3 += bytes([c ^ 0xFF])

    buf4 = b'KAVM' + buf3

    f = buf4
    for i in range(3):
        md5 = hashlib.md5()
        md5.update(f)
        f = bytes(md5.hexdigest(), encoding='utf-8')
    
    buf4 += f

    kmd_name = fname.split('.')[0] + '.kmd'
    fp = open(kmd_name, 'wb')
    fp.write(buf4)
    fp.close()

    print("{} -> {}".format(fname, kmd_name))

def main():
    parser = ArgumentParser(description='db encrypt & decrypt tool')
    parser.add_argument('filenames', nargs='?', help='Files to encrypt or decrypt')
    parser.add_argument('--decrypt', '-d', action='store_true', help='decrpyt .kmd file to .db file')
    args = parser.parse_args()

    fname = args.filenames
    fname = fname.replace('.\\', '')
    if args.decrypt:
        DecodeKMD(fname)
    else:
        EncryptKMD(fname)

if __name__ == "__main__":
    main()