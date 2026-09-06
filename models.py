from pydantic import BaseModel, field_validator


class PincodeRequest(BaseModel):
    pincode: str

    #pincode must be exactly six digits
    @field_validator('pincode')
    @classmethod
    def validate_pincode(cls, v):
        if not v.isdigit() or len(v) != 6:
            raise ValueError("Pincode must be exactly six digits")
        return v


class PincodeResponse(BaseModel):
    pincode: str
    city: str
    state: str
    district: str   

class BulkRequest(BaseModel):
    pincodes: list[str]

    @field_validator('pincodes')
    @classmethod
    def validate_pincodes(cls, pincodes):
        if len(pincodes) == 0:
            raise ValueError("Pincodes list cannot be empty")
        if len(pincodes) > 10:
            raise ValueError("Pincodes list cannot contain more than 10 pincodes")        
        for pincode in pincodes:
            if not pincode.isdigit() or len(pincode) != 6:
                raise ValueError(f"Each Pincode '{pincode}' must be exactly six digits")
        return pincodes

class BulkResponse(BaseModel):
    status: str = "Success"
    found: int
    not_found: int
    results: list[PincodeResponse]


