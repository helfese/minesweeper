def cria_gerador(b, s):
    if not (isinstance(b, int) and isinstance(s, int) and s > 0 and ((b == 32 and s < 2 ** 32 - 1) \
        or (b == 64 and s <= 2 ** 64 - 1))):
        raise ValueError('cria_gerador: argumentos invalidos')

    return {'bits': b, 'seed': s}

def cria_copia_gerador(g):
    return g.copy()

def obtem_estado(g):
    return g['seed']

def obtem_bits(g):
    return g['bits']

def define_estado(g, s):
    g['seed'] = s
    return g['seed']

def atualiza_estado(g):
    if g['bits'] == 32:
        g['seed'] ^= (g['seed'] << 13) & 0xFFFFFFFF
        g['seed'] ^= (g['seed'] >> 17) & 0xFFFFFFFF
        g['seed'] ^= (g['seed'] << 5) & 0xFFFFFFFF
        return g['seed']

    elif g['bits'] == 64:
        g['seed'] ^= (g['seed'] << 13) & 0xFFFFFFFFFFFFFFFF
        g['seed'] ^= (g['seed'] >> 7) & 0xFFFFFFFFFFFFFFFF
        g['seed'] ^= (g['seed'] << 17) & 0xFFFFFFFFFFFFFFFF
        return g['seed']

def eh_gerador(arg):
    return isinstance(arg, dict) and 'bits' in arg and 'seed' in arg and isinstance(arg['bits'], int) \
    and (arg['bits'] == 32 or arg['bits'] == 64) and isinstance(arg['seed'], int) and arg['seed'] > 0 and len(arg) == 2

def geradores_iguais(g1, g2):
    return eh_gerador(g1) and eh_gerador(g2) and g1['bits'] == g2['bits'] and g1['seed'] == g2['seed']

def gerador_para_str(g):
    return 'xorshift{}(s={})'.format(g['bits'], g['seed'])

def gera_numero_aleatorio(g, n):
    atualiza_estado(g)
    return 1 + (obtem_estado(g) % n)

def gera_carater_aleatorio(g, c):
    atualiza_estado(g)
    string = ''.join([chr(x) for x in range(ord('A'), ord(c) + 1)])
    return string[obtem_estado(g) % len(string)]

def cria_coordenada(col, lin):
    if not (isinstance(col, str) and 'A' <= col <= 'Z' and len(col) == 1 and isinstance(lin, int) and 1 <= lin <= 99):
        raise ValueError('cria_coordenada: argumentos invalidos')

    return (col, lin)

def obtem_coluna(c):
    return c[0]

def obtem_linha(c):
    return c[1]

def eh_coordenada(arg):
    return isinstance(arg, tuple) and isinstance(arg[0], str) and len(arg[0]) == 1 and isinstance(arg[1], int) \
        and 'A' <= arg[0] <= 'Z' and len(arg[0]) == 1 and 1 <= arg[1] <= 99 and len(arg) == 2

def coordenadas_iguais(c1, c2):
    return eh_coordenada(c1) and eh_coordenada(c2) and obtem_coluna(c1) == obtem_coluna(c2) and obtem_linha(c2) == obtem_linha(c1)

def coordenada_para_str(c):
    return '{}{:0>2}'.format(obtem_coluna(c), obtem_linha(c))

def str_para_coordenada(s):
    return (s[0],int(s[1:]))

def obtem_coordenadas_vizinhas(c):
    if obtem_coluna(c) == 'A':
        if obtem_linha(c) == 1:
            return (('B', 1), ('B', 2), ('A', 2))
        elif obtem_linha(c) == 99:
            return (('A', 98), ('B', 98), ('B', 99))
        else:
            return (('A', obtem_linha(c)-1), ('B', obtem_linha(c)-1), ('B', obtem_linha(c)), ('B', obtem_linha(c)+1), ('A', obtem_linha(c)+1))

    elif obtem_coluna(c) == 'Z':
        if obtem_linha(c) == 1:
            return (('Z', 2), ('Y', 2), ('Y', 1))
        elif obtem_linha(c) == 99:
            return (('Y', 98), ('Z', 98), ('Y', 99))
        else:
            return (('Y', obtem_linha(c)-1), ('Z', obtem_linha(c)-1), ('Z', obtem_linha(c)+1), ('Y', obtem_linha(c)+1), ('Y', obtem_linha(c)))

    else:
        if obtem_linha(c) == 1:
            return ((chr(ord(obtem_coluna(c)) + 1), 1), (chr(ord(obtem_coluna(c)) + 1), 2), (obtem_coluna(c), 2), (chr(ord(obtem_coluna(c)) - 1), 2), (chr(ord(obtem_coluna(c)) - 1), 1))
        elif obtem_linha(c) == 99:
            return ((chr(ord(obtem_coluna(c)) - 1), 98), (obtem_coluna(c), 98), (chr(ord(obtem_coluna(c)) + 1), 98), (chr(ord(obtem_coluna(c)) + 1), 99), (chr(ord(obtem_coluna(c)) - 1), 99))
        else:
            return ((chr(ord(obtem_coluna(c)) - 1), obtem_linha(c)-1), (obtem_coluna(c), obtem_linha(c)-1), (chr(ord(obtem_coluna(c)) + 1), obtem_linha(c)-1), (chr(ord(obtem_coluna(c)) + 1), obtem_linha(c)), \
                    (chr(ord(obtem_coluna(c)) + 1), obtem_linha(c)+1), (obtem_coluna(c), obtem_linha(c)+1), (chr(ord(obtem_coluna(c)) - 1), obtem_linha(c)+1), (chr(ord(obtem_coluna(c)) - 1), obtem_linha(c)))

def obtem_coordenada_aleatoria(c, g):
    return cria_coordenada(gera_carater_aleatorio(g, obtem_coluna(c)), gera_numero_aleatorio(g, obtem_linha(c)))

def cria_parcela():
    return {'estado': '#', 'mina': False}

def cria_copia_parcela(p):
    return p.copy()

def limpa_parcela(p):
    p['estado'] = '?/X'
    return p

def marca_parcela(p):
    p['estado'] = '@'
    return p

def desmarca_parcela(p):
    p['estado'] = '#'
    return p

def esconde_mina(p):
    p['mina'] = True
    return p

def eh_parcela(arg):
    if isinstance(arg, dict) and 'estado' in arg \
        and isinstance(arg['estado'], str) and (arg['estado'] == '#' or arg['estado'] == '@' or arg['estado'] == '?/X') \
        and 'mina' in arg and isinstance(arg['mina'], bool) and (arg['mina'] == True or arg['mina'] == False) and len(arg) == 2:
            return True
    return False

def eh_parcela_tapada(p):
    return p['estado'] == '#'

def eh_parcela_marcada(p):
    return p['estado'] == '@'

def eh_parcela_limpa(p):
    return p['estado'] == '?/X'

def eh_parcela_minada(p):
    return p['mina']

def parcelas_iguais(p1, p2):
    return eh_parcela(p1) and eh_parcela(p2) and p1['estado'] == p2['estado'] and p1['mina'] == p2['mina']

def parcela_para_str(p):
    if p['estado'] == '?/X':
        if p['mina']:
            return 'X'
        else:
            return '?'
    return p['estado']

def alterna_bandeira(p):
    if eh_parcela_marcada(p):
        desmarca_parcela(p)
        return True
    elif eh_parcela_tapada(p):
        marca_parcela(p)
        return True
    return False

def cria_campo(c, l):
    if not (isinstance(c, str) and 'A' <= c <= 'Z' and len(c) == 1 and isinstance(l, int) and 1 <= l <= 99):
        raise ValueError('cria_campo: argumentos invalidos')

    m = []
    lin = 1
    while lin <= l:
        col = ord('A')
        while col <= ord(c):
            m += [[cria_parcela(), cria_coordenada(chr(col), lin)]]
            col += 1
        lin += 1
    return m

def cria_copia_campo(m):
    r = []
    for items in m:
        r += [[cria_copia_parcela(items[0]), items[1]]]
    return r

def obtem_ultima_coluna(m):
    return sorted(m, key = lambda x: x[1][0], reverse = True)[0][1][0]

def obtem_ultima_linha(m):
    return sorted(m, key = lambda x: x[1][1], reverse = True)[0][1][1]

def obtem_parcela(m, c):
    for item in m:
        if item[1] == c:
            return item[0]

def obtem_coordenadas(m, s):
    tup = ()
    if s == 'limpas':
        for item in m:
            if item[0]['estado'] == '?/X':
                tup += (item[1],)
    elif s == 'tapadas':
        for item in m:
            if item[0]['estado'] == '#': #or item[0]['estado'] == '@':
                tup += (item[1],)
    elif s == 'marcadas':
        for item in m:
            if item[0]['estado'] == '@':
                tup += (item[1],)
    elif s == 'minadas':
        for item in m:
            if item[0]['mina']:
                tup += (item[1],)
    return tup

def obtem_numero_minas_vizinhas(m, c):
    num = 0
    for coord in obtem_coordenadas_vizinhas(c):
        if eh_coordenada_do_campo(m, coord) and eh_parcela_minada(obtem_parcela(m, coord)):
            num += 1
    return num

def eh_campo(arg): 
    if isinstance(arg, list):
        for item in arg:
            if not (eh_parcela(item[0]) and eh_coordenada(item[1]) and 10 <= len(arg) <= 26 * 99): #1 + 3 + 5 <= len(arg) <= 26 * 99 ???????????????????????????
                return False
        return True
    return False

def eh_coordenada_do_campo(m, c):
    for item in m:
        if item[1] == c:
            return True
    return False

def campos_iguais(m1, m2):
    Len = 0
    if eh_campo(m1) and eh_campo(m2) and len(m1) == len(m2):
        for item in m1:
            if item in m2:
               Len += 1
        return len(m1) == Len
    return False

def campo_para_str(m):
    def parcela_para_str_(p):
        if eh_parcela_tapada(p):
                return '#'
        elif eh_parcela_marcada(p):
                return '@'
         elif eh_parcela_limpa(p):
            if not eh_parcela_minada(p):
                if obtem_numero_minas_vizinhas(m, z[1]) == 0:
                    return ' '
                else:
                    return str(obtem_numero_minas_vizinhas(m, z[1]))
              else: return 'X'
        return p['estado']

    cols = '   ' + ''.join([chr(x) for x in range(ord('A'), ord(obtem_ultima_coluna(m)) + 1)])+ '\n  '
    string = cols + '+'
    len_cols = len(''.join(cols.split()))
    for y in range(len_cols):
        string += '-'
    string += '+'
    limit = string[4 + len_cols: 4 + 2 * len_cols + 4]
    for y in range(1, obtem_ultima_linha(m) + 1):
        string += '\n' + '{:0>2}'.format(y) + '|'
        for z in m:
            if z[1][1] == y:
                string += parcela_para_str_(z[0])
        string += '|'
    string += '\n' + limit
    return string

def coloca_minas(m, c, g, n):
    coord_minas = ()
    i = 0
    while i < n:
        coord = obtem_coordenada_aleatoria(cria_coordenada(obtem_ultima_coluna(m), obtem_ultima_linha(m)), g)
        if coord != c and coord not in obtem_coordenadas_vizinhas(c) and coord not in coord_minas:
            esconde_mina(obtem_parcela(m, coord))
            coord_minas += (coord,)
            i += 1
    return m

def limpa_campo(m, c):
    limpa_parcela(obtem_parcela(m, c))
    limpas = [[c,True]]
    for coord in obtem_coordenadas_vizinhas(c):
            if eh_coordenada_do_campo(m, coord):
                if eh_parcela_minada(obtem_parcela(m, coord)):
                    return m
    for coord in obtem_coordenadas_vizinhas(c):
            if eh_coordenada_do_campo(m, coord) and not eh_parcela_limpa(obtem_parcela(m, coord)) and not eh_parcela_minada(obtem_parcela(m, coord)) and not eh_parcela_marcada(obtem_parcela(m, coord)):
                limpa_parcela(obtem_parcela(m, coord))
                limpas += [[coord, False]]
            
    for item in limpas:
        if not item[1]:
            limpa_campo(m, item[0])
            
    return m

def jogo_ganho(m):
    parcelas_minadas = []
    for coord in obtem_coordenadas(m, 'minadas'):
        parcelas_minadas += [obtem_parcela(m, coord)]
    for item in m:
        if item[0] not in parcelas_minadas:
            if not eh_parcela_limpa(item[0]):
                return False
 return True

def turno_jogador(m):
    global jogada
    input_incorrect = True
    while input_incorrect:
        turnoLM = input('Escolha uma ação, [L]impar ou [M]arcar:')
        if turnoLM == 'L' or turnoLM == 'M':
            input_incorrect = False
    input_incorrect = True
    while input_incorrect:
        turnoC = input('Escolha uma coordenada:')
        jogada = turnoC
        if 'A' <= turnoC[0] <= obtem_ultima_coluna(m) and len(turnoC) == 3: 
            for L in turnoC[1:]:                
                if '0' <= L <= '9':
                    if eh_coordenada((turnoC[0], int(turnoC[1:]))) and eh_coordenada_do_campo(m, str_para_coordenada(turnoC)):
                        input_incorrect = False
        if jogo_ganho(m):
            return False
        if turnoLM == 'L':
            limpa_campo(m, str_para_coordenada(turnoC))
        elif turnoLM == 'M':
            alterna_bandeira(obtem_parcela(m, str_para_coordenada(turnoC)))

    if str_para_coordenada(jogada) in obtem_coordenadas(m, 'minadas'):
            if not (eh_parcela_marcada(obtem_parcela(m, str_para_coordenada(jogada)))):
                return False

    return True
        
