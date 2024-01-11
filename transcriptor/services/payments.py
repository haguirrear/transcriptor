from datetime import datetime, timedelta
from typing_extensions import TypedDict
from uuid import uuid4
import pytz
import mercadopago
from typing import List

import logging
from transcriptor.models.payments import (
    MercadoPagoItem,
    MercadoPagoPayer,
    PreferencesResponse,
)
from transcriptor.settings import settings

logger = logging.getLogger(__name__)

sdk_mercado = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)

DEFAULT_PREFERENCE_DATA = {
    "backs_urls": {
        "success": settings.SITE_HOST + "/payments/success",
        "failure": settings.SITE_HOST + "/payments/failure",
        "pending": settings.SITE_HOST + "/payments/pending",
    },
    "auto_return": "approved",
    "statement_descriptor": settings.INVOICE_NAME,
    "binary_mode": True,  # Deactivate the "pending" state for payments (they can only be approved or fail)
    "expires": False,
}


class PreferenceRes(TypedDict):
    id: str
    external_reference: str


async def create_preference(
    items: List[MercadoPagoItem],
    payer: MercadoPagoPayer,
    timezone: str,
    expires_in: timedelta | None = None,
) -> PreferenceRes:
    preference_data = {
        "items": items,
        "payer": payer,
        **DEFAULT_PREFERENCE_DATA,
    }

    if expires_in is not None:
        date_now = datetime.now(pytz.timezone(timezone))
        preference_data.update(
            {
                "expires": True,
                "expiration_date_from": date_now.isoformat(),
                "expiration_date_to": (date_now + expires_in).isoformat(),
            }
        )

    external_reference = str(uuid4())
    preference_data.update({"external_reference": external_reference})

    response: PreferencesResponse = sdk_mercado.preference().create(preference_data)
    if response["status"] != 200:
        logger.error(f"Error occured creating preferences: {response}")
        # TODO: Raise some error

    return {
        "id": response["response"]["id"],
        "external_reference": external_reference,
    }
