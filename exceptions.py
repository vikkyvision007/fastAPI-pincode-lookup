from fastapi.responses import JSONResponse
from fastapi.requests import Request

# Custome Error for Pincode Lookup API
class PincodeNotFoundError(Exception):
    def __init__(self, pincode: str):
        self.pincode = pincode


class PincodeInvalidError(Exception):
    def __init__(self, pincode: str, reason: str = "Invalid pincode format"):
        self.pincode = pincode
        self.reason = reason 

# custome exception handler for Pincode Lookup API
async def pincode_not_found_handler(request: Request, exc: PincodeNotFoundError):
    return JSONResponse(
        status_code = 404,
        content = {
            "error" : "Pincode not found",
            "message" : f"Provided pincode '{exc.pincode}' is not found in the database",
            "pincode" : exc.pincode
        }
    )

async def pincode_invalid_handler( request: Request, exc: PincodeInvalidError):
    return JSONResponse(
        status_code = 400,
        content = {
            "error" : "Invalid pincode",
            "message" : f"Provided pincode '{exc.pincode}' is invalid. Reason: {exc.reason}",
            "pincode" : exc.pincode
        }
    )