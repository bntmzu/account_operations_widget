import json
from datetime import datetime


def mask_card_number(card_number: str) -> str:
    return f'{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}'


def mask_account_number(account_number: str) -> str:
    return f'**{account_number[-4:]}'


def format_date(date_str: str) -> str:
    date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
    return date.strftime("%d.%m.%Y")


def format_operation(operation: dict) -> str:
    date = format_date(operation['date'])
    description = operation['description']
    from_account = operation.get('from', '')
    to_account = operation['to']
    amount = operation['operationAmount']['amount']
    currency = operation['operationAmount']['currency']['name']

    if from_account:
        if ' ' in from_account:
            from_account_name, from_account_number = from_account.rsplit(' ', 1)
            from_account = f'{from_account_name} {mask_card_number(from_account_number)}'
        else:
            from_account = f'Счет {mask_account_number(from_account)}'
    else:
        from_account = 'Неизвестно'

    to_account = f'Счет {mask_account_number(to_account)}'

    return f"{date} {description}\n{from_account} -> {to_account}\n{amount} {currency}"


def print_last_operations(operations, count=5):
    executed_operations = [op for op in operations if op.get('state') == 'EXECUTED']
    last_operations = sorted(executed_operations, key=lambda x: x['date'], reverse=True)[:count]

    for operation in last_operations:
        print(format_operation(operation))
        print()  # Пустая строка между операциями


if __name__ == "__main__":
    with open('operations.json', 'r', encoding='utf-8') as f:
        operations = json.load(f)
    print_last_operations(operations)
