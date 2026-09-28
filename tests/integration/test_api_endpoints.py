import pytest
import sys
import os
from fastapi.testclient import TestClient

# Add apps/api to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../apps/api")))

from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "prism-edu-api"


def test_loan_emi_calculation_api():
    payload = {
        "principal": 500000,
        "annual_rate_pct": 9.5,
        "tenure_months": 60,
        "moratorium_months": 0,
        "processing_fee_pct": 1.0
    }
    response = client.post("/api/v1/loans/calculate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "emi" in data
    assert data["emi"] > 0
    assert data["principal"] == 500000
    assert data["processing_fee"] == 5000.0
    assert len(data["repayment_schedule"]) == 60
    assert "disclaimer" in data


def test_cost_estimate_api():
    payload = {
        "tuition_per_year": 120000,
        "accommodation_per_year": 60000,
        "food_per_year": 30000,
        "transport_per_year": 10000,
        "books_per_year": 10000,
        "insurance_per_year": 5000,
        "application_fees": 1500,
        "visa_costs": 0,
        "other_per_year": 5000,
        "duration_years": 4.0,
        "currency": "INR",
        "family_contribution": 200000,
        "savings": 50000,
        "scholarship_amount": 100000,
        "loan_amount": 400000
    }
    response = client.post("/api/v1/loans/cost-estimate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "cost_breakdown" in data
    assert "funding_analysis" in data
    assert data["cost_breakdown"]["program_total"] > 0
    assert data["funding_analysis"]["funding_gap"] >= 0


def test_careers_list_api():
    response = client.get("/api/v1/careers/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, (list, dict))


def test_decision_matrix_endpoint():
    response = client.get("/api/v1/decision-matrix/")
    assert response.status_code == 200
