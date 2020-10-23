import os

class KavMain:
    def init(self, plugins_path):
        self.virus_name = 'Dummy-Test-File (not a virus)'
        self.dummy_pattern = 'Dummy Engine test file - KICOM Anti-Virus Project'
        return 0

    def uninit(self):
        del self.virus_name
        del self.dummy_pattern

        return 0

    def scan(self, filehandle, filename):
        try:
            fp = open(filename)
            buf = fp.read(len(self.dummy_pattern))
            fp.close()

            if buf == self.dummy_pattern:
                return True, self.virus_name, 0 # result, virus_name, virus_ID
        except:
            pass

        return False, '', -1
    
    def disinfect(self, filename, malware_id):
        try:
            if malware_id == 0:
                os.remove(filename)
                return True
        except IOError:
            pass

        return False
    
    def listvirus(self):
        vlist = list()

        vlist.append(self.virus_name)

        return vlist

    def getinfo(self):
        info = dict()

        info['author'] = 'kth93'
        info['version'] = '1.0'
        info['title'] = 'Dummy Scan Engine'
        info['kmd_name'] = 'dummy'

        return info
