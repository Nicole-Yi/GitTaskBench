import sys
from transparent_background import Remover

class SimpleProgress:
    def update(self, n=1):
        pass

try:
    from tqdm import tqdm
    progress = tqdm
except ImportError:
    progress = SimpleProgress

remover = Remover()
remover.process(
    input_path=sys.argv[1],
    output_path=sys.argv[2],
    type='green',
    progress=progress
)