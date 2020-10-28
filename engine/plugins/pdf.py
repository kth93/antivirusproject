import re
import zlib

class KavMain:
    def init(self, plugins_path):
        pat = rb'^s*%PDF-1.'
        self.p_pdf_header = re.compile(pat, re.IGNORECASE)

        pat = rb'(\d+)\s+0\s+obj\s*<<.+>>\s*?stream\s*([\d\D]+?)\s*endstream\s+endobj'
        self.p_pdf_obj = re.compile(pat, re.IGNORECASE)

        pat = rb'/Filter\s+/(\w+)'
        self.p_pdf_filter = re.compile(pat, re.IGNORECASE)

        return 0

    def uninit(self):
        return 0

    def getinfo(self):
        info = dict()
        
        info['author'] = 'kth93'
        info['version'] = '1.0'
        info['title'] = 'PDF Engine'
        info['kmd_name'] = 'pdf'

        return info
    
    def format(self, filehandle, filename):
        mm = filehandle
        buf = mm[:4096]

        if self.p_pdf_header.match(buf):
            ret = {'ff_pdf', 'PDF'}

            return ret
        
        return None
    
    def arclist(self, filename, fileformat):
        file_scan_list = []

        if 'ff_pdf' in fileformat:
            buf = ''
            print(buf)
            try:
                with open(filename, 'rb') as fp:
                    buf = fp.read()
            except IOError:
                return []

            for obj in self.p_pdf_obj.finditer(buf):
                obj_id = obj.groups()[0] # get Object Id from Stream
                file_scan_list.append(['arc_pdf', 'PDF #%s' % obj_id])
        
        return file_scan_list

    def unarc(self, arc_engine_id, arc_name, fname_in_arc):
        if arc_engine_id == 'arc_pdf':
            buf = ''

            try:
                with open(arc_name, 'rb') as fp:
                    buf = fp.read()
            except IOError:
                return None
            
            for obj in self.p_pdf_obj.finditer(buf):
                obj_id = obj.groups()[0]
                if obj_id == fname_in_arc[5:]: # need decompress?
                    data = obj.groups()[1]

                    t = self.p_pdf_filter.search(obj.group())
                    if (t is not None) and (t.group()[0].lower() == 'flatedecode'):
                        try:
                            data = zlib.decompress(data)
                        except zlib.error:
                            pass

                    return data
        
        return None
