import random


class Peca(object):
    """
    Objeto que representa cada peca no jogo de quebra cabecas
    """

    def __init__(self, simbolo, coringa=False):
        self.simbolo = simbolo
        self.coringa = coringa
        self.filhos = []
        self.visitada = False
        self.posicao_atual = 0

    def __repr__(self):
        return self.simbolo

    # TODO, agora é que ta o problema se uma peca ja foi visitada mas o caminho por um dos filhos nao
    def proxima(self):
        """
        :return: A proxima peca nao visitada ou caso todas ja tiverem sido visitadas retorna um filho aleatorio
        """
        for f in self.filhos:
            if not f.visitada:
                f.visitada = True
                return f
        return self.filhos[random.randint(0, len(self.filhos) - 1)]


def mostrar_como_matriz(pecas, x):
    """ 
    mostra um vetor no formato matriz
    -> A B C X D E F G H
          
        -> A B C
        -> X D E
        -> F G H
    :param pecas: Um vetor de pecas
    :param x: Um inteiro representando o comprimento x da matriz
    """
    for i in range(x, len(pecas) + 1, x):
        for j in range(i-x, i):
            print(pecas[j], end=" ")
        print()


def construir_pecas(simbolos, coringa='X'):
    """
    :param simbolos: O simbolos a serem atribuidos a cada peca
    :param coringa: A peca vaga (nula)
    :return: Um vetor de pecas
    """
    pecas = []
    for i in range(len(simbolos)):
        if simbolos[i] == coringa:
            pecas.append(Peca(simbolos[i], coringa=True))
        else:
            pecas.append(Peca(simbolos[i]))
        pecas[i].posicao_atual = i
    return pecas


def gerar_jogo_aleatorio(simbolos, matriz=(3, 3), coringa='X'):
    """
    :param simbolos: Um Vetor com os simbolos da pecas
    :param matriz: Uma Tupla (x, y) o tamanho o jogo
    :param coringa: A peca vaga (nula)
    :return: Retorna um vetor de pecas desordenado com os filhos de cada Peca atribuidos
    """
    x, y = matriz
    size = len(simbolos)
    if size != x * y: # Se o tamanho do vetor de simbolos for menor que a multiplicacao (X por Y) da matriz
        raise ValueError('Erro quantidade de simbolos nao satisfaz o tamanho da matriz')
    if not coringa in simbolos: # Nao foi definida uma peca coringa
        raise ValueError('Erro coringa nao encontrado')

    copy_simb = simbolos.copy()
    random.shuffle(copy_simb)

    pecas = construir_pecas(copy_simb, coringa)

    # Distribui filhos para os respectivos nós
    for i in range(size):
        if i <= x or i + 1 % x == 0 or i % x == 0 or i > size - x:
            if i == 0 or i == size - 1 or i == x-1 or i == size-x: # 2 filhos
                if i == 0:  # superior esquerdo e 2 filhos
                    pecas[i].filhos.append(pecas[i+1])
                    pecas[i].filhos.append(pecas[i+x])
                elif i == x-1:  # (i-1), (i+x-1),    superior direito e 2 filhos
                    pecas[i].filhos.append(pecas[i-1])
                    pecas[i].filhos.append(pecas[i+x])
                elif i == size-x:  # (i+1), (i-x),   inferior esquerdo e 2 filhos
                    pecas[i].filhos.append(pecas[i+1])
                    pecas[i].filhos.append(pecas[i-x])
                elif i == size-1:  # (i-x), (i-1)    inferior direito e 2 filhos
                    pecas[i].filhos.append(pecas[i-x])
                    pecas[i].filhos.append(pecas[i-1])
            else:  # 3 filhos
                if i < x:  # (i-1), (i+1), (i+x-1),  superior e 3 filhos
                    pecas[i].filhos.append(pecas[i-1])
                    pecas[i].filhos.append(pecas[i+1])
                    pecas[i].filhos.append(pecas[i+x])
                elif i % x == 0:  # (i-x), (i+1), (i+x),   esquerdo e 3 filhos
                    pecas[i].filhos.append(pecas[i-x])
                    pecas[i].filhos.append(pecas[i+1])
                    pecas[i].filhos.append(pecas[i+x])
                elif i+1 % x == 0:  # (i-x), (i+x), (i-1),  direito e 3 filhos
                    pecas[i].filhos.append(pecas[i-x])
                    pecas[i].filhos.append(pecas[i+x])
                    pecas[i].filhos.append(pecas[i-1])
                elif i > size-x:  # (i-x), (i+1), (i-1),  inferior e 3 filhos
                    pecas[i].filhos.append(pecas[i-x])
                    pecas[i].filhos.append(pecas[i+1])
                    pecas[i].filhos.append(pecas[i-1])
        else:  # (i - 1), (i + 1), (i + x), (i - x), 4 filhos
            pecas[i].filhos.append(pecas[i-1])
            pecas[i].filhos.append(pecas[i+1])
            pecas[i].filhos.append(pecas[i+x])
            pecas[i].filhos.append(pecas[i-x])
    return pecas


def buscar(vet_pecas, vet_objetivo, coringa='X'):
    """
    :param vet_pecas: 
    :param vet_objetivo: 
    :param coringa: 
    :return: Um vetor de inteiros, sendo os index do caminho encontrado ate a peca objetivo
    """
    caminho = []
    p_coringa = None
    p_atual = None
    p_objetivo = None
    for p in vet_pecas:
        if p.simbolo == coringa:
            p_coringa = p
            for po in vet_objetivo:
                if p_coringa.posicao_atual == po.posicao_atual:
                    p_objetivo = po
                    break
            break
    p_atual = p_coringa
    while True:
        caminho.append(p_atual.posicao_atual)
        if p_objetivo.simbolo == p_atual.simbolo:
            print("Achou")
            break
        p_atual = p_atual.proxima()
    print(p_objetivo.simbolo)
    return caminho

def move(vet_pecas, caminho):
    for i in range(len(caminho)):
        try:
            vet_pecas[caminho[i]].filhos, vet_pecas[caminho[i+1]].filhos = \
            vet_pecas[caminho[i+1]].filhos, vet_pecas[caminho[i]].filhos

            vet_pecas[caminho[i]], vet_pecas[caminho[i+1]] = \
            vet_pecas[caminho[i+1]], vet_pecas[caminho[i]]
        except:
            break


def start():

    X, Y = 3, 3
    g_simbolos = "X 1 2 3 4 5 6 7 8".split(' ')

    objetivo = construir_pecas(g_simbolos)

    pecas = gerar_jogo_aleatorio(g_simbolos, (X, Y))

    print("Jogo embaralhado: ")
    print(mostrar_como_matriz(pecas, X))



    print("Jogo Movimento: ")
    print(mostrar_como_matriz(pecas, X))
    print("Objetivo: ")
    print(mostrar_como_matriz(objetivo, X))



if __name__ == '__main__':
    start()
