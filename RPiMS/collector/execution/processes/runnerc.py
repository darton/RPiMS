#!/usr/bin/env python3

# -*- coding:utf-8 -*-
#
#  Author : Dariusz Kowalczyk
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License Version 2 as
#  published by the Free Software Foundation.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

# Use in main function before pause() 
#     threading.Thread(target=supervise_forever, daemon=True).start()
#     pause()

# Use in main function when not using pause()
# supervise_forever()


import multiprocessing as mp
import logging
import time
import traceback

log = logging.getLogger(__name__)


class ManagedProcess:
    def __init__(self, func, args, kwargs, name):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.name = name
        self.proc = None
        self.restarts = 0

    def start(self):
        """run proces."""
        self.proc = mp.Process(
            target=self._run_wrapper,
            name=self.name
        )
        self.proc.start()
        log.info(f"[PROC] Started {self.name} (pid={self.proc.pid})")

    def _run_wrapper(self):
        """
        A function wrapper to log exceptions.
        """
        try:
            self.func(*self.args, **self.kwargs)
        except Exception:
            log.error(f"[PROC] {self.name} crashed:\n{traceback.format_exc()}")
            raise

    def supervise(self):
        """It checks if the process is alive — if not, it restarts it."""
        if not self.proc.is_alive():
            log.warning(f"[PROC] {self.name} died, restarting...")
            time.sleep(1)
            self.start()
            self.restarts += 1


class ProcessSupervisor:
    def __init__(self):
        self.processes = []

    def start_process(self, func, *args, name=None, **kwargs):
        """ We are adding processes to the list of monitored ones. """
        proc_name = name or func.__name__
        mp_obj = ManagedProcess(func, args, kwargs, proc_name)
        mp_obj.start()
        self.processes.append(mp_obj)

    def supervise_forever(self):
        """Supervisory loop."""
        try:
            while True:
                for p in self.processes:
                    p.supervise()
                time.sleep(0.5)
        except KeyboardInterrupt:
            log.info("[PROC] Supervisor stopped")
            self.stop_all()

    def stop_all(self):
        """Stoping all processes."""
        for p in self.processes:
            if p.proc.is_alive():
                log.info(f"[PROC] Terminating {p.name} (pid={p.proc.pid})")
                p.proc.terminate()
                p.proc.join(timeout=5)


supervisor = ProcessSupervisor()

start_process = supervisor.start_process
supervise_forever = supervisor.supervise_forever
stop_all_processes = supervisor.stop_all

