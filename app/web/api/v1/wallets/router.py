from typing import Annotated

from fastapi import APIRouter, Depends, Path, HTTPException, status
from pydantic import UUID4

from app.models.wallet import (
    GetWalletAmountRequest,
    GetWalletAmountResponse,
    WalletOperationsRequest,
    WalletOperationsResponse,
)
from app.repository.exeptions import WalletNotFoundException, WalletAmountException
from app.services.wallets import WalletsService

router = APIRouter(
    prefix="/wallets",
    tags=["wallets"],
)


@router.get(
    path='/{wallet_uuid}',
    response_model=GetWalletAmountResponse,
)
async def get_wallet_amount(
    data: GetWalletAmountRequest = Depends(),
    service: WalletsService = Depends(WalletsService),
):
    """
    Получает баланс кошелька
    """

    try:
        return await service.get_wallet_amount(data)
    except WalletNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found",
        ) from exc

@router.post(
    path='/{wallet_uuid}/operation',
    response_model=WalletOperationsResponse,
)
async def wallet_operations(
    wallet_uuid: Annotated[UUID4, Path(..., description="Wallet UUID")],
    data: WalletOperationsRequest,
    service: WalletsService = Depends(WalletsService),
):
    """
    Операции над кошельком
    """
    data.wallet_uuid = wallet_uuid

    try:
        return await service.set_wallet_amount(data)
    except WalletAmountException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Not enough amount"
        ) from exc
    except WalletNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found"
        ) from exc

