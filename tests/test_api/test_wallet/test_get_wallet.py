import pytest
from fastapi import status
from uuid import uuid4

from app.const.wallet import WalletTypeOperation


async def test_get_exist_wallet(
        client,
        create_new_wallet
):
    wallet = await create_new_wallet()
    wallet_uuid = wallet["uid"]
    response = await client.get(
        f"api/v1/wallets/{wallet_uuid}",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["amount"] == "0"


async def test_not_exist_wallet(
        client,
):
    wallet_uuid = str(uuid4())
    response = await client.get(
        f"api/v1/wallets/{wallet_uuid}",
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Wallet not found"


async def test_get_exist_wallet_with_amount(
        client,
        create_new_wallet
):
    wallet = await create_new_wallet()
    wallet_uuid = wallet["uid"]
    response = await client.get(
        f"api/v1/wallets/{wallet_uuid}",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["amount"] == "0"

    amount = 1_000_000
    response = await client.post(
        f"api/v1/wallets/{wallet_uuid}/operation",
        json={
            "operationType": WalletTypeOperation.DEPOSIT.value,
            "amount": amount
        }
    )

    assert response.status_code == status.HTTP_200_OK
    data_json = response.json()
    assert data_json["success"]
    assert data_json["amount"] == str(amount)

    response = await client.post(
        f"api/v1/wallets/{wallet_uuid}/operation",
        json={
            "operationType": WalletTypeOperation.WITHDRAW.value,
            "amount": amount
        }
    )

    assert response.status_code == status.HTTP_200_OK
    data_json = response.json()
    assert data_json["success"]
    assert data_json["amount"] == "0"


async def test_invalid_wallet_uuid(
        client,
):
    wallet_uuid = str(uuid4())
    amount = 1_000_000

    response = await client.post(
        f"api/v1/wallets/{wallet_uuid}/operation",
        json={
            "operationType": WalletTypeOperation.DEPOSIT.value,
            "amount": amount
        }
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Wallet not found"

    response = await client.post(
        f"api/v1/wallets/{wallet_uuid}/operation",
        json={
            "operationType": WalletTypeOperation.WITHDRAW.value,
            "amount": amount
        }
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Wallet not found"


async def test_exist_wallet_not_enough_amount(
        client,
        create_new_wallet
):
    wallet = await create_new_wallet()
    wallet_uuid = wallet["uid"]

    amount = 1_000_000
    response = await client.post(
        f"api/v1/wallets/{wallet_uuid}/operation",
        json={
            "operationType": WalletTypeOperation.WITHDRAW.value,
            "amount": amount
        }
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == "Not enough amount"


async def test_exist_wallet_broken_body(
        client,
        create_new_wallet
):
    wallet = await create_new_wallet()
    wallet_uuid = wallet["uid"]

    amount = "aaaaaaa"
    response = await client.post(
        f"api/v1/wallets/{wallet_uuid}/operation",
        json={
            "operationType": WalletTypeOperation.WITHDRAW.value,
            "amount": amount
        }
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()["detail"][0]["msg"] == "Input should be a valid decimal"

    amount = 1_000_000
    response = await client.post(
        f"api/v1/wallets/{wallet_uuid}/operation",
        json={
            "operationType": "Hell",
            "amount": amount
        }
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()["detail"][0]["msg"] == "Input should be 'DEPOSIT' or 'WITHDRAW'"

