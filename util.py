import json
import requests


class JsonConfig(object):
    @classmethod
    def load(self, filename) -> dict:
        try:
            with open(filename, 'r') as file:
                return json.load(file)
        except Exception as ex:
            print("Unable to load configuration from file {0}".format(filename))
            raise

    @classmethod
    def load_from_url(self, url) -> dict:
        try:
            return requests.get(url).json()
        except Exception as ex:
            print("Unable to load config from URL {0}".format(url))
            raise


Block = namedtuple("Block", "index data")


class BlockCache(object):
    def __init__(self, max_size: int):
        self.blocks = []
        self.current_index = 0
        self.max_size = max_size

    """ Adds blocks to cache, return delta """
    def add(self, blocks: List[Block]) -> List[Block]:
        new_blocks = []
        for block in blocks:
            if block not in self.blocks:
                new_blocks.append(block)
        self.blocks += new_blocks
        self.trim()
        return new_blocks

    """ Remove oldest blocks, reducing cache size to max_size"""
    def trim(self):
        i = len(self.blocks) - self.max_size
        if i > 0:
            self.blocks = self.blocks[i:]

    """ Updates index values, most recent block is assigned head index """
    def index_shift(self, head: int):
        head = head - len(self.blocks)
        for block in self.blocks:
            block.index = head
            head += 1
