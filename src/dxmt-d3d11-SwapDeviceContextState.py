#!/usr/bin/env python3
"""Patch DXMT v0.80's d3d11.dll for use as a *native* DLL next to D3DMetal.

1. SwapDeviceContextState (both context types) logs "not implemented" and
   abort()s; Wine's d2d1 calls it on every draw. Replace the body with:
       if (ppPreviousState) { *ppPreviousState = pState; if (pState) pState->AddRef(); }
   d2d sets all the state it needs per draw, so a pass-through is sufficient.
2. Clear the "Wine builtin DLL" stamp so Wine loads it from system32 as native
   (per-app DllOverrides then pick DXMT vs. D3DMetal).

usage: dxmt-d3d11-SwapDeviceContextState.py <in d3d11.dll> <out d3d11.dll>
Function addresses are for DXMT v0.80 (x86_64); found via objdump symbols.
"""
import struct
import sys

FUNCS = (0x3591651F0, 0x3591843C0)  # immediate / deferred context
STUB = bytes.fromhex("4D85C0 7403 498910 4885D2 7409 4889D1 488B02 FF6008 C3".replace(" ", ""))

src, dst = sys.argv[1:3]
d = bytearray(open(src, "rb").read())
pe = struct.unpack_from("<I", d, 0x3C)[0]
nsec = struct.unpack_from("<H", d, pe + 6)[0]
optsz = struct.unpack_from("<H", d, pe + 20)[0]
base = struct.unpack_from("<Q", d, pe + 24 + 24)[0]
secs = [struct.unpack_from("<8sIIII", d, pe + 24 + optsz + i * 40) for i in range(nsec)]
for addr in FUNCS:
    rva = addr - base
    off = next(rva - va + ro for _, vs, va, rs, ro in secs if va <= rva < va + vs)
    assert d[off] == 0x53, "unexpected prologue; not DXMT v0.80?"
    d[off:off + len(STUB)] = STUB
assert d[64:80] == b"Wine builtin DLL"
d[64:80] = b"\0" * 16
open(dst, "wb").write(d)
