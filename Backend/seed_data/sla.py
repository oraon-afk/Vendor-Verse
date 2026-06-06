import random
from datetime import datetime
from models import SLAMetric


def generate_sla_metrics(supplier):
    """Generate SLA metrics based on actual supplier data from the Kaggle dataset."""
    metrics = []
    now = datetime.utcnow()

    # Lead time SLA
    lead_threshold = 20  # days max acceptable
    lead_target = 12     # days ideal
    lead_current = supplier.avg_lead_time
    if lead_current <= lead_target:
        lead_status = "compliant"
    elif lead_current <= lead_threshold:
        lead_status = "warning"
    else:
        lead_status = "breached"
    lead_deviation = round((lead_current - lead_target) / lead_target * 100, 1)

    metrics.append(SLAMetric(
        id=f"{supplier.supplier_id}-lead_time",
        supplier_id=supplier.supplier_id,
        supplier_name=supplier.name,
        metric="lead_time",
        current=round(lead_current, 1),
        threshold=lead_threshold,
        target=lead_target,
        unit="days",
        status=lead_status,
        deviation_percent=lead_deviation,
        trend=random.choice(["up", "down", "stable"]),
        updated_at=now,
    ))

    # Shipping time SLA
    ship_threshold = 7   # days max
    ship_target = 4      # days ideal
    ship_current = supplier.avg_shipping_time
    if ship_current <= ship_target:
        ship_status = "compliant"
    elif ship_current <= ship_threshold:
        ship_status = "warning"
    else:
        ship_status = "breached"
    ship_deviation = round((ship_current - ship_target) / ship_target * 100, 1)

    metrics.append(SLAMetric(
        id=f"{supplier.supplier_id}-shipping_time",
        supplier_id=supplier.supplier_id,
        supplier_name=supplier.name,
        metric="shipping_time",
        current=round(ship_current, 1),
        threshold=ship_threshold,
        target=ship_target,
        unit="days",
        status=ship_status,
        deviation_percent=ship_deviation,
        trend=random.choice(["up", "down", "stable"]),
        updated_at=now,
    ))

    # Quality / defect rate SLA (lower is better)
    defect_threshold = 3.0   # % max acceptable
    defect_target = 1.0      # % ideal
    defect_current = supplier.defect_rate
    if defect_current <= defect_target:
        quality_status = "compliant"
    elif defect_current <= defect_threshold:
        quality_status = "warning"
    else:
        quality_status = "breached"
    quality_deviation = round((defect_current - defect_target) / defect_target * 100, 1)

    metrics.append(SLAMetric(
        id=f"{supplier.supplier_id}-quality_score",
        supplier_id=supplier.supplier_id,
        supplier_name=supplier.name,
        metric="quality_score",
        current=round(100 - defect_current, 1),  # convert defect rate to quality %
        threshold=100 - defect_threshold,
        target=100 - defect_target,
        unit="%",
        status=quality_status,
        deviation_percent=quality_deviation,
        trend=random.choice(["up", "down", "stable"]),
        updated_at=now,
    ))

    # Inspection pass rate SLA
    inspect_threshold = 60   # % minimum
    inspect_target = 90      # % ideal
    inspect_current = supplier.inspection_pass_rate
    if inspect_current >= inspect_target:
        inspect_status = "compliant"
    elif inspect_current >= inspect_threshold:
        inspect_status = "warning"
    else:
        inspect_status = "breached"
    inspect_deviation = round((inspect_target - inspect_current) / inspect_target * 100, 1)

    metrics.append(SLAMetric(
        id=f"{supplier.supplier_id}-inspection_rate",
        supplier_id=supplier.supplier_id,
        supplier_name=supplier.name,
        metric="inspection_rate",
        current=round(inspect_current, 1),
        threshold=inspect_threshold,
        target=inspect_target,
        unit="%",
        status=inspect_status,
        deviation_percent=inspect_deviation,
        trend=random.choice(["up", "down", "stable"]),
        updated_at=now,
    ))

    return metrics
