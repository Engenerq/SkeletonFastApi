from fastapi import Depends
from app.repository.wallets import WalletRepository
from app.models.wallet import (
    GetWalletAmountRequest,
    GetWalletAmountResponse,
    WalletOperationsRequest,
    WalletOperationsResponse,
)
from app.const.wallet import WalletTypeOperation


class WalletsService:
    def __init__(self, wallet_repository: WalletRepository = Depends(WalletRepository)):
        self._wallet_repository = wallet_repository

    async def get_wallet_amount(self, params: GetWalletAmountRequest) -> GetWalletAmountResponse:

        amount = await self._wallet_repository.get_wallets_amount(params.wallet_uuid)

        return GetWalletAmountResponse(amount=amount)

    async def set_wallet_amount(self, params: WalletOperationsRequest) -> WalletOperationsResponse:

        match params.operation_type:
            case WalletTypeOperation.DEPOSIT:
                operation = self._wallet_repository.set_wallets_amount(params.wallet_uuid, params.amount)
            case WalletTypeOperation.WITHDRAW:
                operation = self._wallet_repository.set_wallets_amount(params.wallet_uuid, -params.amount)
            case _:
                raise ValueError("Неизвестный тип операции")

        return WalletOperationsResponse(
            **dict(await operation)
        )
