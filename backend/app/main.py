from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from .model import ClinicalNoteGenerator
from .schema import PatientSummary, MedicalReportResponse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="MedReportGen AI - Sickle Cell Demo")

# --- CORS Middleware (Adjust origins for production) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Load Model (This happens once on startup) ---
logger.info("Initializing Clinical Note Generator...")
try:
    generator = ClinicalNoteGenerator(model_name="distilgpt2")
    logger.info("Generator initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize generator: {e}")
    raise e

@app.post("/generate", response_model=MedicalReportResponse)
async def generate_note_endpoint(summary: PatientSummary):
    try:
        # Convert Pydantic model to dict for the generator
        summary_dict = summary.dict()

        # Generate the clinical note using the model
        generated_text = generator.generate_note(summary_dict)

        # Simple confidence scoring (placeholder)
        confidence = 0.78 # Placeholder - in a real system, this would come from model logits or eval

        # Generate warnings based on input (simple logic)
        warnings = []
        if summary.pain_intensity > 7:
            warnings.append("High pain intensity reported.")
        if summary.hemoglobin < 7.0:
            warnings.append("Critically low hemoglobin level.")
        if summary.oxygen_saturation < 92:
            warnings.append("Low oxygen saturation - potential hypoxia.")
        if summary.admitted.lower() == "yes":
            warnings.append("Patient was admitted - consider severity.")

        # Return the response
        return MedicalReportResponse(
            generated_note=generated_text,
            confidence_score=confidence,
            warnings=warnings
        )

    except ValidationError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception as e:
        logger.error(f"Unexpected error in generate_note_endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/")
def root():
    return {"message": "MedReportGen AI Backend (Sickle Cell) is running. POST /generate"}

# Optional: Endpoint to check model loading status
@app.get("/health")
def health_check():
    return {"status": "ok", "model_loaded": generator is not None}