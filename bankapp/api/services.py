import requests
from bs4 import BeautifulSoup

from wallet.models import Transfer
from django.db import transaction


def calc_rate(currency):
    """ Парсинг валют с открытых источников. """
    if currency == "usd":
        URL = "https://www.google.com/search?q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80&oq=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80&aqs=chrome..69i57j0i10i131i433i512l2j0i10i433i512j0i10i512l2j46i10i131i433i512j0i10i131i433i512l2j0i10i512.7270j1j15&sourceid=chrome&ie=UTF-8"
    elif currency == "eur":
        URL = "https://www.google.com/search?q=%D0%B5%D0%B2%D1%80%D0%BE&sxsrf=APwXEddPwrfnVmK0af5cSIDe5dVfeJ-clA%3A1680463843533&ei=49cpZPWjINXargTzgIK4Cg&ved=0ahUKEwi1oc7T94v-AhVVrYsKHXOAAKcQ4dUDCA8&uact=5&oq=%D0%B5%D0%B2%D1%80%D0%BE&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIECCMQJzIKCAAQigUQsQMQQzILCAAQgAQQsQMQgwEyBwgAEIoFEEMyBwgAEIoFEEMyBwgAEIoFEEMyBwgAEIoFEEMyCwgAEIAEELEDEIMBMgcIABCKBRBDMggIABCABBCxAzoKCAAQRxDWBBCwAzoNCAAQRxDWBBDJAxCwAzoLCAAQigUQkgMQsAM6DQgAEIoFELADEEMQiwM6EAgAEOQCENYEELADEIsDGAE6GwguEIoFENQCEMgDELADEEMQiwMQpAMQqAMYAjobCC4QigUQ1AIQyAMQsAMQQxCLAxCoAxCdAxgCOg0IABCABBCxAxCDARAKOhIIABCABBAUEIcCELEDEIMBEAo6CggAEIAEELEDEAo6BwgAEIAEEAo6EAgAEIAEEBQQhwIQsQMQgwE6BQgAEIAEOg4ILhCDARDUAhCxAxCABDoNCAAQigUQsQMQgwEQQzoLCC4QgAQQxwEQ0QM6EQguEIAEELEDEIMBEMcBENEDOgsILhCKBRCxAxCDAToHCCMQ6gIQJzoNCAAQjwEQ6gIQtAIYAzoNCC4QjwEQ6gIQtAIYAzoLCAAQigUQsQMQgwE6CwguEIAEELEDEIMBOg4ILhCABBCxAxDHARDRAzoLCC4QgAQQxwEQrwE6BQguEIAEOgkIABCABBAKEAE6CQgAEIAEEAoQKjoLCC4Q1AIQsQMQgAQ6BwgjELECECdKBAhBGABQmgRYhlVg_VZoCnABeACAAXSIAcIMkgEEMTIuNZgBAKABAbABFMgBEbgBAsABAdoBBggBEAEYCdoBBggCEAEYCNoBBggDEAEYCg&sclient=gws-wiz-serp"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

    full_page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(full_page.content, 'html.parser')

    convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})

    return convert[0].text


def calc_exchange_rate(balance, currency):
    if currency == "usd":
        rate = float(calc_rate(currency="usd").replace(",", "."))
    elif currency == "eur":
        rate = float(calc_rate(currency="eur").replace(",", "."))
    return str(float('{:.2f}'.format(balance / rate)))


def calc_balance(account, sum, income=False, expenses=False):
    """ Расчет текущего баланса. """
    if income:
        balance = account.balance + sum
        account.balance = balance
        account.save()
    if expenses:
        if account.balance >= sum:
            balance = account.balance - sum
            account.balance = balance
            account.save()
        else:
            raise(ValueError('Not enough money'))



def make_transfer(from_account, to_account, amount):

    if from_account.balance < amount:
        raise(ValueError('Not enough money'))
    if from_account == to_account:
        raise(ValueError('Chose another account'))

    with transaction.atomic():
        from_balance = from_account.balance - amount
        from_account.balance = from_balance
        from_account.save()

        to_balance = to_account.balance + amount
        to_account.balance = to_balance
        to_account.save()

        transfer = Transfer.objects.create(
            from_account=from_account,
            to_account=to_account,
            amount=amount
        )

    return transfer