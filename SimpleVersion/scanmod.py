import os
import hashlib

def SearchVDB(vdb, fmd5):
    for t in vdb:
        if t[0] == fmd5:
            return True, t[1]

    return False, ''

def ScanMD5(vdb, vsize, fname):
    ret = False
    vname = ''

    if not os.path.isfile(fname):
        return ret, 'NotExistFile'

    size = os.path.getsize(fname)

    if vsize.count(size):
        fp = open(fname, 'rb')
        buf = fp.read()
        fp.close()

        m = hashlib.md5()
        m.update(buf)
        fmd5 = m.hexdigest()

        ret, vname = SearchVDB(vdb, fmd5)

    return ret, vname

def ScanStr(fp, offset, mal_str):
    size = len(mal_str)

    fp.seek(offset)
    buf = fp.read(size)

    if buf == mal_str:
        return True
    else:
        return False

def ScanVirus(vdb, vsize, sdb, fname):
    # scan malware using MD5 hash
    ret, vname = ScanMD5(vdb, vsize, fname)
    if ret == True:
        print('ScanMD5')
        return ret, vname

    if vname == 'NotExistFile':
        return ret, vname

    # scan malware using offset search
    fp = open(fname, 'rb')
    for t in sdb:
        if ScanStr(fp, t[0], t[1]) == True:
            print('ScanStr')
            ret = True
            vname = t[2]
            break
    fp.close()

    return ret, vname