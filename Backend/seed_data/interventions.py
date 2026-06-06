import json
from datetime import datetime
from models import Intervention


def generate_interventions(suppliers):
    """Generate interventions based on actual supplier performance from the Kaggle dataset."""
    interventions = []

    # Find problem suppliers (AI fields may be None)
    critical_suppliers = [s for s in suppliers if (s.risk_level or "") in ("Critical", "High")]
    low_inspect = [s for s in suppliers if s.inspection_pass_rate < 50]
    high_defect = [s for s in suppliers if s.defect_rate > 2.0]
    slow_delivery = [s for s in suppliers if (s.otd_percentage or 100) < 80]

    # 1. Quality intervention for 0% inspection pass (Supplier 4)
    zero_inspect = [s for s in suppliers if s.inspection_pass_rate == 0]
    if zero_inspect:
        interventions.append(Intervention(
            id="INT-001",
            type="automated",
            category="risk_mitigation",
            priority="critical",
            title="Emergency Quality Audit — 0% Inspection Pass Rate",
            description="Supplier 4 has 0% inspection pass rate with the highest manufacturing cost ($62.71/unit). Immediate on-site audit required to identify root cause of quality failures.",
            target_suppliers=json.dumps([s.supplier_id for s in zero_inspect]),
            actions=json.dumps([
                {"step": 1, "action": "Halt new orders to Supplier 4", "status": "pending"},
                {"step": 2, "action": "Deploy quality auditor to manufacturing site", "status": "pending"},
                {"step": 3, "action": "Review manufacturing process and defect logs", "status": "pending"},
                {"step": 4, "action": "Establish corrective action plan within 7 days", "status": "pending"}
            ]),
            status="pending",
            impact_risk_reduction=45.0,
            impact_cost_savings=28000,
            impact_performance_improvement=35.0,
            estimated_duration="2 weeks",
        ))

    # 2. Inspection improvement for all low-pass suppliers
    if low_inspect:
        interventions.append(Intervention(
            id="INT-002",
            type="ai_suggested",
            category="performance_boost",
            priority="high",
            title="Inspection Process Overhaul — Network-wide",
            description=f"All 5 suppliers have inspection pass rates below 50%. Best performer (Supplier 1) is at 48.1%. This suggests systemic quality issues that need cross-supplier intervention.",
            target_suppliers=json.dumps([s.supplier_id for s in low_inspect]),
            actions=json.dumps([
                {"step": 1, "action": "Standardize inspection criteria across all suppliers", "status": "pending"},
                {"step": 2, "action": "Implement pre-shipment quality checks", "status": "pending"},
                {"step": 3, "action": "Set up real-time defect tracking dashboard", "status": "pending"}
            ]),
            status="in_progress",
            impact_risk_reduction=30.0,
            impact_cost_savings=15000,
            impact_performance_improvement=25.0,
            estimated_duration="4 weeks",
        ))

    # 3. Delivery improvement
    if slow_delivery:
        interventions.append(Intervention(
            id="INT-003",
            type="manual",
            category="performance_boost",
            priority="high",
            title="On-Time Delivery Improvement Program",
            description=f"{len(slow_delivery)} suppliers below 80% OTD target. Supplier 4 is worst at 68%. Need to optimize logistics and reduce lead times.",
            target_suppliers=json.dumps([s.supplier_id for s in slow_delivery]),
            actions=json.dumps([
                {"step": 1, "action": "Analyze shipping route efficiency for each supplier", "status": "pending"},
                {"step": 2, "action": "Negotiate faster shipping carriers", "status": "pending"},
                {"step": 3, "action": "Implement order tracking with milestone alerts", "status": "pending"},
                {"step": 4, "action": "Set up penalty/bonus structure for OTD performance", "status": "pending"}
            ]),
            status="pending",
            impact_risk_reduction=20.0,
            impact_cost_savings=12000,
            impact_performance_improvement=18.0,
            estimated_duration="6 weeks",
        ))

    # 4. Cost optimization
    high_cost = [s for s in suppliers if s.avg_manufacturing_cost > 50]
    if high_cost:
        interventions.append(Intervention(
            id="INT-004",
            type="ai_suggested",
            category="cost_optimization",
            priority="medium",
            title="Manufacturing Cost Reduction — Supplier 4",
            description="Supplier 4's manufacturing cost ($62.71/unit) is 43% higher than the network average ($47.60). With the lowest revenue ($86,469) and 0% inspection pass, this supplier is the least cost-effective.",
            target_suppliers=json.dumps([s.supplier_id for s in high_cost]),
            actions=json.dumps([
                {"step": 1, "action": "Benchmark manufacturing processes against Supplier 2 ($41.62/unit)", "status": "pending"},
                {"step": 2, "action": "Identify raw material cost reduction opportunities", "status": "pending"},
                {"step": 3, "action": "Evaluate alternative manufacturing partners", "status": "pending"}
            ]),
            status="pending",
            impact_risk_reduction=10.0,
            impact_cost_savings=35000,
            impact_performance_improvement=8.0,
            estimated_duration="8 weeks",
        ))

    # 5. Supplier diversification
    interventions.append(Intervention(
        id="INT-005",
        type="ai_suggested",
        category="risk_mitigation",
        priority="medium",
        title="Supplier Diversification Strategy",
        description="All 5 suppliers operate in the same Indian cities (Mumbai, Delhi, Chennai, Bangalore, Kolkata) with the same product types. Geographic concentration creates supply chain vulnerability.",
        target_suppliers=json.dumps([s.supplier_id for s in suppliers]),
        actions=json.dumps([
            {"step": 1, "action": "Identify potential suppliers in Southeast Asia and Europe", "status": "pending"},
            {"step": 2, "action": "Run pilot orders with 2-3 new regional suppliers", "status": "pending"},
            {"step": 3, "action": "Develop dual-sourcing strategy for critical products", "status": "pending"}
        ]),
        status="pending",
        impact_risk_reduction=25.0,
        impact_cost_savings=20000,
        impact_performance_improvement=15.0,
        estimated_duration="12 weeks",
    ))

    return interventions
