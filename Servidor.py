class Usuario:
    def __init__(self, ttask, tick_atual):
        self._tick_saida = tick_atual + ttask

    @property
    def tick_saida(self):
        return self._tick_saida


class Servidor:
    def __init__(self, ttask, umax):
        self._ttask = ttask
        self._umax = umax
        self._custo = 1
        self._usuario_logados = 0
        self._serv_online = True
        self._lista_usuarios = []

    @property
    def ttask(self):
        return self._ttask

    @property
    def custo(self):
        return self._custo

    @property
    def usuarios_logados(self):
        return self._usuario_logados

    @usuarios_logados.setter
    def usuarios_logados(self, usuarios_logados):
        self._usuario_logados = usuarios_logados

    def adiciona_usuario(self, tick_atual):
        """Insere usuario no servidor atual

        :param tick_atual: ciclo atual de atividade (tick)
        :return: retornar True se inseriu senao False caso servidor cheio
        """
        if self.usuarios_logados < self.umax:
            self.usuarios_logados += 1
            self._lista_usuarios.append(Usuario(self.ttask, tick_atual))
            return True
        else:
            return False

    def remove_usuario(self, usuario):
        """Remove usuario da lista de usuarios do servidor do objeto atual.

        :param usuario: usuario do servidor atual a ser removido
        """
        if self.usuarios_logados > 0:
            self.usuarios_logados = 0
            self._lista_usuarios.remove(usuario)

    @property
    def lista_usuarios(self):
        return self._lista_usuarios

    @property
    def umax(self):
        return self._umax

    @property
    def serv_online(self):
        return self._serv_online

    @serv_online.setter
    def serv_online(self, serv_online):
        self._serv_online = serv_online


def check_usuario(servidores, tick):
    """Valida se algum usuario do servidor e tick atual está no tick de saida,
    removendo através do metodo remove_usuario(usuario).

    :param servidores:
    :param tick:
    """
    for servs in servidores:
        for usuario in servs.lista_usuarios:
            if usuario.tick_saida == tick:
                servs.remove_usuario(usuario)

def insere_usuario(servidores, vttask, vumax, tick):
    """ Insere usuario no servidor através do metodo adiciona_usuario(tick), caso  servidor esteja ativado
    (serv_online=True), caso nao estiver (serv_online=False) ativa.

    :param servidores: lista de servidores ativos e inativos
    :param vttask: parametro para definir tarefa final do usuario
    :param vumax: parametro para definir quantidade maxima de usuarios no servidor
    :param tick: tick atual do ciclo de tarefas
    :return: retorna lista de servidores atualizada com os novos usuarios
    """
    inseriu = False
    for servs in servidores:
        if servs.usuarios_logados > 0 and servs.adiciona_usuario(tick):
            inseriu = True
            break

        elif servs.usuarios_logados == 0 and not servs.serv_online:
            servs.serv_online = True
            servs.adiciona_usuario(tick)
            inseriu = True
            break

    if not inseriu:
        serv = Servidor(vttask, vumax)
        serv.adiciona_usuario(tick)
        servidores.append(serv)
    return servidores


def health_check(servidores):
    """Checa status do servidor online, desativando caso usuarios logados forem iguais a 0

    :param servidores: lista de servidores ativado e desativado
    :return: returna lista de servidores atualizada
    """
    for servs in servidores:
        if servs.usuarios_logados == 0 and servs.serv_online:
            servs.serv_online = False
    return servidores


def calcula_custo(servidores):
    """Calcula custo para servidores online

    :param servidores: lista de servidores ativado e desativado
    :return: retorna custo 1 para cada servidor online
    """
    custo = 0
    for serv in servidores:
        if serv.serv_online:
            custo += serv.custo

    return custo

def gera_saida(servidores, lista_saida):
    """
    Concatena lista de usuarios por servidor em forma de lista separado por vírgula

    :param servidores: Lista de servidores
    :param lista_saida: lista
    :return:
    """
    lista_temp = []
    for i in servidores:
        lista_temp.append(str(i.usuarios_logados))

    lista_saida.append(','.join(lista_temp))
    return lista_saida


def le_arquivo():
    """Le arquivo com lista de dados para entrada.

    :return: Retorna lista lida no arquivo.
    """
    lista = []
    try:
        with open('input.txt') as f:
            lines = f.readlines()
        for i in lines:
            lista.append(int(i.replace('\n', '').strip()))
    except FileNotFoundError:
        print('Erro na leitura do arquivo.')

    return lista

def escreve_arquivo(dados):
    """Cria arquivo de saida com a lista de dados informados por parametro.

    :param dados: Lista que contem os dados para serem escritos.
    """
    with open('output.txt', 'w') as f:
            f.write(''.join('{0}\n'.format(i) for i in dados))

#bloco principal
if __name__ == '__main__':
    inputs = le_arquivo()

    vttask = inputs[0]
    vumax = inputs[1]
    novos_usuarios = inputs[2:]

    lista_servidores = []
    lista_output = []

    v_exit = False
    tick = 0
    custo_total = 0

    for i in novos_usuarios:
        tick += 1
        check_usuario(lista_servidores, tick)

        for usuario in range(i):
            if bool(lista_servidores):
                lista_servidores = insere_usuario(lista_servidores, vttask, vumax, tick)

            else:
                lista_servidores.append(Servidor(vttask, vumax))
                lista_servidores = insere_usuario(lista_servidores, vttask, vumax, tick)

        lista_servidores = health_check(lista_servidores)
        custo_total += calcula_custo(lista_servidores)
        lista_output = gera_saida(lista_servidores, lista_output)

    for p in range(vttask):
        tick += 1
        check_usuario(lista_servidores, tick)
        lista_servidores = health_check(lista_servidores)
        custo_total += calcula_custo(lista_servidores)
        lista_output = gera_saida(lista_servidores, lista_output)

    lista_output.append(str(custo_total))
    escreve_arquivo(lista_output)