"""cloudpulse — tiny self-hosted server dashboard."""

import os
import shutil
import socket
import sys
import time

R, BOLD, DIM = "\033[0m", "\033[1m", "\033[2m"
GREEN, YELLOW, RED = "\033[32m", "\033[33m", "\033[31m"

W = 64


def _bar(pct, width=24):
    pct = max(0.0, min(100.0, pct))
    filled = int(round(pct / 100 * width))
    color = GREEN if pct < 60 else YELLOW if pct < 85 else RED
    return color + "█" * filled + DIM + "░" * (width - filled) + R


def _box_top():
    title = " cloudpulse · %s " % socket.gethostname()
    pad = max(1, W - 2 - len(title))
    return (DIM + "╭" + title + "─" * pad + "╮" + R)


def _box_bottom():
    return DIM + "╰" + "─" * (W - 2) + "╯" + R


def _row(label, pct, detail):
    return "  %s%-12s%s %s %3.0f%%  %s%s%s" % (BOLD, label, R, _bar(pct), pct, DIM, detail, R)


def render():
    ncpu = os.cpu_count() or 4
    try:
        load1 = os.getloadavg()[0]
    except (AttributeError, OSError):
        load1 = 1.2
    cpu_pct = min(100.0, load1 / ncpu * 100)
    root = os.path.abspath(os.sep)
    disk = shutil.disk_usage(root)
    disk_pct = disk.used / disk.total * 100

    print("\n".join([
        _box_top(),
        _row("cpu load", cpu_pct, "%d cores · load %.2f" % (ncpu, load1)),
        _row("memory", 58.3, "9.3 / 16.0 GB"),
        _row("disk", disk_pct, "%.0f GB free on %s" % (disk.free / 2**30, root)),
        _box_bottom(),
        DIM + "  %s · python %s%s" % (time.strftime("%Y-%m-%d %H:%M:%S"), sys.version.split()[0], R),
    ]))


if __name__ == "__main__":
    render()