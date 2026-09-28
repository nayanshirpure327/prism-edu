from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.domains.finance.calculator import calculate_emi, calculate_total_education_cost, calculate_funding_gap

router = APIRouter()


# ── Schemas ───────────────────────────────────────────────────
class EMIRequest(BaseModel):
    principal: float = Field(..., gt=0, description="Loan amount")
    annual_rate_pct: float = Field(..., ge=0, le=50, description="Annual interest rate %")
    tenure_months: int = Field(..., gt=0, le=360, description="Repayment tenure in months")
    moratorium_months: int = Field(0, ge=0, description="Grace/moratorium period in months")
    processing_fee_pct: float = Field(0.0, ge=0, le=10, description="Processing fee %")


class CostEstimateRequest(BaseModel):
    tuition_per_year: float = Field(0, ge=0)
    accommodation_per_year: float = Field(0, ge=0)
    food_per_year: float = Field(0, ge=0)
    transport_per_year: float = Field(0, ge=0)
    books_per_year: float = Field(0, ge=0)
    insurance_per_year: float = Field(0, ge=0)
    application_fees: float = Field(0, ge=0)
    visa_costs: float = Field(0, ge=0)
    other_per_year: float = Field(0, ge=0)
    duration_years: float = Field(4.0, gt=0, le=10)
    currency: str = Field("INR")
    family_contribution: float = Field(0, ge=0)
    savings: float = Field(0, ge=0)
    scholarship_amount: float = Field(0, ge=0)
    loan_amount: float = Field(0, ge=0)


# ── Endpoints ────────────────────────────────────────────────

@router.get("/products")
async def list_loan_products(
    country: Optional[str] = None,
    loan_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_active_user),
):
    """List available loan products. Data labeled by verification status."""
    from app.models.education import LoanProduct
    query = select(LoanProduct).where(LoanProduct.is_active == True)
    result = await db.execute(query)
    products = result.scalars().all()
    return {
        "data": [
            {
                "id": str(p.id),
                "name": p.name,
                "provider": p.provider,
                "loan_type": p.loan_type,
                "min_amount": p.min_amount,
                "max_amount": p.max_amount,
                "currency": p.currency,
                "interest_rate_min": p.interest_rate_min,
                "interest_rate_max": p.interest_rate_max,
                "rate_type": p.rate_type,
                "max_tenure_months": p.max_tenure_months,
                "moratorium_months": p.moratorium_months,
                "processing_fee_pct": p.processing_fee_pct,
                "collateral_required": p.collateral_required,
                "co_borrower_required": p.co_borrower_required,
                "description": p.description,
                "application_url": p.application_url,
                "data_status": p.data_status.value if p.data_status else "NEEDS_VERIFICATION",
                "data_notice": "⚠️ Sample data. Verify with lender before decisions.",
            }
            for p in products
        ]
    }


@router.post("/calculate")
async def calculate_emi_endpoint(
    req: EMIRequest,
):
    """
    Calculate EMI using standard reducing-balance formula.
    Returns full repayment schedule.
    This is an ESTIMATE — actual lender terms may differ.
    """
    result = calculate_emi(
        principal=req.principal,
        annual_rate_pct=req.annual_rate_pct,
        tenure_months=req.tenure_months,
        moratorium_months=req.moratorium_months,
        processing_fee_pct=req.processing_fee_pct,
    )
    return {
        "principal": result.principal,
        "annual_rate_pct": result.annual_rate_pct,
        "tenure_months": result.tenure_months,
        "moratorium_months": result.moratorium_months,
        "emi": result.emi,
        "total_repayment": result.total_repayment,
        "total_interest": result.total_interest,
        "processing_fee": result.processing_fee,
        "net_disbursed": result.net_disbursed,
        "repayment_schedule": [
            {
                "month": p.month,
                "payment": p.payment,
                "principal_component": p.principal_component,
                "interest_component": p.interest_component,
                "remaining_balance": p.remaining_balance,
            }
            for p in result.repayment_schedule
        ],
        "disclaimer": result.disclaimer,
    }


@router.post("/cost-estimate")
async def cost_estimate_endpoint(
    req: CostEstimateRequest,
):
    """Estimate total education cost and funding gap."""
    cost = calculate_total_education_cost(
        tuition_per_year=req.tuition_per_year,
        accommodation_per_year=req.accommodation_per_year,
        food_per_year=req.food_per_year,
        transport_per_year=req.transport_per_year,
        books_per_year=req.books_per_year,
        insurance_per_year=req.insurance_per_year,
        application_fees=req.application_fees,
        visa_costs=req.visa_costs,
        other_per_year=req.other_per_year,
        duration_years=req.duration_years,
        currency=req.currency,
    )
    funding = calculate_funding_gap(
        total_cost=cost.program_total,
        family_contribution=req.family_contribution,
        savings=req.savings,
        scholarship_amount=req.scholarship_amount,
        loan_amount=req.loan_amount,
    )
    return {
        "cost_breakdown": {
            "tuition_total": cost.tuition_total,
            "accommodation_total": cost.accommodation_total,
            "food_total": cost.food_total,
            "transport_total": cost.transport_total,
            "books_total": cost.books_total,
            "insurance_total": cost.insurance_total,
            "application_fees": cost.application_fees,
            "visa_costs": cost.visa_costs,
            "other_total": cost.other_total,
            "annual_total": cost.annual_total,
            "program_total": cost.program_total,
            "currency": cost.currency,
            "duration_years": cost.duration_years,
        },
        "funding_analysis": funding,
        "disclaimer": cost.disclaimer,
    }
