import json
import time
from pathlib import Path

import psutil

CONFIG_PATH = Path(__file__).resolve().parents[2] / "config" / "config.json"

def load_config() -> dict:
    """Load monitoring thresholds from the JSON configuration file."""
    with CONFIG_PATH.open(encoding="utf-8") as config_file:
        return json.load(config_file)

def collect_metrics() -> dict:
    """Collect basic health metrics from the local Linux host."""

    # CPU utilization average over a one-second sampling interval.
    cpu_percent = psutil.cpu_percent(interval=1)

    # System memory utilization.
    memory = psutil.virtual_memory()

    # Disk utilization for the root filesystem
    disk = psutil.disk_usage("/")

    # Second since the system booted
    uptime_seconds = int(time.time() - psutil.boot_time())

    return {
        "cpu_percent": cpu_percent,
        "memory_percent": memory.percent,
        "memory_available_mb": round(memory.available / (1021**2), 2),
        "disk_percent": disk.percent,
        "disk_free_gb": round(disk.free / (1024**3), 2),
        "uptime_seconds": uptime_seconds,
    }

def evaluate_health(metrics: dict, thresholds: dict) -> list[str]:
    """Return warnings for metrics that exceed their thresholds."""
    warnings = []

    for metric_name in ("cpu_percent", "memory_percent", "disk_percent"):
        value = metrics[metric_name]
        threshold = thresholds[metric_name]

        if value >= threshold:
            warnings.append(f"{metric_name} is {value}% "
                            f"(threshold: {threshold}%)")
    return warnings

def main() -> None:
    """Collect and display a basic host health report."""
    config = load_config()
    metrics = collect_metrics()
    warnings = evaluate_health(metrics, config["thresholds"])

    print("=== Linux Infrastructure Health ===")
    print(f"CPU utilization:    {metrics['cpu_percent']}%")
    print(f"Memory utilization: {metrics['memory_percent']}%")
    print(f"Memory available:   {metrics['memory_available_mb']} MB")
    print(f"Root disk usage:    {metrics['disk_percent']}%")
    print(f"Root disk free:     {metrics['disk_free_gb']} GB")
    print(f"System uptime:      {metrics['uptime_seconds']} seconds")

    if warnings:
        print("\nSTATUS: DEGRADED")
        for warning in warnings:
            print(f"WARNING: {warning}")
    else:
        print("\nSTATUS: HEALTHY")

if __name__ == "__main__":
    main()