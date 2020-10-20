import os
import io
import datetime

import k2kmdfile
import k2rsa

class Engine:
    def __init__(self, debug=False):
        self.debug = debug

        self.plugins_path = None
        self.kmdfiles = []  # priority
        self.kmd_modules = [] # loaded module

        self.max_datetime = datetime.datetime(1980, 1, 1, 0, 0, 0, 0)

    def set_plugins(self, plugins_path):
        self.plugins_path = plugins_path

        pu = k2rsa.read_key(plugins_path + os.sep + 'key.pkr')

        if not pu:
            return False
        
        ret = self.__get_kmd_list(plugins_path + os.sep + 'kicom.kmd', pu)

        if not ret:
            return False
        
        if self.debug:
            print('[*] kicom.kmd :')
            print('   ', self.kmdfiles)
        
        for kmd_name in self.kmdfiles:
            kmd_path = plugins_path + os.sep + kmd_name
            k = k2kmdfile.KMD(kmd_path, pu)
            module = k2kmdfile.load(kmd_name.split('.')[0], k.body)

            if module:
                self.kmd_modules.append(module)
                self.__get_last_kmd_build_time(k)
            else:
                print(kmd_name, "is failed to load on memory")

        if self.debug:
            print('[*] kmd_moudles :')
            print('    ', self.kmd_modules)
            print('[*] Last updated %s UTC' % (self.max_datetime.ctime()))

        return True

    def create_instance(self):
        ei = EngineInstance(self.plugins_path, self.max_datetime, self.debug)
        if ei.create(self.kmd_modules):
            return ei
        else:
            return None

    def __get_last_kmd_build_time(self, kmd_info):
        d_y, d_m, d_d = kmd_info.date
        t_h, t_m, t_s = kmd_info.time
        t_datetime = datetime.datetime(d_y, d_m, d_d, t_h, t_m, t_s)

        if self.max_datetime < t_datetime:
            self.max_datetime = t_datetime

    def __get_kmd_list(self, kicom_kmd_file, pu):
        kmdfiles = []

        k = k2kmdfile.KMD(kicom_kmd_file, pu)

        if k.body:
            msg = io.StringIO(k.body.decode()) # byte to string

            while True:
                line = msg.readline().strip()

                if not line:
                    break
                elif line.find('.kmd') != -1:
                    kmdfiles.append(line)
                else:
                    continue
           
        if len(kmdfiles):
            self.kmdfiles = kmdfiles
            return True
        else:
            return False

class EngineInstance:
    def __init__(self, plugins_path, max_datetime, debug=False):
        self.debug = debug

        self.plugins_path = plugins_path
        self.max_datetime = max_datetime

        self.kavmain_inst = [] # plugins's KavMain Instance

    def init(self):
        t_kavmain_inst = [] # the final instance list

        if self.debug:
            print('[*] KavMain.init() :')

        for inst in self.kavmain_inst:
            try:
                ret = inst.init(self.plugins_path) # call plugin engine's init function
                if not ret:
                    t_kavmain_inst.append(inst)

                    if self.debug:
                        print('[-] %s.init() : %d' % (inst.__module__, ret))
            except AttributeError:
                continue

        self.kavmain_inst = t_kavmain_inst

        if len(self.kavmain_inst):
            if self.debug:
                print('[*] Count of KavMain.init() : %d' % (len(self.kavmain_inst)))
            return True
        else:
            return False

    def uninit(self):
        if self.debug:
            print('[*] KavMain.uninit() :')

        for inst in self.kavmain_inst:
            try:
                ret = inst.uninit()
                if self.debug:
                    print('[-] %s.uninit() : %d' % (inst.__module__, ret))
            except AttributeError:
                continue

    def create(self, kmd_modules):
        for mod in kmd_modules:
            try:
                t = mod.KavMain()
                self.kavmain_inst.append(t)
            except AttributeError: # not have KavMain class
                continue

        if len(self.kavmain_inst):
            if self.debug:
                print('[*] Count of KavMain : %d' % (len(self.kavmain_inst)))
            return True
        else:
            return False