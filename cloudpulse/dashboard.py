"""cloudpulse — tiny self-hosted server dashboard. Stdlib-only core."""

import argparse
import os
import shutil
import socket
import sys
import time

R, BOLD, DIM = "\033[0m", "\033[1m", "\033[2m"
GREEN, YELLOW, RED, CYAN = "\033[32m", "\033[33m", "\033[31m", "\033[36m"

W = 64

# Optional pretty output via prettyformat-utils (declared in requirements.txt).
# Falls back to a local implementation so the core stays stdlib-only.
try:
    from prettyformat_utils import format_bytes as _fmt_bytes

    _USING_PRETTY = True
except ImportError:  # pragma: no cover - pre-install fallback

    def _fmt_bytes(n):
        for unit in ("B", "KB", "MB", "GB", "TB"):
            n = float(n)
            if abs(n) < 1024.0 or unit == "TB":
                return ("%.1f %s" % (n, unit)).strip()
            n /= 1024.0

    _USING_PRETTY = False


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


def _svc(name, status, detail):
    dot, col = {
        "healthy": ("●", GREEN),
        "degraded": ("●", YELLOW),
    }.get(status, ("●", RED))
    return "   %-16s%s%s %-8s%s %s%s%s" % (name, col, dot, status, R, DIM, detail, R)


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

    out = [
        _box_top(),
        _row("cpu load", cpu_pct, "%d cores · load %.2f" % (ncpu, load1)),
        _row("memory", 58.3, "9.3 / 16.0 GB"),
        _row("disk", disk_pct, "%s free on %s" % (_fmt_bytes(disk.free), root)),
        "",
        "  " + BOLD + "SERVICES" + R,
        _svc("api-gateway", "healthy", "p99 12ms · 0 errors"),
        _svc("worker-pool", "healthy", "4/4 nodes · queue 0"),
        _svc("billing-sync", "degraded", "queue 2.4k · retrying"),
        _svc("redis-cache", "healthy", "hit rate 98.1%"),
        "",
        _box_bottom(),
        DIM + "  %s · python %s · rendered with %s%s" % (
            time.strftime("%Y-%m-%d %H:%M:%S"),
            sys.version.split()[0],
            "prettyformat-utils" if _USING_PRETTY else "stdlib fallback",
            R,
        ),
    ]
    print("\n".join(out))


def main():
    parser = argparse.ArgumentParser(prog="cloudpulse")
    parser.add_argument("--watch", action="store_true", help="live refresh")
    parser.add_argument("--interval", type=float, default=1.0)
    args = parser.parse_args()
    if args.watch:
        try:
            while True:
                print("\033[2J\033[H", end="")
                render()
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print(R + "\nbye.")
    else:
        render()


if __name__ == "__main__":
    main()