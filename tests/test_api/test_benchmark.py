import pytest

from app.const.wallet import WalletTypeOperation


@pytest.mark.benchmark(group="wallet_load_test", min_rounds=1000)
async def test_wallet_load_test(
        benchmark,
        client,
        create_new_wallet,
):
    wallet = await create_new_wallet()
    wallet_uuid = wallet["uid"]

    async def send_request():
        response = await client.get(
            f"api/v1/wallets/{wallet_uuid}",
        )
        assert response.status_code == 200

    await benchmark(send_request)


@pytest.mark.benchmark(group="wallet_load_test", min_rounds=1000)
async def test_wallet_load_test(
        benchmark,
        client,
        create_new_wallet,
):
    wallet = await create_new_wallet()
    wallet_uuid = wallet["uid"]

    async def send_request():
        response = await client.post(
            f"api/v1/wallets/{wallet_uuid}/operation",
            json={
                "operationType": WalletTypeOperation.DEPOSIT.value,
                "amount": 1
            }
        )
        assert response.status_code == 200

    await benchmark(send_request)
