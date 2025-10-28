from pydantic import BaseModel
from typing import Optional

class PatientSummary(BaseModel):
    pain_intensity: int  # Numeric pain rating from 1 to 10
    hemoglobin: float    # Lab result (g/dL)
    oxygen_saturation: float # Patient oxygen level (%)
    pain_type: str       # e.g., 'legs', 'chest', 'abdomen'
    facility_type: str   # e.g., 'ER', 'Urgent Care', 'Outpatient'
    location: str        # e.g., 'Bronx', 'Brooklyn'
    admitted: str        # 'Yes' or 'No'
    # Optional: You could add age/gender if derivable or added as defaults
    age: Optional[int] = 30 # Default age for demo
    gender: Optional[str] = "Male" # Default gender for demo

class MedicalReportResponse(BaseModel):
    generated_note: str
    confidence_score: float # Placeholder for now
    warnings: list[str]