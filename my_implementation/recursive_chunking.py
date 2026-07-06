# externals
from typing_extensions import List
from pydantic import StrictInt, StrictStr

# constants
CHUNK_SIZE = 200
CHUNK_OVERLAP = 80
SEPERATORS = [
    '\n\n', '\n', '. ', '! ', '? ', '; ', ', ', ' ', '',
]


def split_on_sep(
    text: StrictStr,
    sep: StrictStr,
) -> List[StrictStr]:
    if sep == '':
        return [text]
    splits = text.split(sep)
    return [s + sep for s in splits[:-1]] + [splits[-1]]


def merge_splits(
    splits: List[StrictStr],
    size: StrictInt,
    overlap: StrictInt,
) -> List[StrictStr]:
    chunks = []
    current: List[StrictStr] = []
    current_len = 0

    for split in splits:
        split_len = len(split)
        if current_len + split_len > size and current:
            chunks.append(''.join(current))
            # drop from the front until we're within overlap what's left becomes
            # the start of the next chunk
            while current and current_len > overlap:
                current_len -= len(current[0])
                current.pop(0)
        current.append(split)
        current_len += split_len

    if current:
        chunks.append(''.join(current))

    return chunks


def recursive_chunking(
    text: StrictStr,
    size: StrictInt = CHUNK_SIZE,
    overlap: StrictInt = CHUNK_OVERLAP,
    seperators: List[StrictStr] = SEPERATORS,
) -> List[StrictStr]:

    for idx, sep in enumerate(seperators):
        splits = split_on_sep(text, sep)

        if len(splits) == 1 and sep != '':
            # it means separator didn't split anything, try the next one
            continue

        good_splits: List[StrictStr] = []
        remaining_seps = seperators[idx + 1:]

        for s in splits:
            # still too big, go deeper with finer separators
            if len(s) > size and sep != '':
                good_splits.extend(recursive_chunking(s, size, overlap, remaining_seps))
            else:
                good_splits.append(s)

        return merge_splits(good_splits, size, overlap)

    # ran out of separators return it directly as a chunk
    return [text]
