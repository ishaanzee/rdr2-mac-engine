import struct,sys
def exports(p):
    d=open(p,'rb').read(); pe=struct.unpack_from('<I',d,0x3c)[0]; nsec=struct.unpack_from('<H',d,pe+6)[0]; osz=struct.unpack_from('<H',d,pe+20)[0]
    opt=pe+24; magic=struct.unpack_from('<H',d,opt)[0]; dd=opt+(112 if magic==0x20b else 96)
    erva=struct.unpack_from('<I',d,dd)[0]; secs=[struct.unpack_from('<8sIIII',d,pe+24+osz+i*40) for i in range(nsec)]
    def off(r):
        for n,vs,va,rs,ro in secs:
            if va<=r<va+max(vs,rs): return r-va+ro
    if not erva: return []
    e=off(erva); nn=struct.unpack_from('<I',d,e+24)[0]; np_=off(struct.unpack_from('<I',d,e+32)[0])
    out=[]
    for i in range(nn):
        s=off(struct.unpack_from('<I',d,np_+4*i)[0]); out.append(d[s:d.index(b'\0',s)].decode())
    return out
for p in sys.argv[1:]: print(p.split('/')[-1], exports(p))
