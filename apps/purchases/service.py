import hmac

import requests
from django.urls import reverse

from apps.purchases.models import Purchase


class LeadpayError(Exception):
    pass


def calc_payload_hash(payload: dict, secret: str) -> str:
    raw_value = "".join([x[1] for x in sorted(payload.items())])
    return hmac.new(secret.encode("utf-8"), raw_value.encode("utf-8"), "sha256").hexdigest()


def generate_leadpay_payment_link(purchase: Purchase) -> str:
    payload = dict(
        login="demo-login",
        id=str(purchase.id),
        product_name=purchase.course.name,
        product_price=str(purchase.price),
        count="1",
        email=purchase.user.email,
        phone="+79991112233",  # TODO: add phone to User model
        fio=purchase.user.get_full_name(),
        notification_url=reverse("leadpay-notification"),  # TODO: add BASE_URL
    )

    payload["hash"] = calc_payload_hash(payload, "SECRET")

    response = requests.post(
        "https://app.leadpay.ru/api/v2/getLink/",
        json=payload,
    )
    if response.status_code != 200:
        try:
            error = response.json()["description"]
        except Exception as ex:
            raise LeadpayError(f"Unexpected error in Leadpay: {ex}")
        raise LeadpayError(error)
    return response.json()["url"]
