from fastapi import FastAPI


app = FastAPI(
title="Pincode lookup FastAPI",
description="This is a simple API to lookup pincode information.",
version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Welcome to the Pincode Lookup API"}


@app.get("/pincode/{pincode}", tags=["Pincode Lookup"], summary="Get information for a specific pincode", description="This endpoint retrieves information for a given pincode.")
def get_pincode_info(pincode: str):
    # Here you would implement the logic to look up the pincode information.
    # For demonstration purposes, we'll return a mock response.
    mock_response = {
        "pincode": pincode,
        "city": "Sample City",
        "state": "Sample State",
        "country": "Sample Country"
    }
    return mock_response