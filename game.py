def create_generator(b, s):
    if not (isinstance(b, int) and isinstance(s, int) and s > 0 and ((b == 32 and s < 2 ** 32 - 1) or (b == 64 and s <= 2 ** 64 - 1))):
        raise ValueError('create_generator: invalid arguments')
    return {'bits': b, 'seed': s}

def copy_generator(g):
    return g.copy()

def get_state(g):
    return g['seed']

def get_bits(g):
    return g['bits']

def set_state(g, s):
    g['seed'] = s
    return g['seed']

def update_state(g):
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

def is_generator(arg):
    return isinstance(arg, dict) and 'bits' in arg and 'seed' in arg and isinstance(arg['bits'], int) \
    and (arg['bits'] == 32 or arg['bits'] == 64) and isinstance(arg['seed'], int) and arg['seed'] > 0 and len(arg) == 2

def generator_equals(g1, g2):
    return is_generator(g1) and is_generator(g2) and g1['bits'] == g2['bits'] and g1['seed'] == g2['seed']

def generator_to_str(g):
    return 'xorshift{}(s={})'.format(g['bits'], g['seed'])

def gen_rnd_num(g, n):
    update_state(g)
    return 1 + (get_state(g) % n)

def gen_rnd_char(g, c):
    update_state(g)
    string = ''.join([chr(x) for x in range(ord('A'), ord(c) + 1)])
    return string[get_state(g) % len(string)]

def create_coord(col, row):
    if not (isinstance(col, str) and 'A' <= col <= 'Z' and len(col) == 1 and isinstance(row, int) and 1 <= row <= 99):
        raise ValueError('create_coord: invalid arguments')
    return (col, row)

def get_col(c):
    return c[0]

def get_row(c):
    return c[1]

def is_coord(arg):
    return isinstance(arg, tuple) and isinstance(arg[0], str) and len(arg[0]) == 1 and isinstance(arg[1], int) and 'A' <= arg[0] <= 'Z' and len(arg[0]) == 1 and 1 <= arg[1] <= 99 and len(arg) == 2

def coord_equal(c1, c2):
    return is_coord(c1) and is_coord(c2) and get_col(c1) == get_col(c2) and get_row(c2) == get_row(c1)

def coord_to_str(c):
    return '{}{:0>2}'.format(get_col(c), get_row(c))

def str_to_coord(s):
    return (s[0],int(s[1:]))

def get_coord_neighbors(c):
    if get_col(c) == 'A':
        if get_row(c) == 1:
            return (('B', 1), ('B', 2), ('A', 2))
        elif get_row(c) == 99:
            return (('A', 98), ('B', 98), ('B', 99))
        else:
            return (('A', get_row(c)-1), ('B', get_row(c)-1), ('B', get_row(c)), ('B', get_row(c)+1), ('A', get_row(c)+1))
            
    elif get_col(c) == 'Z':
        if get_row(c) == 1:
            return (('Z', 2), ('Y', 2), ('Y', 1))
        elif get_row(c) == 99:
            return (('Y', 98), ('Z', 98), ('Y', 99))
        else:
            return (('Y', get_row(c)-1), ('Z', get_row(c)-1), ('Z', get_row(c)+1), ('Y', get_row(c)+1), ('Y', get_row(c)))

    else:
        if get_row(c) == 1:
            return ((chr(ord(get_col(c)) + 1), 1), (chr(ord(get_col(c)) + 1), 2), (get_col(c), 2), (chr(ord(get_col(c)) - 1), 2), (chr(ord(get_col(c)) - 1), 1))
        elif get_row(c) == 99:
            return ((chr(ord(get_col(c)) - 1), 98), (get_col(c), 98), (chr(ord(get_col(c)) + 1), 98), (chr(ord(get_col(c)) + 1), 99), (chr(ord(get_col(c)) - 1), 99))
        else:
            return ((chr(ord(get_col(c)) - 1), get_row(c)-1), (get_col(c), get_row(c)-1), (chr(ord(get_col(c)) + 1), get_row(c)-1), (chr(ord(get_col(c)) + 1), get_row(c)), \
                    (chr(ord(get_col(c)) + 1), get_row(c)+1), (get_col(c), get_row(c)+1), (chr(ord(get_col(c)) - 1), get_row(c)+1), (chr(ord(get_col(c)) - 1), get_row(c)))

def get_rnd_coord(c, g):
    return create_coord(gen_rnd_char(g, get_col(c)), gen_rnd_num(g, get_row(c)))

def create_plot():
    return {'state': '#', 'mine': False}

def copy_plot(p):
    return p.copy()

def clear_plot(p):
    p['state'] = '?/X'
    return p

def mark_plot(p):
    p['state'] = '@'
    return p

def unmark_plot(p):
    p['state'] = '#'
    return p

def hide_mine(p):
    p['mine'] = True
    return p

def is_plot(arg):
    if isinstance(arg, dict) and 'state' in arg \
        and isinstance(arg['state'], str) and (arg['state'] == '#' or arg['state'] == '@' or arg['state'] == '?/X') \
        and 'mine' in arg and isinstance(arg['mine'], bool) and (arg['mine'] == True or arg['mine'] == False) and len(arg) == 2:
            return True
    return False

def is_plot_flag(p):
    return p['state'] == '#'

def is_plot_mark(p):
    return p['state'] == '@'

def is_plot_clear(p):
    return p['state'] == '?/X'

def is_plot_mine(p):
    return p['mine']

def plot_equals(p1, p2):
    return is_plot(p1) and is_plot(p2) and p1['state'] == p2['state'] and p1['mine'] == p2['mine']

def plot_to_str(p):
    if p['state'] == '?/X':
        if p['mine']:
            return 'X'
        else:
            return '?'
    return p['state']

def toggle_flag(p):
    if is_plot_mark(p):
        unmark_plot(p)
        return True
    elif is_plot_flag(p):
        mark_plot(p)
        return True
    return False

def create_field(c, l):
    if not (isinstance(c, str) and 'A' <= c <= 'Z' and len(c) == 1 and isinstance(l, int) and 1 <= l <= 99):
        raise ValueError('create_field: invalid arguments')
    m = []
    row = 1
    while row <= l:
        col = ord('A')
        while col <= ord(c):
            m += [[create_plot(), create_coord(chr(col), row)]]
            col += 1
        row += 1
    return m

def copy_field(m):
    r = []
    for items in m:
        r += [[copy_plot(items[0]), items[1]]]
    return r

def get_last_col(m):
    return sorted(m, key = lambda x: x[1][0], reverse = True)[0][1][0]

def get_last_row(m):
    return sorted(m, key = lambda x: x[1][1], reverse = True)[0][1][1]

def get_plot(m, c):
    for item in m:
        if item[1] == c:
            return item[0]

def get_coord(m, s):
    tup = ()
    if s == 'clear':
        for item in m:
            if item[0]['state'] == '?/X':
                tup += (item[1],)
    elif s == 'flag':
        for item in m:
            if item[0]['state'] == '#':
                tup += (item[1],)
    elif s == 'mark':
        for item in m:
            if item[0]['state'] == '@':
                tup += (item[1],)
    elif s == 'mine':
        for item in m:
            if item[0]['mine']:
                tup += (item[1],)
    return tup

def get_mines_neighbor(m, c):
    num = 0
    for coord in get_coord_neighbors(c):
        if is_field_coord(m, coord) and is_plot_mine(get_plot(m, coord)):
            num += 1
    return num

def is_field(arg): 
    if isinstance(arg, list):
        for item in arg:
            if not (is_plot(item[0]) and is_coord(item[1]) and 10 <= len(arg) <= 26 * 99):
                return False
        return True
    return False

def is_field_coord(m, c):
    for item in m:
        if item[1] == c:
            return True
    return False

def field_equals(m1, m2):
    Len = 0
    if is_field(m1) and is_field(m2) and len(m1) == len(m2):
        for item in m1:
            if item in m2:
               Len += 1
        return len(m1) == Len
    return False

def field_to_str(m):
    def plot_to_str_(p):
        if is_plot_flag(p): return '#'
        elif is_plot_mark(p): return '@'
        elif is_plot_clear(p):
        if not is_plot_mine(p):
                if get_mine_neighbors(m, z[1]) == 0: return ' '
                else: return str(get_mine_neighbors(m, z[1]))
            else: return 'X'
        return p['state']

    cols = '   ' + ''.join([chr(x) for x in range(ord('A'), ord(get_last_col(m)) + 1)])+ '\n  '
    string = cols + '+'
    len_cols = len(''.join(cols.split()))
    for y in range(len_cols):
        string += '-'
    string += '+'
    limit = string[4 + len_cols: 4 + 2 * len_cols + 4]
    for y in range(1, get_last_row(m) + 1):
        string += '\n' + '{:0>2}'.format(y) + '|'
        for z in m:
            if z[1][1] == y:
                string += plot_to_str_(z[0])
        string += '|'
    string += '\n' + limit
    return string

def place_mines(m, c, g, n):
    coord_mines = ()
    i = 0
    while i < n:
        coord = get_rnd_coord(create_coord(get_last_col(m), get_last_row(m)), g)
        if coord != c and coord not in get_coord_neighbors(c) and coord not in coord_mines:
            hide_mine(get_plot(m, coord))
            coord_mines += (coord,)
            i += 1
    return m

def clear_field(m, c):
    clear_plot(get_plot(m, c))
    clear = [[c,True]]
    for coord in get_coord_neighbors(c):
            if is_field_coord(m, coord):
                if is_plot_mine(get_plot(m, coord)):
                    return m
    for coord in get_coord_neighbors(c):
            if is_field_coord(m, coord) and not is_plot_clear(get_plot(m, coord)) and not is_plot_mine(get_plot(m, coord)) and not is_plot_mark(get_plot(m, coord)):
                clear_plot(get_plot(m, coord))
                clear += [[coord, False]]
    for item in clear:
        if not item[1]:
            clear_field(m, item[0])     
    return m

def win(m):
    plots_mine = []
    for coord in get_coord(m, 'mine'):
        plots_mine += [get_plot(m, coord)]
    for item in m:
        if item[0] not in plots_mine:
            if not is_plot_clear(item[0]):
                return False
    return True

def round(m):
    global play
    input_wrong = True
    while input_wrong:
        turnCM = input('Choose an action, [C]lean or [M]ark:')
        if turnCM == 'L' or turnCM == 'M': input_wrong = False
    input_wrong = True
    while input_wrong:
        turnCoord = input('Choose a coordinate:')
        play = turnCoord
        if 'A' <= turnCoord[0] <= get_last_col(m) and len(turnCoord) == 3: 
            for L in turnCoord[1:]:                
                if '0' <= L <= '9':
                    if is_coord((turnCoord[0], int(turnCoord[1:]))) and is_field_coord(m, str_to_coord(turnCoord)):
                        input_wrong = False
        if win(m): return False
        if turnCM == 'C': clear_field(m, str_to_coord(turnCoord))
        elif turnCM == 'M':toggle_flag(get_plot(m, str_to_coord(turnCoord)))
    if str_to_coord(play) in get_coord(m, 'mine'):
            if not (is_plot_mark(get_plot(m, str_to_coord(play)))):
                return False
    return True

def mines(col, row, n, d, s):
    if not (isinstance(col, str) and len(col) == 1 and 'A' <= col <= 'Z' and isinstance(row, int) and 1 <= row <= 99 \
        and isinstance(n, int) and 1 <= n <= (abs(ord('A') - ord(col)) + 1) * row - 1 - 3 \
        and isinstance(d, int) and isinstance(s, int) and s > 0 and ((d == 32 and s <= 2 ** 32 - 1) or (d == 64 and s <= 2 ** 64 - 1))):
        raise ValueError('mines: invalid arguments')

    m = create_field(col, row)
    def marked_plots(m):
        marked_plot = 0
        for item in m:
            if is_plot_mark(item[0]):
                marked_plot += 1
        return marked_plot
    print('   [Flags {}/{}]'.format(marked_plots(m), n))
    print(field_to_str(m))
    
    input_wrong = True
    while input_wrong:
        turnCoord = input('Choose a coordinate:')
        if len(turnCoord) == 3 and is_coord(str_to_coord(turnCoord)) and is_coord((turnCoord[0], int(turnCoord[1:]))) and is_field_coord(m, str_to_coord(turnCoord)):
            input_wrong = False
    place_mines(m, str_to_coord(turnCoord), create_generator(d, s), n)
    clear_field(m, str_to_coord(turnCoord))
    print('   [Flags {}/{}]'.format(marked_plots(m), n))
    print(field_to_str(m))
    
    while not win(m):
        global play
        round(m)
        print('   [Flags {}/{}]'.format(marked_plots(m), n))
        print(field_to_str(m))
        if str_to_coord(play) in get_coord(m, 'mine'):
            if not (is_plot_mark(get_plot(m, str_to_coord(play)))):
                print('BOOM!')
                return False
    print('WIN!')
    return True
