"""
SYNTX Algorithms - Statistical & ML algorithms
"""

from typing import List, Dict, Any
import statistics

def calculate_moving_average(values: List[float], window: int = 5) -> List[float]:
    if len(values) < window:
        return values
    result = []
    for i in range(len(values)):
        if i < window - 1:
            result.append(values[i])
        else:
            window_values = values[i - window + 1:i + 1]
            result.append(sum(window_values) / window)
    return result

def detect_outliers(values: List[float], threshold: float = 2.0) -> List[int]:
    if len(values) < 3:
        return []
    mean = statistics.mean(values)
    stdev = statistics.stdev(values)
    outliers = []
    for i, value in enumerate(values):
        z_score = abs((value - mean) / stdev) if stdev > 0 else 0
        if z_score > threshold:
            outliers.append(i)
    return outliers

def calculate_trend(values: List[float]) -> str:
    if len(values) < 2:
        return "STABIL"
    n = len(values)
    x = list(range(n))
    x_mean = sum(x) / n
    y_mean = sum(values) / n
    numerator = sum((x[i] - x_mean) * (values[i] - y_mean) for i in range(n))
    denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
    if denominator == 0:
        return "STABIL"
    slope = numerator / denominator
    if slope > 0.5:
        return "STEIGEND"
    elif slope < -0.5:
        return "FALLEND"
    else:
        return "STABIL"

def calculate_correlation(x: List[float], y: List[float]) -> float:
    if len(x) != len(y) or len(x) < 2:
        return 0.0
    n = len(x)
    x_mean = sum(x) / n
    y_mean = sum(y) / n
    numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
    x_var = sum((x[i] - x_mean) ** 2 for i in range(n))
    y_var = sum((y[i] - y_mean) ** 2 for i in range(n))
    denominator = (x_var * y_var) ** 0.5
    if denominator == 0:
        return 0.0
    return numerator / denominator

def calculate_velocity(values: List[float]) -> float:
    if len(values) < 2:
        return 0.0
    changes = [values[i] - values[i-1] for i in range(1, len(values))]
    return sum(changes) / len(changes) if changes else 0.0

def predict_next_value(values: List[float]) -> float:
    if len(values) < 3:
        return values[-1] if values else 0.0
    recent = values[-3:]
    return sum(recent) / len(recent)

def calculate_health_score(metrics: Dict[str, float], weights: Dict[str, float]) -> float:
    total_weight = sum(weights.values())
    if total_weight == 0:
        return 0.0
    weighted_sum = sum(metrics.get(key, 0) * weight for key, weight in weights.items())
    return (weighted_sum / total_weight) * 100

def detect_bottleneck(queue_history: List[Dict]) -> Dict[str, Any]:
    if len(queue_history) < 5:
        return {"detected": False}
    processing_counts = [q.get('processing', 0) for q in queue_history[-5:]]
    avg_processing = sum(processing_counts) / len(processing_counts)
    if avg_processing > 5:
        return {"detected": True, "type": "HIGH_PROCESSING", "avg_processing": avg_processing}
    incoming_counts = [q.get('incoming', 0) for q in queue_history[-5:]]
    if all(incoming_counts[i] < incoming_counts[i+1] for i in range(len(incoming_counts)-1)):
        return {"detected": True, "type": "GROWING_BACKLOG", "growth_rate": incoming_counts[-1] - incoming_counts[0]}
    return {"detected": False}
