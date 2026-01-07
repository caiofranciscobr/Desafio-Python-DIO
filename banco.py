import textwrap

def menu():
    texto_menu = """
    [d] \tDepositar
    [s] \tSacar
    [e] \tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [ci]\tConsultar informações do usuário
    [q] \tSair

    => """
    return input(textwrap.dedent(texto_menu))


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\nDepósito realizado com sucesso!")
    else:
        print("\nOperação falhou, valor inválido.")
    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\nOperação falhou, saldo insuficiente.")

    elif excedeu_limite:
        print("\nOperação falhou, valor excede o limite.")

    elif excedeu_saques:
        print("\nOperação falhou, limite de saques atingido.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\nSaque realizado com sucesso!")

    else:
        print("\nOperação falhou, valor inválido.")

    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
    print('\nEXTRATO')
    print('Não foram realizadas movimentações') if not extrato else extrato
    print(f'\nSaldo:\t\tR$ {saldo:.2f}')

def criar_usuario(usuarios):
    cpf = input('Informe o CPF (somente números): ')

    if not validar_cpf(cpf):
        print('\nCPF inválido, cadastro encerrado.')
        return

    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print('\nJá existe um usuário com este CPF!')
        return

    nome = input('Insira o nome completo: ')
    nome = padronizar_nome(nome)

    data_nascimento = input('Informe a data de nascimento (dd/mm/aaaa): ')
    endereco = input('Insira o endereço (logradouro, nº, bairro, cidade e sigla do estado): ')
    endereco = padronizar_endereco(endereco)

    usuarios.append({
        'nome': nome,
        'data_nascimento': data_nascimento,
        'cpf': cpf,
        'endereco': endereco
    })

    print('\nUsuário criado com sucesso!')

def padronizar_endereco(endereco: str) -> str:
    endereco = endereco.strip().lower()

    partes = [p.strip() for p in endereco.split(",")]

    partes_corrigidas = []

    for parte in partes[:-1]:
        if parte:
            palavras = []
            for palavra in parte.split():
                # se for número, mantém
                if palavra.isdigit():
                    palavras.append(palavra)
                else:
                    palavras.append(palavra.capitalize())

            partes_corrigidas.append(" ".join(palavras))

    uf = partes[-1].strip().upper()
    partes_corrigidas.append(uf)

    return ", ".join(partes_corrigidas)


def validar_cpf(cpf: str) -> bool:
    cpf = ''.join(filter(str.isdigit, cpf))

    if len(cpf) != 11:
        return False

    if cpf in [c * 11 for c in "0123456789"]:
        return False

    soma1 = sum(int(cpf[i]) * (10 - i) for i in range(10))
    digito1 = (soma1 * 10 % 11) % 10

    soma2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
    soma2 += digito1 * 2
    digito2 = (soma2 * 10 % 11) % 10

    return cpf.endswith(f"{digito1}{digito2}")
    
def padronizar_nome(nome: str) -> str:
    nome = nome.strip()

    conectivos = ["de", "da", "do", "das", "dos", "e"]

    partes = nome.title().split()

    partes_corrigidas = [
        parte if parte.lower() not in conectivos else parte.lower()
        for parte in partes
    ]

    return " ".join(partes_corrigidas)

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario['cpf'] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input('Informe o cpf do usuário: ')
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print('\nConta criada com sucesso!')
        return {'agencia': agencia, 'numero_conta': numero_conta, 'usuario': usuario}
    print('\nUsuário não encontrado, fluxo de criação de conta encerrado.')

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
    print('=' * 100)
    print(textwrap.dedent(linha))

def consultar_usuario(usuarios):
    cpf = input("Informe o CPF para consulta: ")

    usuario = filtrar_usuario(cpf, usuarios)

    if not usuario:
        print("\nUsuário não encontrado.")
        return

    print("\nINFORMAÇÕES DO USUÁRIO")
    print(f"Nome: {usuario['nome']}")
    print(f"CPF: {usuario['cpf']}")
    print(f"Data de nascimento: {usuario['data_nascimento']}")
    print(f"Endereço: {usuario['endereco']}")


def main():
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []
    LIMITE_SAQUES = 3
    AGENCIA = '0001'

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == 'e':
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

            else:
                print("\nConta não pôde ser criada.")

        elif opcao == "ci":
            consultar_usuario(usuarios)


        elif opcao == "q":
            print("\nSaindo do sistema.")
            break

        else:
            print("\nOperação inválida, selecione novamente.")

main()