import json
import logging
import time
from pathlib import Path

import psutil

CONFIG_PATH = Path(__file__).resolve().parents[2] / "config" / "config.json"
LOG_PATH = Path(__file__).resolve().parents[2] / "logs" / "monitor.log"

logger = logging.getLogger(__name__)

def configure_logging() -> None:
    """Configure console and file logging."""
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s: %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(LOG_PATH)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

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
        "memory_available_mb": round(memory.available / (1024**2), 2),
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

def report_health(warnings: list[str]) -> None:
    """Log the overall health status and any warnings."""
    if warnings:
        logger.warning("System health is degraded")

        for warning in warnings:
            logger.warning(warning)
    else:
        logger.info("System health is healthy")

def main() -> None:
    """Collect and display a basic host health report."""
    configure_logging()
    
    config = load_config()
    logger.info("Configuration loaded")

    metrics = collect_metrics()
    logger.info("System metrics collected")

    warnings = evaluate_health(metrics, config["thresholds"])
    logger.info("Health evaluation completed")

    print("=== Linux Infrastructure Health ===")
    print(f"CPU utilization:    {metrics['cpu_percent']}%")
    print(f"Memory utilization: {metrics['memory_percent']}%")
    print(f"Memory available:   {metrics['memory_available_mb']} MB")
    print(f"Root disk usage:    {metrics['disk_percent']}%")
    print(f"Root disk free:     {metrics['disk_free_gb']} GB")
    print(f"System uptime:      {metrics['uptime_seconds']} seconds")

    report_health(warnings)

if __name__ == "__main__":
    main()