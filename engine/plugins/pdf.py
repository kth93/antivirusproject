import re
import zlib

class KavMain:
    def init(self, plugins_path):
        pat = r'^s*%PDF-1.'
        self.p_pdf_header = re.compile(pat, re.IGNORECASE)

        pat = r'(\d+)\s+0\s+obj\s*<<.+>>\s*?stream\s*([\d\D]+?)\s*endstream\s+endobj'
        self.p_pdf_obj = re.compile(pat, re.IGNORECASE)

        pat = r'/Filter\s+/(\w+)'
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