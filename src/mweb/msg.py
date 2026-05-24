import struct

def put_int(m, x):
    m += struct.pack("<I", x)

def put_bytes(m, bs):
    put_int(m, len(bs))
    m += bs

def get_int(m, off=0):
    n, = struct.unpack_from("<I", m, off)
    return n, off + 4

def get_bytes(m, off=0):
    n, off = get_int(m, off)
    return m[off:off+n], off + n

def get_strs(m, off=0):
    res = []
    n, off = get_int(m, off)
    for _ in range(n):
        bs, off = get_bytes(m, off)
        res.append(bs.decode())
    return res, off

def get_recipient(m, off=0):
    address, off = get_bytes(m, off)
    value, = struct.unpack_from("<q", m, off)
    return {"Address": address.decode(), "Value": value}, off + 8

def get_recipients(m, off=0):
    res = []
    n, off = get_int(m, off)
    for _ in range(n):
        recipient, off = get_recipient(m, off)
        res.append(recipient)
    return res, off
