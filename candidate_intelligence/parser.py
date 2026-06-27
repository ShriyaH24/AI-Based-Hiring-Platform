import gzip
import orjson
from tqdm import tqdm


def load_candidates(file_path):
    """
    Generator that streams candidates one by one.
    Works for both .jsonl and .jsonl.gz
    """

    if file_path.endswith(".gz"):
        file = gzip.open(file_path, "rb")
    else:
        file = open(file_path, "rb")

    with file as f:
        for line in tqdm(f):
            yield orjson.loads(line)