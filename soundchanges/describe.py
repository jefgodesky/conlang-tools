from typing import List


def oxford_comma(items: List[str]) -> str:
    if len(items) < 1:
        return ""
    elif len(items) == 1:
        return items[0]
    elif len(items) == 2:
        return items[0] + " and " + items[1]
    else:
        return ", ".join(items[:-1]) + ", and " + items[-1]
