import pytest
import sys
import os

# Add apps/api to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../apps/api")))

from app.domains.finance.calculator import (
    calculate_emi,
    calculate_total_education_cost,
    calculate_funding_gap,
    EMIResult,
    CostResult
)


def test_standard_emi_calculation():
    # 1,000,000 at 8.5% for 120 months (10 years)
    result = calculate_emi(
        principal=1000000,
        annual_rate_pct=8.5,
        tenure_months=120,
        moratorium_months=0,
        processing_fee_pct=0.5
    )
    assert isinstance(result, EMIResult)
    # Expected EMI ~ 12,398.57
    assert 12390 <= result.emi <= 12410
    assert result.principal == 1000000
    assert result.processing_fee == 5000.0
    assert result.net_disbursed == 995000.0
    assert len(result.repayment_schedule) == 120
    assert result.total_repayment > result.principal
    assert abs(result.total_repayment - (result.principal + result.total_interest)) < 5.0


def test_zero_interest_emi():
    # 120,000 at 0% for 12 months -> exactly 10,000 / month
    result = calculate_emi(
        principal=120000,
        annual_rate_pct=0.0,
        tenure_months=12,
        moratorium_months=0,
        processing_fee_pct=0.0
    )
    assert result.emi == 10000.0
    assert result.total_repayment == 120000.0
    assert result.total_interest == 0.0


def test_moratorium_period():
    # 500,000 at 10% for 24 months with 6 months moratorium
    result = calculate_emi(
        principal=500000,
        annual_rate_pct=10.0,
        tenure_months=24,
        moratorium_months=6,
        processing_fee_pct=1.0
    )
    assert len(result.repayment_schedule) == 24
    # First 6 months should have 0 principal repayment (interest only)
    for m in range(6):
        assert result.repayment_schedule[m].principal_component == 0.0
        assert result.repayment_schedule[m].interest_component > 0


def test_invalid_loan_inputs():
    with pytest.raises(ValueError, match="Principal must be positive"):
        calculate_emi(principal=0, annual_rate_pct=5.0, tenure_months=12)

    with pytest.raises(ValueError, match="Interest rate cannot be negative"):
        calculate_emi(principal=100000, annual_rate_pct=-1.0, tenure_months=12)

    with pytest.raises(ValueError, match="Tenure must be positive"):
        calculate_emi(principal=100000, annual_rate_pct=5.0, tenure_months=0)


def test_education_cost_calculator():
    cost = calculate_total_education_cost(
        tuition_per_year=150000,
        accommodation_per_year=80000,
        food_per_year=40000,
        transport_per_year=10000,
        books_per_year=15000,
        insurance_per_year=5000,
        application_fees=2000,
        visa_costs=5000,
        other_per_year=10000,
        duration_years=4.0,
        currency="INR"
    )
    assert isinstance(cost, CostResult)
    expected_annual = 150000 + 80000 + 40000 + 10000 + 15000 + 5000 + 10000
    assert cost.annual_total == expected_annual
    expected_total = (expected_annual * 4.0) + 2000 + 5000
    assert cost.program_total == expected_total


def test_funding_gap_analysis():
    analysis = calculate_funding_gap(
        total_cost=1000000,
        family_contribution=300000,
        savings=100000,
        scholarship_amount=200000,
        loan_amount=300000
    )
    assert analysis["total_cost"] == 1000000.0
    assert analysis["total_funding"] == 900000.0
    assert analysis["funding_gap"] == 100000.0
    assert analysis["funding_coverage_pct"] == 90.0
