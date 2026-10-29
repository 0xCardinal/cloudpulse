# cloudpulse

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org)

A tiny, self-hosted server monitoring dashboard. One file, stdlib-only core,
renders straight in your terminal.

## Install

Requires Python 3.8+. Our optional pretty-output helper is hosted on the PyPI
test index — the index is already configured in `requirements.txt`, so just:

```bash
python -m venv demoenv && source demoenv/bin/activate   # recommended
python -m pip install -r requirements.txt
```

## Usage

```bash
python -m cloudpulse             # one snapshot
python -m cloudpulse --watch     # live refresh (Ctrl+C to quit)
cloudpulse --watch               # same, after install
```

## What it shows

- CPU load, disk usage, core count
- Service health table (api-gateway, worker-pool, billing-sync, redis-cache)
- Optional output formatting via `prettyformat-utils`

## Changelog

See [CHANGELOG.md](CHANGELOG.md). MIT license — see [LICENSE](LICENSE).
