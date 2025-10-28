from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch
import logging

logger = logging.getLogger(__name__)

class ClinicalNoteGenerator:
    def __init__(self, model_name="distilgpt2"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Loading model '{model_name}' on {self.device}...")

        try:
            # Load tokenizer and model
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            # Add padding token if it doesn't exist (common for GPT-2 models)
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token

            self.model = AutoModelForCausalLM.from_pretrained(model_name).to(self.device)

            # Initialize the text generation pipeline
            self.generator = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                max_new_tokens=200,      # Limit output length for demo
                temperature=0.8,         # Creativity: 0.7-0.9 is often good
                top_p=0.9,              # Nucleus sampling
                do_sample=True,         # Enable sampling
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
                truncation=True,
                # return_full_text=False # Only return generated part (sometimes causes issues)
            )
            logger.info("Model and pipeline loaded successfully.")

        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise e

    def generate_note(self, summary: dict) -> str:
        # Construct the prompt from the structured summary
        prompt = f"""
        Patient Summary:
        Age: {summary['age']}
        Gender: {summary['gender']}
        Pain Intensity (1-10): {summary['pain_intensity']}
        Hemoglobin (g/dL): {summary['hemoglobin']}
        Oxygen Saturation (%): {summary['oxygen_saturation']}
        Pain Type: {summary['pain_type']}
        Facility Type: {summary['facility_type']}
        Location: {summary['location']}
        Admitted: {summary['admitted']}

        Clinical Note:
        """.strip()

        try:
            # Generate text using the pipeline
            result = self.generator(
                prompt,
                max_new_tokens=200,
                temperature=0.8,
                top_p=0.9,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
                truncation=True,
                return_full_text=False # Important: Only get the generated part
            )

            # Extract the generated text part
            generated_text = result[0]['generated_text']
            # Post-process: remove prompt if it's included (some pipelines do)
            note = generated_text.replace(prompt, "", 1).strip()
            return note

        except Exception as e:
            logger.error(f"Generation failed: {e}")
            return f"Error generating note: {str(e)}"