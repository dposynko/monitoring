# Linux Infrastructure Monitor

A Python-based Linux infrastructure monitoring tool that collects host-level resource metrics, evaluates them against configurable thresholds, and reports system health.

This project was built as an SRE learning and portfolio project with an emphasis on observability, reliability, testing, and operational simplicity.

## Project Goals

The monitor is designed to:

* Collect Linux host resource metrics
* Evaluate metrics against configurable thresholds
* Identify potentially degraded system conditions
* Provide a simple health status
* Keep monitoring configuration separate from application code
* Validate monitoring behavior with automated tests

The project is intentionally being developed incrementally to demonstrate the engineering decisions behind a small SRE monitoring system.

## Current Capabilities

The current implementation monitors:

* CPU utilization
* Memory utilization
* Available memory
* Root filesystem utilization
* Available root filesystem capacity
* System uptime

The monitor currently reports two possible states:

* `HEALTHY` — configured thresholds are not exceeded
* `DEGRADED` — one or more configured thresholds are exceeded

## Architecture

```text
                 Linux Host
                     │
                     ▼
              ┌──────────────┐
              │   psutil     │
              └──────┬───────┘
                     │
                     ▼
             collect_metrics()
                     │
                     ▼
              ┌──────────────┐
              │    Metrics   │
              └──────┬───────┘
                     │
                     ▼
             evaluate_health()
                     │
              ┌──────┴──────┐
              ▼             ▼
          HEALTHY       DEGRADED
```

Configuration is kept separately:

```text
config/config.json
        │
        ▼
   load_config()
        │
        ▼
health thresholds
```

## Project Structure

```text
monitoring/
├── config/
│   └── config.json
├── logs/
├── src/
│   └── sre_monitor/
│       ├── __init__.py
│       └── monitor.py
├── tests/
│   └── test_monitor.py
├── .gitignore
├── pytest.ini
├── README.md
└── requirements.txt
```

### Directory Responsibilities

| Directory/File     | Purpose                          |
| ------------------ | -------------------------------- |
| `src/sre_monitor/` | Application source code          |
| `tests/`           | Automated tests                  |
| `config/`          | Runtime monitoring configuration |
| `logs/`            | Runtime log files                |
| `requirements.txt` | Python dependencies              |
| `pytest.ini`       | Pytest configuration             |
| `README.md`        | Project documentation            |

## Requirements

* Linux
* Python 3.12+
* `pip`
* Python virtual environment support

## Installation

Clone the repository and enter the project directory:

```bash
cd monitoring
```

Create a Python virtual environment:

```bash
python3 -m venv .venv
```

Activate the environment:

```bash
source .venv/bin/activate
```

Install the project dependencies:

```bash
python -m pip install -r requirements.txt
```

## Configuration

Monitoring thresholds are defined in:

```text
config/config.json
```

Example:

```json
{
  "thresholds": {
    "cpu_percent": 80,
    "memory_percent": 85,
    "disk_percent": 85
  }
}
```

These values are initial project defaults and are not intended to represent universal production thresholds.

Thresholds should ultimately be selected based on workload characteristics, historical behavior, and service-level objectives.

## Running the Monitor

From the project root:

```bash
python -m sre_monitor.monitor
```

The application reports the current host metrics and overall health status.

Example:

```text
=== Linux Infrastructure Health ===
CPU utilization:    23.7%
Memory utilization: 56.0%
Memory available:   7032.43 MB
Root disk usage:    12.4%
Root disk free:     784.86 GB
System uptime:      451822 seconds

STATUS: HEALTHY
```

The actual values will vary depending on the host's current workload.

## Running Tests

Run the complete test suite with:

```bash
python -m pytest -v
```

The tests currently validate:

1. Healthy metrics produce no warnings.
2. A threshold breach produces a warning.
3. A value exactly equal to the configured threshold triggers a warning.

Example:

```text
3 passed
```

## Design Decisions

### Separate metric collection from health evaluation

Metric collection and health evaluation are implemented as separate functions.

This allows the health evaluation logic to be tested using controlled input without having to manipulate the actual Linux host.

For example, tests can provide simulated CPU or memory values without intentionally exhausting system resources.

### Configuration is separate from application logic

Thresholds are stored in JSON rather than hard-coded into the monitoring logic.

This allows operational thresholds to be changed without modifying the Python implementation.

### The project uses a `src` layout

Application code is kept under:

```text
src/sre_monitor/
```

This separates the Python package from project-level files such as tests, configuration, and documentation.

## Roadmap

The project will be developed incrementally.

### Completed

* [x] Collect Linux host metrics
* [x] Evaluate metrics against configurable thresholds
* [x] Report `HEALTHY` and `DEGRADED` states
* [x] Add automated tests
* [x] Document project architecture and usage

### Planned

* [ ] Add structured application logging
* [ ] Add continuous monitoring
* [ ] Add service/process health checks
* [ ] Detect failure and recovery events
* [ ] Improve configuration validation
* [ ] Run as a Linux `systemd` service
* [ ] Expose Prometheus-compatible metrics
* [ ] Expand automated testing
* [ ] Add failure simulation and reliability testing

## SRE Concepts Demonstrated

This project is intended to demonstrate practical application of:

* Observability
* Monitoring
* Health checks
* Alert thresholds
* Failure detection
* Recovery detection
* Configuration management
* Automated testing
* Linux operations
* Python automation
* Service management
* Reliability engineering

## Project Status

**Current status: Early development**

The monitor currently performs point-in-time host monitoring. It is not intended to replace a production monitoring platform.

Future iterations will introduce continuous monitoring, structured logging, service health checks, and metrics export.
