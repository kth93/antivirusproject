import time

# t is 2byte date obejct
def convert_date(t):
    y = ((t & 0xFE00) >> 9) + 1980
    m = (t & 0x01E0) >> 5
    d = (t & 0x001F)

    # print('%04d-%02d-%02d' % (y, m, d))
    return y, m, d

# t is 2byte time obejct
def convert_time(t):
    h = (t & 0xF800) >> 11
    m = (t & 0x07E0) >> 5
    s = (t & 0x001F) * 2

    # print('%02d-%02d-%02d' % (h, m, s))
    return h, m, s

# convert now_date to 2byte date object
def get_now_date(now=None):
    if not now:
        now = time.gmtime()
    
    t_y = now.tm_year - 1980
    t_y = (t_y << 9) & 0xFE00
    t_m = (now.tm_mon << 5) & 0x01E0
    t_d = now.tm_mday & 0x001F

    return (t_y | t_m | t_d) & 0xFFFF

# convert now_time to 2byte time object
def get_now_time(now=None):
    if not now:
        now = time.gmtime()
    
    t_h = (now.tm_hour << 11) & 0xF800
    t_m = (now.tm_min << 5) & 0x07E0
    t_s = int(now.tm_sec / 2) & 0x001F

    return (t_h | t_m | t_s) & 0xFFFF