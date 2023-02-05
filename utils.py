import redis

def gera_id():
    """
    Função para gerar ID's automáticos
    """
    try:
        conn = conectar()
        
        chave = conn.get('chave')

        if chave:
            chave = conn.incr('chave')
            return chave
        else:
            conn.set('chave',1)
            return 1
    except redis.exceptions.ConnectionError as e:
        (f'Não foi possível gerar o ID: {e}')

def conectar():
    """
    Função para conectar ao servidor
    """
    conn = redis.Redis(host = 'localhost', port = 6379)
    return conn

def desconectar(conn):
    """ 
    Função para desconectar do servidor.
    """
    if conn:
        conn.connection_pool.disconnect()

def listar():
    """
    Função para listar os produtos
    """
    # Definição da conexão
    conn = conectar()

    try:
        produtos = conn.keys(pattern = 'produtos:*')

        if len(produtos) > 0: 
            for chave in produtos:
                print('Listando produtos ...')
                print('---------------------')
                # Retorno de cada produto em uma string binária (utilizar o comando 'str' para adequação dos textos)
                produto = conn.hgetall(chave)
                print(f"ID: {str(chave, 'utf-8', 'ignore')}")
                print(f"Produto: {str(produto[b'nome'], 'utf-8', 'ignore')}")
                print(f"Preço: {str(produto[b'preco'], 'utf-8', 'ignore')}")
                print(f"Estoque: {str(produto[b'estoque'], 'utf-8', 'ignore')}")
                print('---------------------')
        else:
            print("Não existem produtos a serem listados!")
            print('---------------------')
    except redis.exceptions.ConnectionError as e:
        print(f'Não foi possível listar os produtos: {e}')
        print('---------------------')
        
    desconectar(conn)

def inserir():
    """
    Função para inserir um produto
    """ 
    # Definição da conexão 
    conn = conectar()

    print('Inserindo produto ...')
    print('---------------------')
    nome = input("Informe o nome do produto: ")
    preco = float(input("Informe o preço do produto: "))
    estoque = int(input("Informe a quantidade de produtos em estoque: "))

    valorProduto = {'nome': nome, 'preco': preco, 'estoque': estoque}
    chave = f'produtos:{gera_id()}'

    try:
        # 'hmset': inserção de múltiplos valores
        res = conn.hmset(chave, valorProduto)
        
        if res:
            print(f'O produto {nome} foi inserido com sucesso.')
            print('---------------------')
        else:
            print('Não foi possível inserir o produto.')
            print('---------------------')
    except redis.exceptions.ConnectionError as e:
        print(f'Não foi possível inserir o produto: {e}')
        print('---------------------')

    desconectar(conn)

def atualizar():
    """
    Função para atualizar um produto
    """
    # Definição da conexão
    conn = conectar()

    print('Atualizando produto ...')
    print('---------------------')

    chave = input('Informe a chave do produto: ')

    if conn.keys(pattern = chave):
        nome = input('Informe o nome atualizado do produto: ')
        preco = float(input('Informe o preço atualizado do produto: '))
        estoque = int(input('Informe a quantidade atualizada de produtos em estoque: '))

        valorProduto = {'nome': nome, 'preco': preco, 'estoque': estoque}

        try:
            # 'hmset': inserção de múltiplos valores
            res = conn.hmset(chave, valorProduto)

            if res:
                print(f'O produto {nome} foi atualizado com sucesso.')
                print('---------------------')
        except redis.exceptions.ConnectionError as e:
            print(f'Não foi possível atualizar o produto: {e}')
            print('---------------------')
    else:
        print('Não foi possível localizar o produto (Chave sem correspondência).')
        print('---------------------')

    desconectar(conn)

def deletar():
    """
    Função para deletar um produto
    """  
    # Definição da conexão
    conn = conectar()

    print('Deletando produtos ...')
    print('---------------------')

    chave = input('Informe a chave do produto: ')

    try:
        res = conn.delete(chave)

        if res:
            print(f'O produto com a chave {chave} foi deletado com sucesso.')
            print('---------------------')
        else:
            print(f'Não foi possível deletar o produto (chave {chave} sem correspondência).')
            print('---------------------')
    except redis.exceptions.ConnectionError as e:
        print(f'Não foi possível deletar o produto: {e}.')
        print('---------------------')

    desconectar(conn)

def menu():
    """
    Função para gerar o menu inicial
    """
    # Operações disponíveis no menu ('sair' sempre em última posição)
    operacoesTxt = ['Listar produtos.', 'Inserir produto.', 'Atualizar produto.', 'Deletar produto.', 'Sair.']
    # Extração de nomes das funções correspondentes
    operacoes = [operacao.split()[0].lower() for operacao in operacoesTxt]
    # Formatação de exibição de texto das operações disponíveis no menu
    operacoesTxt = [str(it+1) + ' - ' + operacoesTxt[it] for it in range(0,len(operacoesTxt))]
    
    opcao = 0
    # Loop para seleção de operações no menu pelo usuário
    while(opcao != len(operacoesTxt)):
        #  Prints das operações dispníveis no terminal
        print('=========Gerenciamento de Produtos==============')
        print('Selecione uma opção: ')
        for operacaoTxt in operacoesTxt:
            print(operacaoTxt)
        # Coleta da operação desejada pelo usuário
        opcao = int(input())
        # Chamada das funções desejadas pelo usuário
        if opcao != len(operacoesTxt):
            globals()[operacoes[opcao-1]]()
        # Encerramento do loop 
        elif opcao == len(operacoesTxt):
                print('*** Saindo ***')
        else:
            print('*** Opção inválida ***')
