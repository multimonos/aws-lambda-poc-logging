import pytest
import os
import boto3
from typing import cast
from mypy_boto3_lambda import LambdaClient


@pytest.fixture
def client() -> LambdaClient:
    client: LambdaClient = cast(LambdaClient, boto3.client("lambda"))
    return client


@pytest.fixture
def fns() -> dict[str, str]:
    dev_fn = os.environ.get("DEV_FN", "")
    prod_fn = os.environ.get("PROD_FN", "")

    if not dev_fn or not prod_fn:
        raise ValueError("Missing required env variables")

    return {"dev": dev_fn, "prod": prod_fn}


def test_something(client: LambdaClient, fns: dict[str, str]):
    print("client:", client)
    print("fns:", fns)
    pass
