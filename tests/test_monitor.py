
from sre_monitor.monitor import evaluate_health


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