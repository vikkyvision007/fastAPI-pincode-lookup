from fastapi import FastAPI
from pydantic.config import JsonEncoder
from exceptions import PincodeNotFoundError, PincodeInvalidError, pincode_not_found_handler, pincode_invalid_handler
from models import PincodeRequest, PincodeResponse, BulkRequest, BulkResponse
from data import pincode_db


app = FastAPI(
title="Pincode lookup FastAPI",
description="This is a simple API to lookup pincode information.",
version="1.0.0"
)

#register custome exception handler
app.add_exception_handler(PincodeNotFoundError, pincode_not_found_handler)
app.add_exception_handler(PincodeInvalidError, pincode_invalid_handler)

@app.get("/")
def root():
    return {"message": "Welcome to the Pincode Lookup API"}


@app.get("/pincode/{code}", tags=["Pincode Lookup"], response_model=PincodeResponse, summary="Get information for a specific pincode", description="This endpoint retrieves information for a given pincode.")
def lookup_pincode(code: str):
    # Case 1: If the pincode is invalid (not a 6-digit number), raise PincodeInvalidError
    if len(code) != 6 or not code.isdigit():
        raise PincodeInvalidError(pincode=code, reason="Pincode must be exactly six digits")
    # Case 2: If the pincode is not found in the database, raise PincodeNotFoundError
    if code not in pincode_db:
        raise PincodeNotFoundError(pincode=code)
    # Case 3: If the pincode is found, return the corresponding information as a PincodeResponse object.
    return PincodeResponse(**pincode_db[code])
    

@app.post("/pincode/bulk", response_model=BulkResponse, tags=["Pincode Lookup"], summary="Get information for multiple pincodes", description="This endpoint retrieves information for multiple pincodes in a single request.")
def bulk_lookup_pincodes(request: BulkRequest):
    results = []
    missing = []

    for code in request.pincodes:
        if len(code) != 6 or not code.isdigit():
            raise PincodeInvalidError(pincode=code, reason="Pincode must be exactly six digits")
        if code in pincode_db:
            results.append(pincode_db[code])
        else:
            missing.append(code)

    return BulkResponse(
        found=len(results),
        not_found=len(missing),
        results=results,
        missing=missing
    )