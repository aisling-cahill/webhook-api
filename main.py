from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncpg
import os
from dotenv import load_dotenv
from typing import Optional, Dict, Any

load_dotenv()

app = FastAPI(title="Telnyx Dynamic Variables API")

class TelnyxWebhookPayload(BaseModel):
    data: Dict[str, Any]

class DynamicVariablesResponse(BaseModel):
    dynamic_variables: Dict[str, Optional[str]]

async def get_db_connection():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise HTTPException(status_code=500, detail="Database URL not configured")

    try:
        return await asyncpg.connect(database_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

@app.post("/telnyx-dynamic-vars", response_model=DynamicVariablesResponse)
async def telnyx_webhook(payload: TelnyxWebhookPayload):
    try:
        # Extract the patient phone number from the payload
        patient_phone = payload.data.get("payload", {}).get("telnyx_end_user_target")

        if not patient_phone:
            raise HTTPException(status_code=400, detail="telnyx_end_user_target not found in payload")

        # Connect to database
        conn = await get_db_connection()

        try:
            # Execute the query from your n8n workflow
            query = """
            SELECT *
            FROM public.appointments_cache
            WHERE patient_phone = $1
            ORDER BY appointment_time DESC
            LIMIT 1;
            """

            result = await conn.fetchrow(query, patient_phone)

            if not result:
                # Return empty dynamic variables if no appointment found
                return DynamicVariablesResponse(
                    dynamic_variables={
                        "acuity_id": None,
                        "patient_email": None,
                        "patient_phone": patient_phone,
                        "paid": None,
                        "appointment_time": None,
                        "first_name": None,
                        "last_name": None
                    }
                )

            # Convert result to the expected format
            return DynamicVariablesResponse(
                dynamic_variables={
                    "acuity_id": str(result.get("acuity_id", "")),
                    "patient_email": result.get("patient_email", ""),
                    "patient_phone": result.get("patient_phone", ""),
                    "paid": str(result.get("paid", "")),
                    "appointment_time": str(result.get("appointment_time", "")),
                    "first_name": result.get("first_name", ""),
                    "last_name": result.get("last_name", "")
                }
            )

        finally:
            await conn.close()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing webhook: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)