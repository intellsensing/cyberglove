"""
Sensor reading
==============
A simple console application that takes readings from a CyberGlove every 500 ms
and displays the raw (i.e. uncalibrated measurements) on the screen.
"""

import argparse
import threading
import time

from cyberglove import CyberGlove


class RepeatedTimer(object):
    """
    A simple timer implementation that repeats itself and avoids drift over
    time.
    Implementation based on https://stackoverflow.com/a/40965385.

    Parameters
    ----------
    target : callable
        Target function
    interval : float
        Target function repetition interval
    name : str, optional (default: None)
        Thread name
    args : list
        Non keyword-argument list for target function
    kwargs : key,value mappings
        Keyword-argument dict for target function
    """

    def __init__(self, target, interval, args=(), kwargs={}):

        self.target = target
        self.interval = interval
        self.args = args
        self.kwargs = kwargs

        self._timer = None
        self._is_running = False
        self._next_call = time.time()

    def _run(self):
        self._is_running = False
        self.start()
        self.target(*self.args, **self.kwargs)

    def start(self):
        if not self._is_running:
            self._next_call += self.interval
            self._timer = threading.Timer(self._next_call - time.time(),
                                          self._run)
            self._timer.start()
            self._is_running = True

    def stop(self):
        self._timer.cancel()
        self._is_running = False


def display_sensor_readings(cyberglove):
    """Displays raw sensor readings.

    cyberglove : CyberGlove
        Device to take readings from.
    """
    raw_data = cyberglove.read()
    print("\nData glove raw measurements:\n{}".format(
        raw_data.reshape(-1,).tolist()))


def main(s_port):
    cg = CyberGlove(n_df=18, s_port=s_port, samples_per_read=1)
    rt = RepeatedTimer(display_sensor_readings, 0.5, kwargs={"cyberglove": cg})
    rt.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        rt.stop()
        cg.stop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("port", help="Data glove serial port (str).",
                        type=str)
    args = parser.parse_args()
    s_port = args.port
    main(s_port)
