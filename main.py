from time import time
from typing import List

CELLS_IN_CUBE = 27
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

    dx = 0
    dy = 0
    dz = 0
    dr = 0
    ds = 0

    def __init__(self, shard_num: int, cells: List[int], dx_max: int, dy_max: int, dz_max: int) -> None:
        self.shard_num = shard_num
        self.cells = cells
        self.dx_max = dx_max
        self.dy_max = dy_max
        self.dz_max = dz_max
        self.dr_max = 3
        self.ds_max = 5

    def position(self, cube) -> bool:
        aligned_cells = self.cells
        # apply alignments
        if self.dx:
            aligned_cells = list(map(lambda x: x + 1 * self.dx, aligned_cells))
        if self.dy:
            aligned_cells = list(map(lambda y: y + 3 * self.dy, aligned_cells))
        if self.dz:
            aligned_cells = list(map(lambda z: z + 9 * self.dz, aligned_cells))
        if self.dr:
            aligned_cells = list(map(lambda i: ROTATE[self.dr - 1][i], aligned_cells))
        if self.ds:
            aligned_cells = list(map(lambda i: SIDE[self.ds - 1][i], aligned_cells))
        for cell in aligned_cells:
            if cube[cell] == 0:
                cube[cell] = self.shard_num
            else:
                return False
        return True

class Cube:
    def __init__(self, shards: List[Shard]) -> None:
        self.shards = shards

    def empty(self) -> None:
        self.cube = [0] * CELLS_IN_CUBE

    def print(self) -> None:
        print(self.cube[0:3], self.cube[9:12], self.cube[18:21])
        print(self.cube[3:6], self.cube[12:15], self.cube[21:24])
        print(self.cube[6:9], self.cube[15:18], self.cube[24:27])

    def process(self) -> None:
        # init all
        for shard in self.shards:
            shard.dx = shard.dx_max
            shard.dy = shard.dy_max
            shard.dz = shard.dz_max
            shard.dr = shard.dr_max
            shard.ds = shard.ds_max
        lap_time = time()
        # iterate all
        while True:
            if time() - lap_time > 10:
                print(
                    (self.shards[0].dx, self.shards[0].dy, self.shards[0].dr, self.shards[0].ds),
                    (self.shards[1].dx, self.shards[1].dy, self.shards[1].dr, self.shards[1].ds),
                    (self.shards[2].dx, self.shards[2].dy, self.shards[2].dr, self.shards[2].ds),
                    (self.shards[3].dx, self.shards[3].dy, self.shards[3].dr, self.shards[3].ds),
                    (self.shards[4].dx, self.shards[4].dy, self.shards[4].dr, self.shards[4].ds),
                    (self.shards[5].dx, self.shards[5].dy, self.shards[5].dr, self.shards[5].ds),
                    self.shards[5].dz
                )
                lap_time = time()
            sum_indexes = 0
            for shard in self.shards:
                sum_indexes += shard.dx
                sum_indexes += shard.dy
                sum_indexes += shard.dz
                sum_indexes += shard.dr
                sum_indexes += shard.ds
            if sum_indexes == 0:
                print('no positions')
                return
            else:
                self.empty()
                if (
                    self.shards[5].position(self.cube) and
                    self.shards[4].position(self.cube) and
                    self.shards[3].position(self.cube) and
                    self.shards[2].position(self.cube) and
                    self.shards[1].position(self.cube) and
                    self.shards[0].position(self.cube)
                ):
                    self.print()
                    return
            self.iterate()

    def iterate(self) -> None:
        # shard 0
        if self.shards[0].dx:
            self.shards[0].dx -= 1
        else:
            self.shards[0].dx = self.shards[0].dx_max

            if self.shards[0].dy:
                self.shards[0].dy -= 1
            else:
                self.shards[0].dy = self.shards[0].dy_max

                if self.shards[0].dr:
                    self.shards[0].dr -= 1
                else:
                    self.shards[0].dr = self.shards[0].dr_max

                    if self.shards[0].ds:
                        self.shards[0].ds -= 1
                    else:
                        self.shards[0].ds = self.shards[0].ds_max
                        # shard 1
                        if self.shards[1].dx:
                            self.shards[1].dx -= 1
                        else:
                            self.shards[1].dx = self.shards[1].dx_max

                            if self.shards[1].dy:
                                self.shards[1].dy -= 1
                            else:
                                self.shards[1].dy = self.shards[1].dy_max

                                if self.shards[1].dr:
                                    self.shards[1].dr -= 1
                                else:
                                    self.shards[1].dr = self.shards[1].dr_max

                                    if self.shards[1].ds:
                                        self.shards[1].ds -= 1
                                    else:
                                        self.shards[1].ds = self.shards[1].ds_max
                                        # shard 2
                                        if self.shards[2].dx:
                                            self.shards[2].dx -= 1
                                        else:
                                            self.shards[2].dx = self.shards[2].dx_max

                                            if self.shards[2].dy:
                                                self.shards[2].dy -= 1
                                            else:
                                                self.shards[2].dy = self.shards[2].dy_max

                                                if self.shards[2].dr:
                                                    self.shards[2].dr -= 1
                                                else:
                                                    self.shards[2].dr = self.shards[2].dr_max

                                                    if self.shards[2].ds:
                                                        self.shards[2].ds -= 1
                                                    else:
                                                        self.shards[2].ds = self.shards[2].ds_max
                                                        # shard 3
                                                        if self.shards[3].dx:
                                                            self.shards[3].dx -= 1
                                                        else:
                                                            self.shards[3].dx = self.shards[3].dx_max

                                                            if self.shards[3].dy:
                                                                self.shards[3].dy -= 1
                                                            else:
                                                                self.shards[3].dy = self.shards[3].dy_max

                                                                if self.shards[3].dr:
                                                                    self.shards[3].dr -= 1
                                                                else:
                                                                    self.shards[3].dr = self.shards[3].dr_max

                                                                    if self.shards[3].ds:
                                                                        self.shards[3].ds -= 1
                                                                    else:
                                                                        self.shards[3].ds = self.shards[3].ds_max
                                                                        # shard 4
                                                                        if self.shards[4].dx:
                                                                            self.shards[4].dx -= 1
                                                                        else:
                                                                            self.shards[4].dx = self.shards[4].dx_max

                                                                            if self.shards[4].dy:
                                                                                self.shards[4].dy -= 1
                                                                            else:
                                                                                self.shards[4].dy = self.shards[4].dy_max

                                                                                if self.shards[4].dr:
                                                                                    self.shards[4].dr -= 1
                                                                                else:
                                                                                    self.shards[4].dr = self.shards[4].dr_max

                                                                                    if self.shards[4].ds:
                                                                                        self.shards[4].ds -= 1
                                                                                    else:
                                                                                        self.shards[4].ds = self.shards[4].ds_max
                                                                                        # shard 5
                                                                                        if self.shards[5].dx:
                                                                                            self.shards[5].dx -= 1
                                                                                        else:
                                                                                            self.shards[5].dx = self.shards[5].dx_max

                                                                                            if self.shards[5].dy:
                                                                                                self.shards[5].dy -= 1
                                                                                            else:
                                                                                                self.shards[5].dy = self.shards[5].dy_max

                                                                                                if self.shards[5].dr:
                                                                                                    self.shards[5].dr -= 1
                                                                                                else:
                                                                                                    self.shards[5].dr = self.shards[5].dr_max

                                                                                                    if self.shards[5].ds:
                                                                                                        self.shards[5].ds -= 1
                                                                                                    else:
                                                                                                        self.shards[5].ds = self.shards[5].ds_max
                                                                                                        # shard 5 - only shard with dz
                                                                                                        if self.shards[5].dz:
                                                                                                            self.shards[5].dz -= 1
                                                                                                        else:
                                                                                                            self.shards[5].dz = self.shards[5].dz_max


if __name__ == '__main__':
    start_time = time()
    cube = Cube(
        [
            Shard(1, [3, 9, 10, 12, 18], 1, 1, 0),
            Shard(2, [3, 9, 10, 12, 21], 1, 1, 0),
            Shard(3, [3, 12, 18, 21], 2, 1, 0),
            Shard(4, [0, 3, 9, 10, 18], 1, 1, 0),
            Shard(5, [0, 9, 12, 18], 2, 1, 0),
            Shard(6, [0, 1, 9, 12], 1, 1, 1),
        ]
    )
    cube.process()
    print(time() - start_time)
