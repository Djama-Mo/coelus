def input_field_size():
    x_field = int(input('Enter the x-coord of field: '))
    y_field = int(input('Enter the y-coord of field: '))
    return x_field, y_field


def input_tetramino_size(l_flag=''):
    count = int(input(f'Enter a count of all tuples of \033[31m{l_flag}tetraminos\033[0m: '))
    tetramino_list = [] * count
    for el in range(count):
        print(f'\t\t({el + 1})')
        x_tetramino = int(input(f'Enter the x-coord of {l_flag}tetramino: '))
        y_tetramino = int(input(f'Enter the y-coord of {l_flag}tetramino: '))
        single_count = int(input(f'Enter a count of this {l_flag}tetramino: '))
        tetramino_list.append(((x_tetramino, y_tetramino), single_count))
    return tetramino_list


def check_coords_size(x_field_check, y_field_check, x_block_check, y_block_check):
    if not (x_block_check > x_field_check and y_block_check > x_field_check
            or x_block_check > y_field_check and y_block_check > y_field_check):
        return True


def add_block(field: list, block_coords: tuple):
    empty_cells = 0
    x_empty_cell_index = 0
    x_len_block = block_coords[0]
    y_len_block = block_coords[1]
    cur_y = -1
    block_square = x_len_block * y_len_block
    for row in field:
        cur_y += 1
        if y_len_block and len(field) - cur_y >= y_len_block:
            for cell in row:
                if cell == ' ':
                    empty_cells += 1
                else:
                    empty_cells = 0
            if empty_cells >= block_coords[0]:
                cur_index = x_empty_cell_index
                for empty_cell in row:
                    if empty_cell != ' ':
                        x_empty_cell_index += 1
                        cur_index = x_empty_cell_index
                        continue
                    if x_len_block:
                        row[cur_index] = '+'
                        block_square -= 1
                        x_len_block -= 1
                        cur_index += 1
            else:
                continue
        else:
            return
        x_len_block = block_coords[0]
        y_len_block -= 1
        if block_square == 0:
            return True


def get_coords(block: tuple):
    x_block = block[0]
    y_block = block[1]
    x_offset = round(x_block / 2)
    y_offset = round(y_block / 2)
    coords_zero = []
    coords_one = []
    coords_two = []
    coords_three = []
    for i in range(x_block):
        coords_zero.append((0, i))
        coords_one.append((-i + x_offset, 0))
        coords_two.append((y_offset, -i + x_offset))
        coords_three.append((i, y_offset))
    for j in range(1, y_block):
        coords_zero.append((j, 0))
        coords_one.append((x_offset, j))
        coords_two.append((-j + y_offset, x_offset))
        coords_three.append((0, -j + y_offset))
    return [coords_zero, coords_one, coords_two, coords_three]


def find_place(e_coords, h_fset, w_size, block):
    b_coords_list = get_coords(block)
    conc = 0
    max_neighbour = 0
    result = 0
    for b_coords in b_coords_list:
        for offset in range(w_size):
            for b_tuple in b_coords:
                for e_tuple in e_coords:
                    if b_tuple[0] + offset == e_tuple[0] and b_tuple[1] + h_fset == e_tuple[1]:
                        conc += 1
                        break
                if conc == 0:
                    break
            if conc == len(b_coords):
                busy_coords = []
                for elem in b_coords:
                    busy_coords.append((elem[0] + offset, elem[1] + h_fset))
                empty_coords = list(set(e_coords) - set(busy_coords))
                neighbours = empty_neighbours(empty_coords)
                if neighbours > max_neighbour:
                    max_neighbour = neighbours
                    result = b_coords, offset, h_fset
            conc = 0
    return result


def distance(e_tuple_1, e_tuple_2):
    return ((e_tuple_1[0] - e_tuple_2[0]) ** 2 + (e_tuple_1[1] - e_tuple_2[1]) ** 2) ** (1 / 2)


def empty_neighbours(empty_coords):
    max_n = 0
    neighbours = 1
    empty_coords.sort(key=lambda x: x[0])
    for i in range(len(empty_coords)):
        for j in range(0, len(empty_coords)):
            if distance(empty_coords[i], empty_coords[j]) == 1:
                neighbours += 1
                # i = j
                break
        if neighbours > max_n:
            max_n = neighbours
        neighbours = 1
    return max_n


def add_l_block(field: list, block_coords: tuple):
    empty_x = 0
    cur_y = -1
    x_block = block_coords[0]
    y_block = block_coords[1]
    coords = []
    block_square = x_block + y_block - 1
    coord_max = max(x_block, y_block)
    result = 0
    for row in field:
        cur_y += 1
        for cell in row:
            if cell == ' ':
                coords.append((empty_x, cur_y))
            empty_x += 1
        empty_cells_in_row = len(row) - empty_x
        if not empty_cells_in_row:
            empty_x = 0
        if len(coords) >= block_square:
            if cur_y < coord_max:
                h_fset = 0
            else:
                h_fset = cur_y - 1
            result = find_place(e_coords=coords, h_fset=h_fset, w_size=len(row), block=block_coords)
        if result:
            b_coords = result[0]
            offset = result[1]
            h_fset = result[2]
            for b_tuple in b_coords:
                _x = b_tuple[0] + offset
                _y = b_tuple[1] + h_fset
                field[_y][_x] = '+'
            return True


def main():
    input_mode = int(input('1 - Input from file\n2 - Input from keyboard:\n>>> '))
    if input_mode == 2:
        x_field_main, y_field_main = input_field_size()  # (x, y)
        tetramino_list_main = input_tetramino_size()  # [ ((x1, y1), c1), ((x2, y2), c2) ]
        print()
        l_tetramino_list_main = input_tetramino_size(l_flag='l-')
    else:
        with open('./input_file.txt', 'r') as fh:
            lns = fh.readlines()
            x_field_main, y_field_main = eval(lns[0].strip())
            tetramino_list_main = eval(lns[1].strip())
            l_tetramino_list_main = eval(lns[2].strip())

    square = x_field_main * y_field_main
    tetr_square = 0
    for tup in tetramino_list_main:
        x_tetr_tup = tup[0][0]
        y_tetr_tup = tup[0][1]
        tetr_square += x_tetr_tup * y_tetr_tup * tup[1]
        if not check_coords_size(x_field_main, y_field_main, x_tetr_tup, y_tetr_tup):
            print(False)
            return
    for tup in l_tetramino_list_main:
        x_l_tetr_tup = tup[0][0]
        y_l_tetr_tup = tup[0][1]
        tetr_square += (x_l_tetr_tup + y_l_tetr_tup - 1) * tup[1]
        if not check_coords_size(x_field_main, y_field_main, x_l_tetr_tup, y_l_tetr_tup):
            print(False)
            return
    if tetr_square > square:
        print(False)
        return
    empty_neighbours([(2, 2), (2, 1), (0, 2), (3, 2)])
    _field = [[' ' for _ in range(x_field_main)] for _ in range(y_field_main)]
    for sq_block in tetramino_list_main:
        for i in range(sq_block[1]):
            if not add_block(_field, sq_block[0]):
                print(False)
                return
    for l_block in l_tetramino_list_main:
        for i in range(l_block[1]):
            if not add_l_block(_field, l_block[0]):
                print(False)
                return
    _field.reverse()
    for el in _field:
        print(el)
    print('\n', '*' * 10, True, '*' * 10)


if __name__ == '__main__':
    main()
