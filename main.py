from time import time
from typing import List

CELLS_IN_CUBE = 27


class Shard:
    def __init__(self, level0: List[int], level1: List[int], level2: List[int]) -> None:
        pass


class Cube:
    def __init__(self, shards: List[Shard]) -> None:
        self.shards = shards
        self.empty()

    def empty(self) -> None:
        self.cube = [0] * CELLS_IN_CUBE

    def print(self) -> None:
        print(self.cube[0:3], self.cube[9:12], self.cube[18:21])
        print(self.cube[3:6], self.cube[12:15], self.cube[21:24])
        print(self.cube[6:9], self.cube[15:18], self.cube[24:27])

    def process(self) -> None:
        self.print()


if __name__ == '__main__':
    start_time = time()
    cube = Cube(
        [
            Shard([0,0,1,0], [1,1,1,0], [1,0,0,0]),
            Shard([0,0,2,0], [2,2,2,0], [0,0,2,0]),
            Shard([0,0,3,0], [0,0,3,0], [3,0,3,0]),
            Shard([4,0,4,0], [4,4,0,0], [4,0,0,0]),
            Shard([5,0,0,0], [5,0,5,0], [5,0,0,0]),
            Shard([6,6,0,0], [6,0,6,0], [0,0,0,0]),
        ]
    )
    cube.process()
    print(time() - start_time)
