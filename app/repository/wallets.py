from decimal import Decimal
from uuid import UUID

from fastapi import Depends
from asyncpg import Connection, Record, CheckViolationError

from app.dependency.db import get_connection
from app.repository.exeptions import WalletNotFoundException, WalletAmountException


class WalletRepository:
    def __init__(self, conn: Connection = Depends(get_connection)):
        self._conn = conn

    async def get_wallets_amount(self, wallet_uid: UUID) -> Decimal:
        query = '''
            SELECT amount 
            FROM wallets
            WHERE uid = $1
        '''

        data = await self._conn.fetchval(query, wallet_uid)

        if data is None:
            raise WalletNotFoundException()

        return data

    async def set_wallets_amount(self, wallet_uid: UUID, amount: Decimal) -> Record:
        query = '''
            UPDATE wallets
            SET amount = amount + $2
            WHERE uid = $1
            RETURNING amount
        '''

        try:
            data = await self._conn.fetchrow(query, wallet_uid, amount)
        except CheckViolationError as exc:
            match exc.constraint_name:
                case "wallet_amount_check":
                    raise WalletAmountException()
            raise

        if data is None:
            raise WalletNotFoundException()

        return data
