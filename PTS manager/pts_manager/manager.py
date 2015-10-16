import os
import re
import tempfile

from enum import Enum
from runner import Runner
from server import Server

# Possible states of the PTS manager
states = Enum('states', 'finished running config idle', module=__name__)

class Manager():
    def __init__(self):
        # State of the manager and map of handler to be called when receiving request
        self.state = states.idle
        self.state_handlers = {
            states.finished: self.request_in_finished,
            states.running: self.request_in_running,
            states.config: self.request_in_config,
            states.idle: self.request_in_idle,
        }
        self.dut_parameters = "../cfg/DUT_Parameters.txt"

    def handler(self, request):
        if not request:
            return "INVALID REQUEST", False
        return self.state_handlers[self.state](request.rstrip())

    def request_in_idle(self, request):
        if request == "CONFIG" in request:
            self.state = states.config
            # Overwrite config file
            with open(self.dut_parameters, 'w'): pass
            return "OK", True
        elif "RUN" in request:
            # Get test case number and params from the request
            match = re.search(r"RUN (?P<number>(?:\d+\.?)+.pl)(?P<params>.*)", request)
            if not match:
                return "WRONG REQUEST", True
            number = match.group("number")
            params = match.group("params").split()
            self.state = states.running
            self.runner = Runner(number=number, params=params, cfg=self.dut_parameters, callback=self.test_finished)
            self.runner.start()
            return "OK", True
        else:
            return "WRONG REQUEST", True

    def request_in_finished(self, request):
        if request == "RESULT":
            self.state = states.idle
            return "RESULT: %s" % self.result, False
        else:
            return "WRONG REQUEST", True

    def request_in_config(self, request):
        if request == "ENDCONFIG":
            self.state = states.idle
            return "OK", True
        else:
            with open(self.dut_parameters, 'a') as dut_parameters:
                print(request, file=dut_parameters)
            return "WROTE TO CONFIG", True

    def request_in_running(self, request):
        if request == "ABORT":
            self.runner.terminate()
            self.result = "ABORTED"
            self.state = states.finished
            return "OK", True
        else:
            return "BUSY", True

    def test_finished(self, result):
        self.state = states.finished
        self.result = result


if __name__ == "__main__":
    ptsmgr = Manager()
    server = Server(ptsmgr.handler)
    