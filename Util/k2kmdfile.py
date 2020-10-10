import hashlib
import os
import py_compile
import random
import shutil
import struct
import sys
import zlib
import k2rc4
import k2rsa
import k2timelib

def make(src_fname, debug=False):
    fname = src_fname

    if fname.split('.')[-1] == 'py':
        py_compile.compile(fname)
        pyc_name = fname + 'c'
    else:
        pyc_name = fname.split('.')[0] + '.pyc'
        shutil.copy(fname, pyc_name)
    
    rsa_pu = k2rsa.read_key('key.pkr') # public key

    rsa_pr = k2rsa.read_key('key.skr') # private key

    if not (rsa_pr and rsa_pu):
        if debug:
            print('Error: Cannot find the key files.')
        return False
    
    # Header
    kmd_data = 'KAVM'

    ret_date = k2timelib.get_now_date()
    ret_time = k2timelib.get_now_time()

    val_date = struct.pack('<H', ret_date)
    val_time = struct.pack('<H', ret_time)

    reserved_buf = val_date + val_time + (chr(0) * 28)

    kmd_data += reserved_buf

    random.seed()

    # Body
    while 1:
        tmp_kmd_data = ''

        key = '' # RC4 algorithm

        for i in range(16):
            key += chr(random.randint(0, 0xff))

        e_key = k2rsa.crypt(key, rsa_pr) # RC4 key encrypt using prviate key

        if len(e_key) != 32:
            print('key encrypt error')
            return False

        d_key = k2rsa.crypt(e_key, rsa_pu)

        # validate key
        if key == d_key and len(key) == len(d_key):
            tmp_kmd_data += e_key

            buf1 = open(pyc_name, 'rb').read()
            buf2 = zlib.compress(buf1)

            e_rc4 = k2rc4.RC4()
            e_rc4.set_key(key)

            buf3 = e_rc4.crypt(buf2) # encrypt image using RC4 algorithm

            e_rc4 = k2rc4.RC4()
            e_rc4.set_key(key)

            if e_rc4.crypt(buf3) != buf2:
                print('image encrypt error')
                return False

            tmp_kmd_data += buf3

            # trailer
            md5 = hashlib.md5()
            md5hash = kmd_data + tmp_kmd_data

            # f = bytes(md5.hexdigest(), encoding='utf-8')
            for i in range(3):
                md5.update(md5hash)
                md5hash = md5.hexdigest()
            
            m = md5hash.decode('hex')

            e_md5 = k2rsa.crypt(m, rsa_pr) # encrypt md5 using private key
            if len(e_md5) != 32:
                print('e_md5 encrypt error')
                return False

            d_md5 = k2rsa.crypt(e_md5, rsa_pu) # decrypt encrypted md5 using public key

            if m == d_md5:
                kmd_data += tmp_kmd_data + e_md5
                break
            else:
                print('d_md5 decrypt error')
                return False
            
    # make KMD file
    ext = fname.find('.')
    kmd_name = fname[0:ext] + '.kmd'

    try:
        if kmd_data:
            open(kmd_name, 'wb').write(kmd_data)
            os.remove(pyc_name)

            if debug:
                print('Success: {0:-13s} -> {1:s}'.format(fname, kmd_name))
            return True
        else:
            raise IOError

    except IOError:
        if debug:
            print('Fail: {}'.format(fname))
        return False