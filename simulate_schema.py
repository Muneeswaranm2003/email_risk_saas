from pydantic import BaseModel, Field

class SimulateRequest(BaseModel):
    domain: str = Field(
        ...,
        example="example.com",
        description="Sender domain to evaluate"
    )

    planned_volume: int = Field(
        ...,
        example=5000,
        description="Planned number of emails to send"
    )

    avg_volume: int = Field(
        default=500,
        example=500,
        description="Average daily sending volume (optional)"
    )
