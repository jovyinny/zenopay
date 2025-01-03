"""ZenoPay."""

import logging
from typing import Optional, Union

import phonenumbers
import requests
from pydantic import BaseModel, EmailStr, Field, HttpUrl, field_validator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


class CheckoutSchema(BaseModel):
    """Base Checkout Data Structure."""

    buyer_name: str
    buyer_phone: str
    buyer_email: EmailStr
    amount: float = Field(ge=10)
    webhook_url: Optional[Union[str, HttpUrl]] = None

    @field_validator("buyer_phone")
    def validate_phone_number(cls, value: str) -> Optional[str]:
        """Check phone number field."""
        phone_number = value if isinstance(value, str) else str(value)
        phone_number = phonenumbers.parse(value, "TZ")

        if not phonenumbers.is_valid_number(phone_number):
            msg = "Invalid phone number"
            raise ValueError(msg)
        return phonenumbers.format_number(
            phone_number,
            phonenumbers.PhoneNumberFormat.E164,
        ).removeprefix("+")


class CardPaymentSchema(CheckoutSchema):
    """Card Payment Data schema."""

    redirect_url: Optional[Union[str, HttpUrl]] = None
    cancel_url: Optional[Union[str, HttpUrl]] = None
    billing_country: str = Field(max_length=2, default="TZ")


class ZenoPay:
    """ZenoPay Client."""

    BASE_URL: Union[str, HttpUrl] = HttpUrl("https://api.zeno.africa")
    BASE_URL = BASE_URL if isinstance(BASE_URL, HttpUrl) else HttpUrl(BASE_URL)
    TIMEOUT: int = 5

    def __init__(self, account_id: str) -> None:
        """Initialize.

        Args:
            account_id: str

        Returns:
            None

        Example:
        >>> from zenopay import ZenoPay
        >>> zenopay = ZenoPay(account_id="zpxxxx")

        """
        self.account_id = account_id
        self._api_key = None
        self._secret_key = None

    @property
    def api_key(self) -> Optional[str]:
        """Client API Key."""
        return self._api_key

    @api_key.setter
    def api_key(self, value: str) -> None:
        """Set API key."""
        if isinstance(value, str):
            self._api_key = value
        else:
            msg = f"Expected str type but received {type(value)}"
            raise TypeError(msg)

    @property
    def secret_key(self) -> Optional[str]:
        """Client API Key."""
        return self._secret_key

    @property
    def headers(self) -> dict:
        """Headers."""
        return {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/x-www-form-urlencoded",
        }

    @secret_key.setter
    def secret_key(self, value: str) -> None:
        """Set Secret Key."""
        if isinstance(value, str):
            self._secret_key = value
        else:
            msg = f"Expected str type but received {type(value)}"
            raise TypeError(msg)

    def post(
        self,
        url: str,
        data: dict,
        *,
        is_json: bool = False,
        headers: Optional[dict] = None,
    ) -> dict:
        """Handle post Request.

        Args:
            url: str
            data: dict
            is_json:bool= False, whether data is to be sent as JSON
            headers: Optional[dict], if not provided uses default headers.

        Returns:
            dict

        """
        headers = headers if headers else self.headers
        # Remove None values
        data = {k: v for k, v in data.items() if v}
        try:
            with requests.Session() as session:
                response = (
                    session.post(
                        url=url,
                        headers=headers,
                        json=data,
                        timeout=self.TIMEOUT,
                    )
                    if is_json
                    else session.post(
                        url=url,
                        headers=headers,
                        data=data,
                        timeout=self.TIMEOUT,
                    )
                )
                response.raise_for_status()

                return response.json()
        except (requests.ConnectionError, requests.RequestException) as error:
            msg = f"Exception occured: {error}"
            logging.exception(msg)
            return {"success": False, "message": "Error handling the request."}

    def mobile_checkout(self, data: Union[dict, CheckoutSchema]) -> dict:
        """Initiate Mobile paymennt.

        Args:
            data: Union[dict, CheckoutSchema]

        Returns:
            Response: dict

        Example:
        >>> from zenopay import ZenoPay
        >>> zenopay = ZenoPay(account_id="zpxxxx")
        >>> zenopay.api_key= ""
        >>> zenopay.secret_key = ""
        >>> data={"buyer_name":"jovine me","buyer_phone":"071xxxxxxx","buyer_email":"jovinexxxxxx@gmail.com","amount":1000}
        >>> zenopay.mobile_checkout(data)
        >>> {'status': 'success', 'message': 'Wallet payment successful', 'order_id': '6777ad7e327xxx'}

        """
        if not all([self.api_key, self.secret_key]):
            msg = "You must have api key and secret key set."
            raise ValueError(msg)
        data = (
            data.model_dump(exclude_none=True)
            if isinstance(data, CheckoutSchema)
            else CheckoutSchema(**data).model_dump(exclude_none=True)
        )
        data.update(
            {
                "create_order": 1,
                "api_key": self.api_key,
                "secret_key": self.secret_key,
                "account_id": self.account_id,
            },
        )
        return self.post(url=str(self.BASE_URL), data=data)

    def card_checkout(self, data: Union[dict, CardPaymentSchema]) -> dict:
        """Initiate Card Payment.

        Args:
            data: Union[dict, CardPaymentSchema]

        Returns:
            response: dict

        Example:
        >>> from zenopay import ZenoPay
        >>> zenopay = ZenoPay(account_id="zpxxxx")
        >>> data={"buyer_name":"jovine me","buyer_phone":"071xxxxxxx","buyer_email":"jovinexxxxxx@gmail.com","amount":1000}
        >>> zenopay.card_checkout(data)
        >>> {'status': 'success', 'message': 'Order created successfully', 'order_id': 'xxxxx', 'payment_link': 'https://secure.payment.tz/link'}

        """
        if not all([self.api_key, self.secret_key]):
            msg = "You must have api key and secret key set."
            raise ValueError(msg)
        _data = CardPaymentSchema(**data) if isinstance(data, dict) else data
        url = str(self.BASE_URL) + "/card"
        data = _data.model_dump(exclude_none=True)
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        data.update(
            {
                "billing.country": _data.billing_country,
                "account_id": self.account_id,
                "api_key": self.api_key,
                "secret_key": self.secret_key,
            },
        )
        return self.post(url=url, data=data, is_json=True, headers=headers)

    def check_order_status(self, order_id: str) -> dict:
        """Check Order Status.

        Args:
            order_id: str

        Returns:
            response: dict ->

        Example:
        >>> from zenopay import ZenoPay
        >>> zenopay = ZenoPay(account_id="zpxxxx")
        >>> status= zenopay.check_order_status(order_id="12121212")
        >>> {"status": "success","order_id": "order_id","message": "Order status updated","payment_status": "PENDING"}

        """
        if not isinstance(order_id, str):
            msg = f"Expected str type but received {type(order_id)}"
            raise TypeError(msg)
        url = str(self.BASE_URL) + "/order-status"
        data = {
            "check_status": 1,
            "order_id": order_id,
            "api_key": self.api_key,
            "secret_key": self.secret_key,
        }
        return self.post(url=url, data=data)


__all__ = ["ZenoPay"]
