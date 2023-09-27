from time import time
from typing import List
import logging

CELLS_IN_CUBE = 27
ORIENTATIONS = 4
SIDES = 6
ROTATE = [
    [2, 5, 8, 1, 4, 7, 0, 3, 6, 11, 14, 17, 10, 13, 16, 9, 12, 15, 20, 23, 26, 19, 22, 25, 18, 21, 24],
    [8, 7, 6, 5, 4, 3, 2, 1, 0, 17, 16, 15, 14, 13, 12, 11, 10, 9, 26, 25, 24, 23, 22, 21, 20, 19, 18],
    [6, 3, 0, 7, 4, 1, 8, 5, 2, 15, 12, 9, 16, 13, 10, 17, 14, 11, 24, 21, 18, 25, 22, 19, 26, 23, 20]
]
SIDE = [
    [18,  9,  0, 21, 12,  3, 24, 15,  6, 19, 10,  1, 22, 13,  4, 25, 16,  7, 20, 11,  2, 23, 14,  5, 26, 17,  8],
    [ 2, 21, 20,  5, 14, 23,  8, 17, 26,  1, 10, 19,  4, 13, 22,  7, 16, 25,  0,  9, 18,  3, 12, 21,  6, 15, 24],
    [18, 10, 20,  9, 10, 11,  0,  1,  2, 21, 22, 23, 12, 13, 14,  3,  4,  5, 24, 25, 26, 15, 16, 17,  6,  7,  8],
    [ 6,  7,  8, 15, 16, 17, 24, 25, 26,  3,  4,  5, 12, 13, 14, 21, 22, 23,  0,  1,  2,  9, 10, 11, 18, 19, 20],
    [24, 25, 26, 21, 22, 23, 18, 19, 20, 15, 16, 17, 12, 13, 14,  9, 10, 11,  6,  7,  8,  3,  4,  5,  0,  1,  2]
]


class Shard:

    def __init__(self, shard_num: int, cells: List[int], dx_max: int, dy_max: int, dz_max: int) -> None:
        self.shard_num = shard_num
        self.cells = cells
        self.dx_max = dx_max
        self.dy_max = dy_max
        self.dz_max = dz_max
        self.aligned_cells = []
        self.calc_alignments()
        self.aligned_cells_count = len(self.aligned_cells)
        logging.error(f'shard {shard_num}, count {self.aligned_cells_count}')

    def calc_alignments(self) -> None:
        for dx in range(self.dx_max):
            for dy in range(self.dy_max):
                for dz in range(self.dz_max):
                    for dr in range(ORIENTATIONS):
                        for ds in range(SIDES):
                            aligned_cells = self.cells
                            # apply alignments
                            if dx:
                                aligned_cells = list(map(lambda x: x + 1 * dx, aligned_cells))
                            if dy:
                                aligned_cells = list(map(lambda y: y + 3 * dy, aligned_cells))
                            if dz:
                                aligned_cells = list(map(lambda z: z + 9 * dz, aligned_cells))
                            if dr:
                                aligned_cells = list(map(lambda i: ROTATE[dr - 1][i], aligned_cells))
                            if ds:
                                aligned_cells = list(map(lambda i: SIDE[ds - 1][i], aligned_cells))
                            self.aligned_cells.append(aligned_cells)
                            #logging.info(f'{aligned_cells}')

    def position(self, arr_in):
        arr_out = []
        for cube_in in arr_in:
            for shard in self.aligned_cells:
                cube = cube_in.copy()
                good_cube = True
                for cell in shard:
                    if cube[cell] == 0:
                        cube[cell] = self.shard_num
                    else:
                        good_cube = False
                        break
                if good_cube:
                    arr_out.append(cube)
        return arr_out

class Cube:
    def __init__(self, shards: List[Shard]) -> None:
        self.shards = shards

    def empty(self) -> None:
        self.cube = [0] * CELLS_IN_CUBE

    def print(self) -> None:
        logging.info(f'{self.cube[0:3], self.cube[9:12], self.cube[18:21]}')
        logging.info(f'{self.cube[3:6], self.cube[12:15], self.cube[21:24]}')
        logging.info(f'{self.cube[6:9], self.cube[15:18], self.cube[24:27]}')

    def process(self) -> None:
        start_time = time()
        # iterate all
        arr = [[0] * CELLS_IN_CUBE]
        for shard in self.shards:
            arr = shard.position(arr)
            print(shard.shard_num, len(arr), time() - start_time)
        self.cube = arr[0]
        self.print()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename="main3.log", filemode="w")
    start_time = time()
    cube = Cube(
        [
            Shard(1, [3, 9, 10, 12, 18], 2, 2, 1),
            Shard(2, [3, 9, 10, 12, 21], 2, 2, 1),
            Shard(3, [3, 12, 18, 21], 3, 2, 1),
            Shard(4, [0, 3, 9, 10, 18], 2, 2, 1),
            Shard(5, [0, 9, 12, 18], 3, 2, 1),
            Shard(6, [0, 1, 9, 12], 2, 2, 2),
        ]
    )
    cube.process()
    print(time() - start_time)
