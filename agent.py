import wmi
import json
import hashlib
import psutil
from datetime import datetime

c = wmi.WMI()

def get_disks():
    disks = []
    for disk in c.Win32_DiskDrive():
        disks.append({
            "model": disk.Model.strip(),
            "serial": disk.SerialNumber.strip() if getattr(disk, "SerialNumber", None) else "UNKNOWN",
            "size_gb": round(int(disk.Size) / (1024**3), 2),
            "interface": disk.InterfaceType,
            "media_type": disk.MediaType,
        })
    return disks

def create_fingerprint(disks):
    base_string = ""
    for d in disks:
        base_string += d["serial"] + str(d["size_gb"])
    return hashlib.sha256(base_string.encode()).hexdigest()

if __name__ == "__main__":
    disk_info = get_disks()
    fingerprint = create_fingerprint(disk_info)

    output = {
        "timestamp": datetime.utcnow().isoformat(),
        "disks": disk_info,
        "fingerprint": fingerprint
    }

    print(json.dumps(output, indent=4))
