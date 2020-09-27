import sys
import os
import hashlib
import zlib
import StringIO
import scanmod
import curemod

VirusDB = []
vdb = []
vsize = []
sdb = []

def DecodeKMD(fname):
    try:
        fp = open(fname, 'rb')
        buf = fp.read()
        fp.close()

        buf2 = buf[:-32]
        fmd5 = buf[-32:]

        f = buf2
        for i in range(3):
            md5 = hashlib.md5()
            md5.update(f)
            f = md5.hexdigest()

        if f != fmd5:
            raise SystemError
        
        buf3 = ''
        for c in buf[4:]:
            buf3 += chr(ord(c) ^ 0xFF)
        
        buf4 = zlib.decompress(buf3)
        return buf4
    except:
        pass

    return None

def LoadVirusDB():
    buf = DecodeKMD('virus.kmd')
    fp = StringIO.StringIO(buf)

    while True:
        line = fp.readline()
        if not line : break

        line = line.strip()
        VirusDB.append(line)

    fp.close()

def MakeVirusDB():
    for pattern in VirusDB:
        t = []
        v = pattern.split(':')

        scan_func = v[0] # Malware Scan function
        # cure_func = v[1] # Malware Cure function

        if scan_func == 'ScanMD5':
            t.append(v[3]) # store MD5 hash
            t.append(v[4]) # store Malware's name
            vdb.append(t)

            size = int(v[2])
            if vsize.count(size) == 0:
                vsize.append(size)
        
        elif scan_func == 'ScanStr':
            t.append(int(v[2])) # store Malware scan string's offset
            t.append(v[3]) # store scan string
            t.append(v[4]) # store Malware's name
            sdb.append(t)
        

def SearchVDB(fmd5):
    for t in vdb:
        if t[0] == fmd5:
            return True, t[1]

    return False, ''

if __name__ == '__main__':
    LoadVirusDB()
    MakeVirusDB()

    if len(sys.argv) != 2:
        print('Usage : antivirus.py [file]')
        exit()

    fname = sys.argv[1]

    ret, vname = scanmod.ScanVirus(vdb, vsize, sdb, fname)

    if ret == True:
        print("{} : {}".format(fname, vname))
        curemod.CureDelete(fname)
    else:
        print("{} : ok".format(fname))