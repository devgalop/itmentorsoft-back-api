from pydantic import BaseModel


class ResendOTPResponse(BaseModel):
    message: str
