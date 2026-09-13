from fastapi import APIRouter, Depends
from typing import Annotated

from src.features.user_management.resend_otp.resend_otp_handler import ResendOTPHandler
from src.features.user_management.resend_otp.resend_otp_request import ResendOtpRequest
from src.features.user_management.resend_otp.resend_otp_response import (
    ResendOTPResponse,
)
from src.features.user_management.shared.dependencies import get_resend_otp_handler

router = APIRouter()


@router.post(
    "/resend-otp",
    status_code=200,
    summary="Resend OTP to the user",
    description="Endpoint to resend the OTP to the user.",
    responses={
        200: {
            "description": "OTP resent successfully",
        },
        400: {
            "description": "Bad request",
        },
        404: {
            "description": "User not found",
        },
        500: {
            "description": "Internal server error",
        },
    },
)
async def resend_otp(
    request: ResendOtpRequest,
    handler: Annotated[ResendOTPHandler, Depends(get_resend_otp_handler)],
) -> ResendOTPResponse:
    return await handler.handle(request)
