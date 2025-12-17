import json
import hashlib
import psutil
import platform
import subprocess
from datetime import datetime

try:
    import wmi  # Windows only
except Exception:
    wmi = None


def get_disks_windows():
    c = wmi.WMI()
    disks = []
    for disk in c.Win32_DiskDrive():
        disks.append({
            "model": (disk.Model or "").strip(),
            "serial": (getattr(disk, "SerialNumber", None) or "UNKNOWN").strip(),
            "size_gb": round(int(disk.Size) / (1024**3), 2) if getattr(disk, "Size", None) else 0.0,
            "interface": getattr(disk, "InterfaceType", "Unknown"),
            "media_type": getattr(disk, "MediaType", "Unknown"),
        })
    return disks


def get_disks_macos():
    disks = []
    try:
        # NVMe
        nvme_raw = subprocess.check_output(["/usr/sbin/system_profiler", "SPNVMeDataType", "-json"], text=True)
        nvme = json.loads(nvme_raw).get("SPNVMeDataType", [])
        for ctrl in nvme:
            for dev in ctrl.get("com_apple_spnvme_nvme_device", []) or []:
                size_bytes = dev.get("size_in_bytes") or dev.get("size")
                try:
                    size_gb = round(int(size_bytes) / (1024**3), 2) if size_bytes else 0.0
                except Exception:
                    size_gb = 0.0
                disks.append({
                    "model": dev.get("device_model", "Unknown"),
                    "serial": dev.get("device_serial", "UNKNOWN"),
                    "size_gb": size_gb,
                    "interface": "NVMe",
                    "media_type": "Solid State",
                })
    except Exception:
        pass

    try:
        # SATA
        sata_raw = subprocess.check_output(["/usr/sbin/system_profiler", "SPSerialATADataType", "-json"], text=True)
        sata = json.loads(sata_raw).get("SPSerialATADataType", [])
        for ctrl in sata:
            for dev in ctrl.get("_items", []) or []:
                size_bytes = dev.get("size_in_bytes") or dev.get("size")
                try:
                    size_gb = round(int(size_bytes) / (1024**3), 2) if size_bytes else 0.0
                except Exception:
                    size_gb = 0.0
                disks.append({
                    "model": dev.get("device_model") or dev.get("_name", "Unknown"),
                    "serial": dev.get("serial_number", "UNKNOWN"),
                    "size_gb": size_gb,
                    "interface": "SATA",
                    "media_type": "Unknown",
                })
    except Exception:
        pass
    return disks


def get_disks_linux():
    disks = []
    try:
        lsblk_raw = subprocess.check_output(["lsblk", "-b", "-J", "-o", "NAME,MODEL,SERIAL,SIZE,ROTA,TYPE"], text=True)
        data = json.loads(lsblk_raw)
        for b in data.get("blockdevices", []) or []:
            if b.get("type") == "disk":
                size_gb = round(int(b.get("size") or 0) / (1024**3), 2)
                media_type = "HDD" if (b.get("rota") in (1, "1", True)) else "Solid State"
                disks.append({
                    "model": b.get("model", "Unknown").strip(),
                    "serial": (b.get("serial") or "UNKNOWN").strip(),
                    "size_gb": size_gb,
                    "interface": "Unknown",
                    "media_type": media_type,
                })
    except Exception:
        pass
    return disks


def get_disks():
    system = platform.system()
    if system == "Windows" and wmi is not None:
        return get_disks_windows()
    if system == "Darwin":
        return get_disks_macos()
    if system == "Linux":
        return get_disks_linux()
    return []

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
