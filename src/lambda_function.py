from dataclasses import dataclass
import logging
import os
from typing import Any
from util import payload_from_event, success_response, error_response

ENV = os.environ.get("ENVIRONMENT")

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@dataclass
class LambdaParams:
    dryrun: bool = False
    message: str = ""

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> "LambdaParams":
        return cls(
            dryrun=payload.get("dryrun", False), message=payload.get("message", "")
        )


def lambda_handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    if not ENV:
        return error_response(500, "Environment not configured.")

    payload = payload_from_event(event)

    params = LambdaParams.from_payload(payload)

    logger.info(params.message)

    return success_response(
        body={"message": "ok", "env": ENV, "params": params.__dict__}
    )


if __name__ == "__main__":
    print(lambda_handler({"dryrun": True, "foobar": True, "bam": "bazzzz"}, None))
    print(lambda_handler({"dryrun": False, "foobar": True, "bam": "bazzzz"}, None))
    print(lambda_handler({"foobar": True, "bam": "bazzzz"}, None))
