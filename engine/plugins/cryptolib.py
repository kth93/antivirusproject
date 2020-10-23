import hashlib

def md5(data):
    return hashlib.md5(data).hexdigest()

class KavMain:
    def init(self, plugins_path):
        return 0
    
    def uninit(self):
        return 0

    def getinfo(self):
        info = dict()

        info['author'] = 'kth93'
        info['version'] = '1.0'
        info['title'] = 'Crypto Library'
        info['kmd_name'] = 'cryptolib'

        return info