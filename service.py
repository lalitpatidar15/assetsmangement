import win32serviceutil
import win32service
import win32event
import win32evtlogutil
import win32evtlog
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
        self.source_name = self._svc_name_
        try:
            # Ensure event source exists
            win32evtlogutil.AddSourceToRegistry(self.source_name, None, "Application")
        except Exception:
            pass

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        try:
            win32evtlogutil.ReportEvent(self.source_name, 0, 0, win32evtlog.EVENTLOG_INFORMATION_TYPE, strings=["Service stop requested"])
        except Exception:
            pass

    def SvcDoRun(self):
        # Resolve agent path relative to the service executable directory
        exe_dir = os.path.dirname(sys.executable)
        agent_path = os.path.join(exe_dir, "agent.exe")
        try:
            win32evtlogutil.ReportEvent(self.source_name, 0, 0, win32evtlog.EVENTLOG_INFORMATION_TYPE, strings=[f"Service started. Agent path: {agent_path}"])
        except Exception:
            pass
        while True:
            try:
                subprocess.call([agent_path])
            except Exception:
                try:
                    win32evtlogutil.ReportEvent(self.source_name, 0, 0, win32evtlog.EVENTLOG_WARNING_TYPE, strings=["Agent execution failed"])
                except Exception:
                    pass
            # Sleep for ~1 hour, checking stop event every second for graceful shutdown
            for _ in range(3600):
                if win32event.WaitForSingleObject(self.stop_event, 1000) == win32event.WAIT_OBJECT_0:
                    try:
                        win32evtlogutil.ReportEvent(self.source_name, 0, 0, win32evtlog.EVENTLOG_INFORMATION_TYPE, strings=["Service stopping"])
                    except Exception:
                        pass
                    return

if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(AssetAgentService)
