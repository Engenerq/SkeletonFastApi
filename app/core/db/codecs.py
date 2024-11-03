from decimal import Decimal

from asyncpg import Connection


def _encoder_numeric(value: Decimal | None) -> str | None:
    if value is None:
        return value

    return str(value)


def _decoder_numeric(value: str | None) -> Decimal | None:
    if value is None:
        return value

    return Decimal(value)


async def init_codec(conn: Connection):
    await conn.set_type_codec(
        "numeric",
        encoder=_encoder_numeric,
        decoder=_decoder_numeric,
        schema="pg_catalog",
        format="text"
    )


__all__ = ["init_codec"]
