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

# Use in main function before pause().
#     threading.Thread(target=supervise_forever, daemon=True).start()
#     pause()

# Use in main function when not using pause()
# supervise_forever()


import multiprocessing as mp
import logging
import time
import traceback

log = logging.getLogger(__name__)

_processes = []


def _wrap_target(func, args, kwargs, name):
    """
    A function wrapper to log exceptions.
    This way the supervisor knows that the process has crashed.
    """
    try:
        func(*args, **kwargs)
    except Exception:
        log.error(f"[PROC] {name} crashed:\n{traceback.format_exc()}")
        raise


def start_process(func, *args, name=None, **kwargs):
    """
    We are adding processes to the list of monitored ones.
    """
    proc_name = name or func.__name__

    proc = mp.Process(
        target=_wrap_target,
        args=(func, args, kwargs, proc_name),
        name=proc_name,
    )
    proc.start()

    _processes.append({
        "name": proc_name,
        "func": func,
        "args": args,
        "kwargs": kwargs,
        "proc": proc,
        "restarts": 0,
    })

    log.info(f"[PROC] Started {proc_name} (pid={proc.pid})")


def supervise_forever():
    """
    Supervisory loop — restarts processes that have failed.
    Call in main() or in a separate thread if you are using GPIO+pause().
    """
    try:
        while True:
            for p in _processes:
                proc = p["proc"]

                if not proc.is_alive():
                    log.warning(f"[PROC] {p['name']} died, restarting...")

                    time.sleep(1)

                    new_proc = mp.Process(
                        target=_wrap_target,
                        args=(p["func"], p["args"], p["kwargs"], p["name"]),
                        name=p["name"],
                    )
                    new_proc.start()

                    p["proc"] = new_proc
                    p["restarts"] += 1

                    log.info(f"[PROC] Restarted {p['name']} (pid={new_proc.pid})")

            time.sleep(0.5)

    except KeyboardInterrupt:
        log.info("[PROC] Supervisor stopped")
        stop_all_processes()


def stop_all_processes():
    """
    It stops all processes when closing the application.
    """
    for p in _processes:
        proc = p["proc"]
        if proc.is_alive():
            log.info(f"[PROC] Terminating {p['name']} (pid={proc.pid})")
            proc.terminate()
            proc.join(timeout=5)

