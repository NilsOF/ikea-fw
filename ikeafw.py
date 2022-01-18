#!/usr/bin/env python3
from struct import pack, unpack
import json
import sys

ota_file_id = pack("<I", 0x0BEEF11E)

def splitfwfile(filename):
    with open(filename, "rb") as f:
        ikeafwf = f.read()
        try:
            offset = ikeafwf.index(ota_file_id)
        except ValueError:
            print('Not a OTA file. Found no OTA 0BEEF11E identifier')
            return
    fwlen = unpack("<I", ikeafwf[offset + 52: offset + 52 + 4])[0]
    print(f"Found OTA 0BEEF11E identifier at: {offset}")
    print(f"OTA file length: {fwlen}")
    outfname = filename + ".ota"
    print(f"Writing splitted out OTA file to: {outfname}")
    with open(outfname, "wb") as f:
        f.write(ikeafwf[offset:offset + fwlen])
    return

def printikeajsonfile(filename):
    with open(filename, "r") as read_file:
        data = json.load(read_file)
    for fwids in data:
        for k,v in fwids.items():
            print(f"{k} : {v}")

if len(sys.argv) > 1:
    if "version_info.json" in sys.argv[1]:
        printikeajsonfile(sys.argv[1])
    elif ".ota" in sys.argv[1]:
        splitfwfile(sys.argv[1])
    else:
        print(f"hmm, file ({sys.argv[1]}) not Ikea json or .ota ??")
else:
    print ("Expected .ota file or json file")
