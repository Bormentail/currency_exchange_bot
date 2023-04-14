import requests
import json

from config import API_KEY, currency_tickets


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_sum(text):
        params = text.split()
        try:
            if len(params) != 3:
                raise APIException("Должно быть 3 параметра, разделенных пробелами.")
        except APIException as err:
            return None, None, None, None, err

        base, sym, amount = params
        try:
            if base not in currency_tickets:
                raise APIException(f"Недоступная валюта {base}.")
        except APIException as err:
            return None, None, None, None, err
        base_ticket = currency_tickets[base]

        try:
            if sym not in currency_tickets:
                raise APIException(f"Недоступная валюта {sym}.")
        except APIException as err:
            return None, None, None, None, err
        sym_ticket = currency_tickets[sym]

        try:
            if base == sym:
                raise APIException("Укажите разные валюты.")
        except APIException as err:
            return None, None, None, None, err

        try:
            num = float(amount.replace(",", "."))
        except ValueError:
            err = f"Третий параметр {amount} должен быть числовой."
            return None, None, None, None, err

        headers = {"apikey": API_KEY}
        url = f"https://api.apilayer.com/exchangerates_data/latest?base={base_ticket}&symbols={sym_ticket}"
        r = requests.get(url, headers=headers)
        text = json.loads(r.content)
        summ = text["rates"][sym_ticket]*num
        return base_ticket, sym_ticket, amount, summ, None
