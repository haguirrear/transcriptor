from typing import Literal
from typing_extensions import TypedDict

Currency = Literal["PEN", "USD"]


class MercadoPagoItem(TypedDict):
    id: str
    title: str
    currency_id: Currency
    picture_url: str
    description: str
    category_id: str
    quantity: int
    unit_price: float


class Phone(TypedDict):
    area_code: str
    number: str


class Identification(TypedDict):
    type: Literal["DNI"]
    number: str


class Address(TypedDict):
    street_name: str
    street_number: str
    zip_code: str


class MercadoPagoPayer(TypedDict):
    name: str
    surname: str
    email: str
    phone: Phone
    identification: Identification
    address: Address


class PreferencesBody(TypedDict):
    id: str


class PreferencesResponse(TypedDict):
    status: int
    response: PreferencesBody
