import win32serviceutil
import win32service
import win32event
import subprocess
import time

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
        while True:
            subprocess.call(["agent.exe"])
            time.sleep(3600)  # Run every 1 hour

if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(AssetAgentService)
