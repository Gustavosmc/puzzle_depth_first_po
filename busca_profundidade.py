import copy


visitados = []
caminho = []
cont_id = 1


class Estado(object):

    def __init__(self, estado="XABCDEFGH", matriz=(3, 3)):
        self.tam_x, self.tam_y = matriz
        self.coringa = 'X'
        self.estado = estado
        self.filhos = []
        self.visitado = False
        self.tam_estado = (self.tam_x * self.tam_y) - 1
        self.pos_coringa = self.estado.find(self.coringa)
        self.pai = None
        self.profundidade = 1
        self.id = cont_id


    def proximo(self):
        global cont_id
        cont_id += 1

        self.expande()
        caminho.append(self)

        # Define um profundidade limite para a busca
        # if self.profundidade == 32:
        #     return self.pai

        for filho in self.filhos:
            if filho != self:
                if filho not in visitados:
                    visitados.append(filho)
                    return filho
        return self.pai

    def expande(self):
        self.move_abaixo()
        self.move_direita()
        self.move_acima()
        self.move_esquerda()

    def move_abaixo(self):
        obj_estado = None
        if self.pos_coringa <= (self.tam_estado - self.tam_x):
            obj_estado = Estado(self.estado)
            est = list(obj_estado.estado)
            pos_coringa = obj_estado.pos_coringa
            est[pos_coringa], est[pos_coringa + self.tam_x] = \
                est[pos_coringa + self.tam_x], est[pos_coringa]
            obj_estado.pos_coringa = pos_coringa + self.tam_x
            obj_estado.pai = self
            obj_estado.estado = ''.join(est)
            obj_estado.profundidade = self.profundidade + 1


            # print(str(self) + ' move abaixo')

        if obj_estado is not None: self.filhos.append(obj_estado)

    def move_acima(self):
        obj_estado = None
        if self.pos_coringa > self.tam_x - 1:
            obj_estado = Estado(self.estado, (self.tam_x, self.tam_y))
            est = list(obj_estado.estado)
            pos_coringa = obj_estado.pos_coringa
            est[pos_coringa], est[pos_coringa - self.tam_x] = \
                est[pos_coringa - self.tam_x], est[pos_coringa]
            obj_estado.pos_coringa = pos_coringa - self.tam_x
            obj_estado.pai = self
            obj_estado.estado = ''.join(est)
            obj_estado.profundidade = self.profundidade + 1

            # print(str(self) + ' move acima')

        if obj_estado is not None: self.filhos.append(obj_estado)

    def move_esquerda(self):
        obj_estado = None
        if self.pos_coringa % self.tam_x != 0:
            obj_estado = Estado(self.estado, (self.tam_x, self.tam_y))
            est = list(obj_estado.estado)
            pos_coringa = obj_estado.pos_coringa
            est[pos_coringa], est[pos_coringa - 1] = \
                est[pos_coringa - 1], est[pos_coringa]
            obj_estado.pos_coringa = pos_coringa - 1
            obj_estado.pai = self
            obj_estado.estado = ''.join(est)
            obj_estado.profundidade = self.profundidade + 1

            # print(str(self) + ' move esquerda')

        if obj_estado is not None: self.filhos.append(obj_estado)

    def move_direita(self):
        obj_estado = None
        if (self.pos_coringa + 1) % self.tam_x != 0:
            obj_estado = Estado(self.estado, (self.tam_x, self.tam_y))
            est = list(obj_estado.estado)
            pos_coringa = obj_estado.pos_coringa
            est[pos_coringa], est[pos_coringa + 1] = \
                est[pos_coringa + 1], est[pos_coringa]
            obj_estado.pos_coringa = pos_coringa + 1
            obj_estado.pai = self
            obj_estado.estado = ''.join(est)
            obj_estado.profundidade = self.profundidade + 1

            # print(str(self) + ' move direita')

        if obj_estado is not None: self.filhos.append(obj_estado)

    def __str__(self):
        ret = ''
        for i in range(len(self.estado)):
            if i % self.tam_x == 0:
                ret += "\n"
            ret += " " + self.estado[i]
        return ret

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.estado == other.estado
        return NotImplemented

    def __ne__(self, other):
        """Define a non-equality test"""
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented


def gerar_estado_aleatorio(str_estado):
    import random
    l = list(str_estado)
    random.shuffle(l)
    return ''.join(l)

if __name__ == '__main__':
    str_estado_inicial = "AXBCDEFGH"
    str_estado_inicial = gerar_estado_aleatorio("ABXCDEFGH")


    estado_objetivo = Estado("XABCDEFGH")
    estado = Estado(str_estado_inicial, (3, 3))

    print("-----------------------------------------")
    print("Estado Inicial" + str(estado))
    print("-----------------------------------------")

    while estado != estado_objetivo:
        try:
            estado = estado.proximo()
            print("-----------------------------------------")
            print("Prof. : " + str(estado.profundidade))
            print("Num.  : " + str(estado.id))
            print(estado)
            print("-----------------------------------------")
        except:
            print("Nao foi possivel encontrar nesse espaco de busca")
            break



        # if estado.profundidade in caminho:
        #     print("achou")
        # caminho.append(estado.profundidade)



        # # DEBUG
        # if estado in caminho: print(estado)
        # if estado.estado[0] == "X":
        #     caminho.append(estado)






