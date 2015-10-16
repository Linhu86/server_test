import os
import re
import subprocess
import threading

class Runner(threading.Thread):
    def __init__(self, cfg, number, params, callback):
        self.stdout = None
        self.stderr = None
        self.cfg = cfg
        self.tc_number = number
        self.tc_parameters = params
        self.callback = callback
        threading.Thread.__init__(self)

    def run(self):
        output = ""
        cmd = ["perl", self.tc_number, "-cfg", self.cfg] + self.tc_parameters
        # os.chdir("/windows/userdata/Perforce/dev_sgo_acri/src")
        os.chdir("C:/userdata/Perforce/dev_sgo_acri/src")
        # cmd = ["ping", "-c", "25", "localhost"] # Test command, long enough but not too much, guaranteed to work!
        self.proc = subprocess.Popen(
            cmd,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        # Poll process for new output until finished
        for line in self.proc.stdout:
            output += line.decode()
            print(line.decode())
        # Check result
        res_match = re.search("Final Verdict is: (\w{4})", output)
        if res_match:
            res = res_match.group(1)
        else:
            res = "ABORTED"
        # Wait for process to finish and invoke the callback
        self.proc.wait()
        self.callback(result=res)
        return self.proc.returncode

    def terminate(self):
        self.proc.kill()