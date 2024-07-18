import nltk
from nltk.tokenize import word_tokenize

# Download NLTK data files (run this uma vez)
nltk.download('punkt')

# Definição das faixas e categorias
faixas = ["branca", "amarela", "vermelha", "laranja", "verde", "roxa", "marrom", "preta"]
categorias = {
    "branca a verde até 75kg": lambda faixa, peso: faixa in faixas[:5] and peso <= 75,
    "branca a verde acima de 75kg": lambda faixa, peso: faixa in faixas[:5] and peso > 75,
    "roxa a preta até 75kg": lambda faixa, peso: faixa in faixas[5:] and peso <= 75,
    "roxa a preta acima de 75kg": lambda faixa, peso: faixa in faixas[5:] and peso > 75
}

# Listas para armazenar os atletas por categoria
listas_categorias = {
    "branca a verde até 75kg": [],
    "branca a verde acima de 75kg": [],
    "roxa a preta até 75kg": [],
    "roxa a preta acima de 75kg": []
}

def parse_atleta_info(texto):
    tokens = word_tokenize(texto.lower())
    
    nome_tokens = []
    faixa = None
    idade = None
    peso = None

    for token in tokens:
        if token in faixas:
            faixa = token
        elif token.isdigit():
            if idade is None:
                idade = int(token)
            else:
                peso = int(token)
        elif "kg" in token:
            peso = int(token.replace("kg", ""))
        else:
            nome_tokens.append(token)

    nome = " ".join(nome_tokens).capitalize() if nome_tokens else None

    # Garantir que idade e peso sejam extraídos corretamente
    if idade is not None and peso is not None:
        if idade < 0 or peso < 0:
            idade, peso = None, None

    return nome, faixa, idade, peso

def categorizar_atleta(texto):
    nome, faixa, idade, peso = parse_atleta_info(texto)
    
    if not all([faixa, idade, peso]):
        return "Dados insuficientes ou formato inválido."

    for categoria, condicao in categorias.items():
        if condicao(faixa, peso):
            listas_categorias[categoria].append(f"{nome}, {faixa}, {idade} anos, {peso}kg")
            return f"Categoria: {categoria}"
    
    return "Dados insuficientes ou formato inválido."

# Loop de entrada de dados
while True:
    texto_entrada = input("Digite as informações do atleta (ex: Yan vermelha 19 70kg) ou -1 para encerrar: ")
    if texto_entrada == "-1":
        break
    resultado = categorizar_atleta(texto_entrada)
    print(resultado)

# Menu para exibição das listas
while True:
    print("\nEscolha uma categoria para exibir a lista de atletas:")
    print("1. Branca a verde até 75kg")
    print("2. Branca a verde acima de 75kg")
    print("3. Roxa a preta até 75kg")
    print("4. Roxa a preta acima de 75kg")
    print("5. Sair")
    
    escolha = input("Digite o número da opção desejada: ")
    
    if escolha == "1":
        print("\nAtletas na categoria branca a verde até 75kg:")
        print("\n".join(listas_categorias["branca a verde até 75kg"]))
    elif escolha == "2":
        print("\nAtletas na categoria branca a verde acima de 75kg:")
        print("\n".join(listas_categorias["branca a verde acima de 75kg"]))
    elif escolha == "3":
        print("\nAtletas na categoria roxa a preta até 75kg:")
        print("\n".join(listas_categorias["roxa a preta até 75kg"]))
    elif escolha == "4":
        print("\nAtletas na categoria roxa a preta acima de 75kg:")
        print("\n".join(listas_categorias["roxa a preta acima de 75kg"]))
    elif escolha == "5":
        break
    else:
        print("Opção inválida. Tente novamente.")
