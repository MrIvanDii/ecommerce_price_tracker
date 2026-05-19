import re
from typing import Optional, Dict


def extract_year(product_name: str) -> Optional[str]:
    match = re.search(r"\b(20\d{2}|19\d{2})\b", product_name)
    if not match:
        return None
    return match.group(1)


def normalize_product_name(product_name: Optional[str]) -> Optional[str]:
    if not product_name:
        return None

    name = product_name

    replacements = {
        "1 4Oz": "1/4oz",
        "1 2Oz": "1/2oz",
        "1 10Oz": "1/10oz",
        "1Oz": "1oz",
        "Oz": "oz",
        "Kc3": "KC3",
        "9167": "916.7",
        "9999": "999.9",
    }

    for old, new in replacements.items():
        name = name.replace(old, new)

    return " ".join(name.split()).strip()


def extract_weight(product_name: str) -> Optional[str]:
    text = product_name.lower()

    # --- Граммы ---
    gram_match = re.search(r"\b(\d+(?:\.\d+)?)\s*g\b", text)
    if gram_match:
        grams = float(gram_match.group(1))
        return f"{grams}g"

    # --- Стандартные oz паттерны ---
    oz_patterns = [
        (r"\b1\s*2\s*ounce\b", "1/2oz"),
        (r"\b1\s*ounce\b", "1oz"),
        (r"\bone[\s-]ounce\b", "1oz"),
        (r"\bone[\s-]oz\b", "1oz"),
        (r"\b1\s*/\s*10\s*oz\b", "1/10oz"),
        (r"\b1\s*10\s*oz\b", "1/10oz"),
        (r"\btenth[\s-]ounce\b", "1/10oz"),
        (r"\b1\s*/\s*4\s*oz\b", "1/4oz"),
        (r"\b1\s*4\s*oz\b", "1/4oz"),
        (r"\bquarter[\s-]ounce\b", "1/4oz"),
        (r"\b1\s*/\s*2\s*oz\b", "1/2oz"),
        (r"\b1\s*2\s*oz\b", "1/2oz"),
        (r"\bhalf[\s-]oz\b", "1/2oz"),
        (r"\bhalf[\s-]ounce\b", "1/2oz"),
        (r"\b1\s*oz\b", "1oz"),
    ]

    for pattern, normalized in oz_patterns:
        if re.search(pattern, text):
            return normalized

    # --- Sovereign паттерны (от специфичных к общим) ---
    if re.search(r"\bquarter[\s-]sovereigns?\b", text):
        return "1/4sovereign"
    if re.search(r"\bdouble[\s-]sovereigns?\b", text):
        return "2sovereign"
    if re.search(r"\bhalf[\s-]sovereigns?\b|½\s*sovereigns?\b", text):
        return "1/2sovereign"
    if re.search(r"\bfull[\s-]sovereigns?\b", text) or re.search(r"\bsovereigns?\b", text):
        return "1sovereign"

    return None


def extract_coin_family(product_name: str) -> Optional[str]:
    text = product_name.lower()

    if any(k in text for k in ["american eagle", "us eagle", "usa eagle"]):
        return "eagle"

    queens_beast_animals = [
        "lion of england",
        "red dragon",
        "unicorn of scotland",
        "yale of beaufort",
        "white greyhound",
        "falcon of the plantagenets",
        "falcon pf the plantagenets",
        "griffin of edward",
        "black bull",
        "white horse of hanover",
        "white lion of mortimer",
        "white lion of england",
    ]

    if any(animal in text for animal in queens_beast_animals):
        return "queens_beast"

    families = {
        "lion and the eagle": "lion_eagle",
        "st george":          "st_george",
        "tudor":              "tudor_beast",
        "maple leaf":         "maple_leaf",
        "britannia":          "britannia",
        "krugerrand":         "krugerrand",
        "sovereign":          "sovereign",
        "maple":              "maple_leaf",
        "kangaroo":           "kangaroo",
        "buffalo":            "buffalo",
        "koala":              "koala",
        "panda":              "panda",
        "philharmonic":       "philharmonic",
    }

    for keyword, normalized in families.items():
        if keyword in text:
            return normalized

    return None


def extract_product_metadata(product_name: Optional[str]) -> Dict[str, Optional[str]]:
    if not product_name:
        return {"year": None, "weight": None, "coin_family": None}

    return {
        "year":        extract_year(product_name),
        "weight":      extract_weight(product_name),
        "coin_family": extract_coin_family(product_name),
    }


def weight_to_oz(weight: Optional[str]) -> Optional[float]:
    if not weight:
        return None

    weight_map = {
        "1oz":           1.0,
        "1/2oz":         0.5,
        "1/4oz":         0.25,
        "1/10oz":        0.1,
        "1sovereign":    0.2354,
        "1/2sovereign":  0.1177,
        "1/4sovereign":  0.0589,  # 1.83g gold content / 31.1035
        "2sovereign":    0.4708,
    }

    if weight in weight_map:
        return weight_map[weight]

    gram_match = re.match(r"^(\d+(?:\.\d+)?)g$", weight)
    if gram_match:
        grams = float(gram_match.group(1))
        return round(grams / 31.1035, 6)

    return None


def calculate_price_per_oz(price: Optional[float], weight: Optional[str]) -> Optional[float]:
    weight_oz = weight_to_oz(weight)

    if price is None or weight_oz is None or weight_oz == 0:
        return None

    return round(price / weight_oz, 2)