import win32serviceutil
import win32service
import win32event
import subprocess
import time
import os
import sys

class AssetAgentService(win32serviceutil.ServiceFramework):
    _svc_name_ = "AssetIntegrityAgent"
    _svc_display_name_ = "Asset Integrity Monitoring Agent"
    _svc_description_ = "Monitors disk hardware integrity"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)

    def SvcDoRun(self):
        # Resolve agent path relative to the service executable directory
        exe_dir = os.path.dirname(sys.executable)
        agent_path = os.path.join(exe_dir, "agent.exe")
        while True:
            try:
                subprocess.call([agent_path])
            except Exception:
                pass
            # Sleep for ~1 hour, checking stop event every second for graceful shutdown
            for _ in range(3600):
                if win32event.WaitForSingleObject(self.stop_event, 1000) == win32event.WAIT_OBJECT_0:
                    return

if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(AssetAgentService)
