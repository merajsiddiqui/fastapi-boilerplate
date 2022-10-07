from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from api.middlewares.auth import JWTBearer
from services.user import *
from schema.user import *
from services.mobile_sms import MobileSMS
from api.responses.response import ApiResponse
from api.responses.user import *

router = APIRouter(prefix = '/user', dependencies = [Depends(JWTBearer())], tags = ['User'])
sms = MobileSMS()


@router.get('/profile', response_model = ApiResponse[UserModel])
async def profile(Authorize: AuthJWT = Depends()):
    user = get_user_by_id(Authorize.get_jwt_subject())
    return ApiResponse[UserModel](data = user, message = "Profile fetched successfully")


@router.post('/mobile/otp/request', response_model = ApiResponse)
async def otp_mobile_number(mobile_details: UserMobileVerificationRequest):
    sms.send_otp(mobile_details.mobile_number)
    return ApiResponse(message = "You will receive an otp shortly")


@router.post('/mobile/otp/verify', response_model = ApiResponse)
async def verify_mobile_number(otp_details: VerifyUserMobileNumber):
    sms.validate_otp(mobile_number = otp_details.mobile_number, otp = otp_details.otp)
    mark_mobile_number_verified(otp_details.mobile_number)
    return ApiResponse(message = "Congrats, your mobile number has been verified")
