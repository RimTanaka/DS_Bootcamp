import sys

def call_center(clients, recipients):
    """
    Возвращает список клиентов, которые не видели промо-письмо.
    """
    return list(set(clients) - set(recipients))

def potential_clients(participants, clients):
    """
    Возвращает список участников, которые не являются клиентами.
    """
    return list(set(participants) - set(clients))

def loyalty_program(clients, participants):
    """
    Возвращает список клиентов, которые не участвовали в мероприятии.
    """
    return list(set(clients) - set(participants))

def marketing():
    clients = [
        'andrew@gmail.com', 'jessica@gmail.com', 'ted@mosby.com',
        'john@snow.is', 'bill_gates@live.com', 'mark@facebook.com',
        'elon@paypal.com', 'jessica@gmail.com'
    ]
    participants = [
        'walter@heisenberg.com', 'vasily@mail.ru',
        'pinkman@yo.org', 'jessica@gmail.com', 'elon@paypal.com',
        'pinkman@yo.org', 'mr@robot.gov', 'eleven@yahoo.com'
    ]
    recipients = ['andrew@gmail.com', 'jessica@gmail.com', 'john@snow.is']

    task_name = ('call_center', 'potential_clients', 'loyalty_program')
    if len(sys.argv) != 2:
        raise ValueError(f"Usage: python3 marketing.py {task_name}")

    task = sys.argv[1].strip()

    if task == "call_center":
        result = call_center(clients, recipients)
    elif task == "potential_clients":
        result = potential_clients(participants, clients)
    elif task == "loyalty_program":
        result = loyalty_program(clients, participants)
    else:
        raise ValueError(f"Unknown task: {task}.\nUsage: python3 marketing.py {task_name}")

    for email in result:
        print(email)

if __name__ == '__main__':
    marketing()
