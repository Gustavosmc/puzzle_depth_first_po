import copy

visitados = []
caminho = []


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
        self.limite = 100

    def proximo(self):
        self.expande()
        caminho.append(self)
        for filho in self.filhos:
            if filho != self.pai:
                if not filho.visitado:
                    filho.visitado = True
                    return filho

        return self.pai

    def expande(self):
        self.move_abaixo()
        self.move_direita()
        self.move_acima()
        self.move_esquerda()

    def copiar(self):
        return copy.copy(self)

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

        if obj_estado is not None: self.filhos.append(obj_estado)

    def __str__(self):
        ret = ''
        cont = 0
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
            return not self.estado.__eq__(other.estado)
        return NotImplemented


if __name__ == '__main__':
    estado_objetivo = Estado("XABCDEFGH")
    estado = Estado("ABCDEXFGH", (3, 3))
    cont = 0
    while estado is not None:
        print(estado)
        if estado == estado_objetivo: break
        estado = estado.proximo()
        cont += 1
        print(cont)




