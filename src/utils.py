from operator import attrgetter
from itertools import groupby
from pathlib import Path

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

def remove_last_str_items_until_digit_or_empty_found(items: list[str]) -> list[str]:
    last_index_with_valid_digit = max(
        (index for index, item in enumerate(items) if is_valid_float(item) or item == ""),
        default=-1
    )

    return items[:last_index_with_valid_digit + 1]

def is_valid_float(input) -> bool:
    return input.replace('.', '').isdigit()

def remove_duplicates_for_attribute(attribute: str, items, sort_by_attrib: str | None = None):
    if sort_by_attrib:
        items.sort(key=attrgetter(sort_by_attrib))
    
    return [next(group) for _, group in groupby(items, key=attrgetter(attribute))]

def is_path_of_format(path: Path, format_suffix_without_dot: str) -> bool:
    return path.suffix.lower() == f".{format_suffix_without_dot}"

def folder_path_to_files(folder: Path, format_suffix_without_dot: str) -> list[Path]:
    return list(folder.glob(f"*.{format_suffix_without_dot}"))

def resolve_path(path: str, format_suffix_without_dot: str) -> Path | list[Path]:
    """
    Translates a string into a path or list of paths
    """
    resolved_path = Path(path)

    if resolved_path.is_file():
        if not is_path_of_format(resolved_path, format_suffix_without_dot):
            raise ValueError(f"File must be {format_suffix_without_dot} format")

        return resolved_path

    elif resolved_path.is_dir():
        return folder_path_to_files(resolved_path, format_suffix_without_dot)
