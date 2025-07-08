from collections import defaultdict, deque

def group_transactions_by_key(transactions):
    """
    Agrupa transações por uma chave composta por (Departamento, Valor, Beneficiário),
    e associa a cada chave uma deque com as datas dessas transações, ordenadas de forma crescente.

    Parâmetros:
    - transactions: lista de listas, onde cada transação tem o formato [data, departamento, valor, beneficiário]

    Retorno:
    - Um dicionário com chaves (departamento, valor, beneficiário) e valores como deques de datas ordenadas.
    """
    grouped = defaultdict(list)  # Dicionário com lista como valor padrão

    for transaction in transactions:
        key = tuple(transaction[1:4])  # Cria chave com os campos de índice 1 a 3 (departamento, valor e beneficiário)
        grouped[key].append(transaction[0])  # Adiciona a data (índice 0) à lista

    # Para cada chave, ordena as datas e transforma em deque para eficiência no acesso
    for key in grouped:
        grouped[key].sort()
        grouped[key] = deque(grouped[key])
    
    return grouped


def restore_original_order(original_list, sorted_with_flags):
    """
    Restaura a ordem da versão marcada com flags para a da lista de transações original

    Parâmetros:
    - original_list: lista original das transações, sem marcação
    - sorted_with_flags: lista das mesmas transações, ordenadas por data e com marcações

    Retorno:
    - Lista com as transações na ordem original e suas respectivas flags
    """
    def transaction_key(transaction):
        # Os quatro primeiros campos são usados para comparar (ignora a flag)
        return tuple(transaction[:4])

    flagged_map = defaultdict(deque)

    # Cria um mapa com as transações com flag agrupadas por chave
    for transaction in sorted_with_flags:
        flagged_map[transaction_key(transaction)].append(transaction)

    restored = []

    # Reconstroi a lista na ordem original, pegando o primeiro elemento disponível para cada chave
    for transaction in original_list:
        key = transaction_key(transaction)
        restored.append(flagged_map[key].popleft())  # popleft é O(1)
    
    return restored


def reconcile_accounts(transactions1, transactions2):
    """
    Compara duas listas de transações e reconcilia elas com base em data, departamento, valor e beneficiário.
    Marca cada transação com 'FOUND' (se encontrada na outra lista) ou 'MISSING' (caso contrário).
    A ordem original das transações é preservada na saída.

    Parâmetros:
    - transactions1 (list): lista de transações 1
    - transactions2 (list): lista de transações 2

    Retorno:
    - Duas lists: transactions1 e transactions2, com flags de 'FOUND' ou 'MISSING', na ordem original
    """
    # Agrupa as transações por chave (departamento, valor, beneficiário) e associa as datas
    dict1 = group_transactions_by_key(transactions1)
    dict2 = group_transactions_by_key(transactions2)

    # Ordena as transações por data para priorizar reconciliação pelas mais antigas
    transactions1_sorted = sorted(transactions1, key=lambda x: x[0])
    transactions2_sorted = sorted(transactions2, key=lambda x: x[0])

    def flag_transactions(transactions, compare_dict):
        """
        Marca cada transação como 'FOUND' se a chave existir no dicionário e ainda houver datas disponíveis.
        Caso contrário, marca como 'MISSING'.
        """
        for transaction in transactions:
            key = tuple(transaction[1:4])
            if key in compare_dict and compare_dict[key]:
                transaction.append('FOUND')
                compare_dict[key].popleft()  # Remove a data correspondente
                if not compare_dict[key]:  # Remove a chave se não houver mais datas
                    del compare_dict[key]
            else:
                transaction.append('MISSING')

    # Marca as transações da primeira lista com base na segunda
    flag_transactions(transactions1_sorted, dict2)
    # Marca as transações da segunda lista com base na primeira
    flag_transactions(transactions2_sorted, dict1)

    # Restaura a ordem original das listas, agora com as flags
    transactions1_restored = restore_original_order(transactions1, transactions1_sorted)
    transactions2_restored = restore_original_order(transactions2, transactions2_sorted)

    return transactions1_restored, transactions2_restored
