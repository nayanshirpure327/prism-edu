"""
PRISM-EDU Deterministic Financial Calculator
All formulas are mathematically correct and unit-testable.
These calculations are ESTIMATES and must never claim to be actual lender terms.
"""
from dataclasses import dataclass, field
from typing import List
import math


@dataclass
class MonthlyPayment:
    month: int
    payment: float
    principal_component: float
    interest_component: float
    remaining_balance: float


@dataclass
class EMIResult:
    principal: float
    annual_rate_pct: float
    tenure_months: int
    moratorium_months: int
    emi: float
    total_repayment: float
    total_interest: float
    processing_fee: float
    net_disbursed: float
    repayment_schedule: List[MonthlyPayment] = field(default_factory=list)
    disclaimer: str = (
        "This is a mathematical estimate only. "
        "Actual terms, EMI, and interest charged by the lender may differ. "
        "Contact the lender for official terms before making financial decisions."
    )


@dataclass
class CostResult:
    tuition_total: float
    accommodation_total: float
    food_total: float
    transport_total: float
    books_total: float
    insurance_total: float
    application_fees: float
    visa_costs: float
    other_total: float
    annual_total: float
    program_total: float
    currency: str
    duration_years: float
    disclaimer: str = (
        "Cost estimates are based on available data and may not reflect actual costs. "
        "Verify all figures with the institution and official sources."
    )


def calculate_emi(
    principal: float,
    annual_rate_pct: float,
    tenure_months: int,
    moratorium_months: int = 0,
    processing_fee_pct: float = 0.0,
) -> EMIResult:
    """
    Calculate loan EMI using the standard reducing-balance formula.

    Formula: EMI = P × r × (1+r)^n / ((1+r)^n - 1)
    where:
        P = principal
        r = monthly interest rate = annual_rate_pct / 12 / 100
        n = repayment tenure in months (excluding moratorium)

    Args:
        principal: Loan amount in currency units
        annual_rate_pct: Annual interest rate as percentage (e.g., 8.5 for 8.5%)
        tenure_months: Total repayment tenure in months
        moratorium_months: Grace period where only interest accrues (no principal)
        processing_fee_pct: Processing fee as percentage of principal

    Returns:
        EMIResult with full repayment schedule
    """
    if principal <= 0:
        raise ValueError("Principal must be positive.")
    if annual_rate_pct < 0:
        raise ValueError("Interest rate cannot be negative.")
    if tenure_months <= 0:
        raise ValueError("Tenure must be positive.")

    processing_fee = round(principal * processing_fee_pct / 100, 2)
    net_disbursed = principal - processing_fee

    monthly_rate = annual_rate_pct / 12 / 100
    repayment_tenure = tenure_months - moratorium_months

    if monthly_rate == 0:
        emi = principal / max(repayment_tenure, 1)
    else:
        emi = principal * monthly_rate * (1 + monthly_rate) ** repayment_tenure / (
            (1 + monthly_rate) ** repayment_tenure - 1
        )

    emi = round(emi, 2)

    # Build repayment schedule
    schedule: List[MonthlyPayment] = []
    balance = principal

    # Moratorium months — interest only
    for month in range(1, moratorium_months + 1):
        interest = round(balance * monthly_rate, 2)
        schedule.append(MonthlyPayment(
            month=month,
            payment=interest,
            principal_component=0.0,
            interest_component=interest,
            remaining_balance=round(balance, 2),
        ))

    # Repayment months — EMI splits into principal + interest
    for month in range(moratorium_months + 1, tenure_months + 1):
        interest = round(balance * monthly_rate, 2)
        principal_paid = round(min(emi - interest, balance), 2)
        balance = round(balance - principal_paid, 2)
        if balance < 0:
            balance = 0.0

        schedule.append(MonthlyPayment(
            month=month,
            payment=emi if balance > 0 else principal_paid + interest,
            principal_component=principal_paid,
            interest_component=interest,
            remaining_balance=balance,
        ))

    total_repayment = round(sum(p.payment for p in schedule), 2)
    total_interest = round(total_repayment - principal, 2)

    return EMIResult(
        principal=principal,
        annual_rate_pct=annual_rate_pct,
        tenure_months=tenure_months,
        moratorium_months=moratorium_months,
        emi=emi,
        total_repayment=total_repayment,
        total_interest=max(total_interest, 0),
        processing_fee=processing_fee,
        net_disbursed=net_disbursed,
        repayment_schedule=schedule,
    )


def calculate_total_education_cost(
    tuition_per_year: float,
    accommodation_per_year: float = 0,
    food_per_year: float = 0,
    transport_per_year: float = 0,
    books_per_year: float = 0,
    insurance_per_year: float = 0,
    application_fees: float = 0,
    visa_costs: float = 0,
    other_per_year: float = 0,
    duration_years: float = 4.0,
    currency: str = "USD",
) -> CostResult:
    """
    Calculate total education cost across all components.

    All inputs in the same currency. Returns annual and total costs.
    Uses ranges conceptually — exact figures should be verified with institutions.
    """
    if duration_years <= 0:
        raise ValueError("Duration must be positive.")

    annual_total = (
        tuition_per_year
        + accommodation_per_year
        + food_per_year
        + transport_per_year
        + books_per_year
        + insurance_per_year
        + other_per_year
    )

    # One-time costs added once
    program_total = round(annual_total * duration_years + application_fees + visa_costs, 2)

    return CostResult(
        tuition_total=round(tuition_per_year * duration_years, 2),
        accommodation_total=round(accommodation_per_year * duration_years, 2),
        food_total=round(food_per_year * duration_years, 2),
        transport_total=round(transport_per_year * duration_years, 2),
        books_total=round(books_per_year * duration_years, 2),
        insurance_total=round(insurance_per_year * duration_years, 2),
        application_fees=round(application_fees, 2),
        visa_costs=round(visa_costs, 2),
        other_total=round(other_per_year * duration_years, 2),
        annual_total=round(annual_total, 2),
        program_total=program_total,
        currency=currency,
        duration_years=duration_years,
    )


def calculate_funding_gap(
    total_cost: float,
    family_contribution: float = 0,
    savings: float = 0,
    scholarship_amount: float = 0,
    loan_amount: float = 0,
) -> dict:
    """Calculate remaining funding gap after all sources."""
    total_funding = family_contribution + savings + scholarship_amount + loan_amount
    gap = max(total_cost - total_funding, 0)
    return {
        "total_cost": round(total_cost, 2),
        "total_funding": round(total_funding, 2),
        "funding_gap": round(gap, 2),
        "funding_coverage_pct": round(min(total_funding / total_cost * 100, 100), 1) if total_cost > 0 else 0,
        "sources": {
            "family_contribution": family_contribution,
            "savings": savings,
            "scholarship_amount": scholarship_amount,
            "loan_amount": loan_amount,
        },
    }
