import azure.functions as func
import logging

app = func.FunctionApp()

def valida_cpf(cpf: str) -> bool:
    """
    Valida um CPF.
    
    Args:
        cpf (str): CPF no formato "xxx.xxx.xxx-xx" ou apenas números "xxxxxxxxxxx".
        
    Returns:
        bool: True se o CPF for válido, False caso contrário.
    """
    # Remover caracteres não numéricos
    cpf = ''.join(filter(str.isdigit, cpf))

    # Verificar se o CPF tem 11 dígitos
    if len(cpf) != 11:
        return False

    # Verificar se todos os dígitos são iguais (ex: 111.111.111-11)
    if cpf == cpf[0] * 11:
        return False

    # Função para calcular o dígito verificador
    def calcular_digito(cpf_parcial, peso_inicial):
        soma = 0
        for i, digito in enumerate(cpf_parcial):
            soma += int(digito) * (peso_inicial - i)
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    # Calcular o primeiro dígito verificador
    digito1 = calcular_digito(cpf[:9], 10)

    # Calcular o segundo dígito verificador
    digito2 = calcular_digito(cpf[:9] + str(digito1), 11)

    # Verificar se os dígitos calculados correspondem aos informados
    return cpf[-2:] == f"{digito1}{digito2}"

@app.route(route="fnvalidacpf", auth_level=func.AuthLevel.ANONYMOUS)
def fnvalidacpf(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Iniciando a validação de CPF.')

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            "JSON inválido.",
            status_code=400
        )
    
    print(req_body)

    if not req_body:
        return func.HttpResponse(
            "Por favor, informe um CPF para validação.",
            status_code=400
        )

    try:
        cpf = req_body.get('cpf')
        if valida_cpf(cpf):
            return func.HttpResponse(
                "CPF válido.",
                status_code=200
            )
        else:
            return func.HttpResponse(
                "CPF inválido.",
                status_code=400
            )
    except ValueError:
        return func.HttpResponse(
            "Por favor, informe um CPF.",
            status_code=400
        )
