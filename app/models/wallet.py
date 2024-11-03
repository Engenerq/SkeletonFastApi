from fastapi import Path
from pydantic import BaseModel, condecimal, Field, UUID4
from typing import Annotated

from app.const.wallet import WalletTypeOperation


class GetWalletAmountRequest(BaseModel):
    wallet_uuid: Annotated[UUID4, Path(..., description="Wallet UUID")]


class GetWalletAmountResponse(BaseModel):
    amount: condecimal(ge=0)


class WalletOperationsRequest(BaseModel):
    wallet_uuid: UUID4 | None = None
    operation_type: WalletTypeOperation = Field(..., alias='operationType')
    amount: condecimal(gt=0)


class WalletOperationsResponse(BaseModel):
    success: bool = True
    amount: condecimal(ge=0)
