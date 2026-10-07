
from sre_monitor.monitor import (
    configure_logging,
    evaluate_health,
    logger,
    report_health,
)


def test_healthy_metrics_produce_no_warnings():
    metrics = {
        "cpu_percent": 20,
        "memory_percent": 40,
        "disk_percent": 30,
    }
    thresholds = {
        "cpu_percent": 80,
        "memory_percent": 85,
        "disk_percent": 85,
    }

    assert evaluate_health(metrics, thresholds) == []


def test_threshold_breach_produces_warning():
    metrics = {
        "cpu_percent": 20,
        "memory_percent": 90,
        "disk_percent": 30,
    }
    thresholds = {
        "cpu_percent": 80,
        "memory_percent": 85,
        "disk_percent": 85,
    }

    warnings = evaluate_health(metrics, thresholds)

    assert len(warnings) == 1
    assert "memory_percent" in warnings[0]


def test_value_equal_to_threshold_triggers_warning():
    metrics = {
        "cpu_percent": 80,
        "memory_percent": 40,
        "disk_percent": 30,
    }
    thresholds = {
        "cpu_percent": 80,
        "memory_percent": 85,
        "disk_percent": 85,
    }

    warnings = evaluate_health(metrics, thresholds)

    assert len(warnings) == 1
    assert "cpu_percent" in warnings[0]

def test_degraded_health_is_logged(caplog):
    """A degraded health result should generate a warning log."""
    metrics = {
    "cpu_percent": 90,
    "memory_percent": 50,
    "disk_percent": 40,
    }

    thresholds = {
    "cpu_percent": 80,
    "memory_percent": 85,
    "disk_percent": 85,
    }

    warnings = evaluate_health(metrics, thresholds)

    assert warnings
    assert "cpu_percent" in warnings[0]

def test_configure_logging_does_not_duplicate_handlers():
    """Repeated logging configuration should not add duplicate handlers."""
    logger.handlers.clear()

    configure_logging()
    first_handler_count = len(logger.handlers)

    configure_logging()
    second_handler_count = len(logger.handlers)

    assert first_handler_count == 2
    assert second_handler_count == 2

    logger.handlers.clear()

def test_degraded_health_is_logged(caplog):
    """A degraded health result should generate warning logs."""
    warnings = [
        "cpu_percent is 90% (threshold: 80%)"
    ]

    with caplog.at_level("WARNING"):
        report_health(warnings)

    assert "System health is degraded" in caplog.text
    assert "cpu_percent is 90%" in caplog.text

def test_healthy_health_is_logged(caplog):
    """A healthy result should generate an info log."""
    with caplog.at_level("INFO"):
        report_health([])

    assert "System health is healthy" in caplog.text