from operator import attrgetter
from itertools import groupby

def flatten(items: list[list[str]]) -> list[str]:
    return [item for sublist in items for item in sublist]

def split_and_strip(input: str) -> list[str]:
    return list(map(str.strip, input.split()))

def zip_items_in_shifted_pairs(items: list[int]) -> list[tuple[int, int]]:
    return list(zip(items, items[1:]))

def search_index_by_any_match(matches: list[str] | str, items: list[str]) -> int | None:
    return next(
        (index for index, item in enumerate(items) if item in matches),
        None
    )

def remove_last_str_items_until_digit_found(items: list[str]) -> list[str]:
    last_index_with_valid_digit = max(
        (index for index, item in enumerate(items) if is_valid_float(item)),
        default=-1
    )

    return items[:last_index_with_valid_digit + 1]

def is_valid_float(input) -> bool:
    return input.replace('.', '').isdigit()

def remove_duplicates_for_attribute(attribute: str, items):
    items.sort(key=attrgetter(attribute))
    
    return [next(group) for _, group in groupby(items, key=attrgetter(attribute))]
