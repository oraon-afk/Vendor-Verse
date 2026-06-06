"""Generate alerts from actual supplier data (called after AI evaluation)."""
from datetime import datetime, timedelta
from models import Alert


def get_realistic_alerts(suppliers=None):
    """Generate alerts based on supplier performance data.
    If suppliers is None, generate generic alerts referencing supplier IDs.
    """
    alerts = []
    now = datetime.utcnow()

    if suppliers is None:
        # Fallback: empty list if no supplier data available
        return alerts

    for s in suppliers:
        # Low inspection pass rate alert
        if s.inspection_pass_rate < 50:
            severity = "Critical" if s.inspection_pass_rate < 15 else (
                "High" if s.inspection_pass_rate < 30 else "Medium"
            )
            alerts.append(Alert(
                alert_id=f"ALT-INSP-{s.supplier_id}",
                supplier_id=s.supplier_id,
                supplier_name=s.name,
                type="Quality",
                severity=severity,
                message=f"Inspection pass rate at {s.inspection_pass_rate}% — below the 80% threshold. "
                        f"Defect rate is {s.defect_rate:.2f}%.",
                timestamp=now - timedelta(hours=2),
                status="New",
            ))

        # High defect rate alert
        if s.defect_rate > 2.0:
            severity = "Critical" if s.defect_rate > 4 else "High"
            alerts.append(Alert(
                alert_id=f"ALT-DEF-{s.supplier_id}",
                supplier_id=s.supplier_id,
                supplier_name=s.name,
                type="Quality",
                severity=severity,
                message=f"Defect rate at {s.defect_rate:.2f}% — exceeds the 2% threshold. "
                        f"Avg manufacturing cost: ${s.avg_manufacturing_cost:.2f}/unit.",
                timestamp=now - timedelta(hours=3),
                status="New",
            ))

        # Long lead time alert
        if s.avg_lead_time > 18:
            alerts.append(Alert(
                alert_id=f"ALT-LEAD-{s.supplier_id}",
                supplier_id=s.supplier_id,
                supplier_name=s.name,
                type="Delivery",
                severity="High" if s.avg_lead_time > 22 else "Medium",
                message=f"Average lead time is {s.avg_lead_time:.1f} days — above the 18-day threshold. "
                        f"Shipping time avg: {s.avg_shipping_time:.1f} days.",
                timestamp=now - timedelta(hours=4),
                status="New",
            ))

        # Low OTD alert (only if AI has evaluated this)
        if s.otd_percentage is not None and s.otd_percentage < 80:
            alerts.append(Alert(
                alert_id=f"ALT-OTD-{s.supplier_id}",
                supplier_id=s.supplier_id,
                supplier_name=s.name,
                type="Delivery",
                severity="Critical" if s.otd_percentage < 70 else "High",
                message=f"On-time delivery estimated at {s.otd_percentage:.1f}% — below 80% SLA target. "
                        f"Lead time: {s.avg_lead_time:.1f} days, shipping: {s.avg_shipping_time:.1f} days.",
                timestamp=now - timedelta(hours=1),
                status="New",
            ))

        # High manufacturing cost alert
        if s.avg_manufacturing_cost > 55:
            alerts.append(Alert(
                alert_id=f"ALT-COST-{s.supplier_id}",
                supplier_id=s.supplier_id,
                supplier_name=s.name,
                type="Contract",
                severity="Medium",
                message=f"Manufacturing cost at ${s.avg_manufacturing_cost:.2f}/unit — above $55 threshold. "
                        f"Total revenue: ${s.total_revenue:,.0f}.",
                timestamp=now - timedelta(hours=6),
                status="New",
            ))

    return alerts
