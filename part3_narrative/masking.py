"""External-facing reseller-name masking helpers."""


def alias_for(reseller_id: str) -> str:
    """Convert RS019 to ALIAS-19, preserving the numeric suffix."""
    return f"ALIAS-{reseller_id[3:]}"


def assert_no_raw_names_leak(text: str, reseller_names: list[str]) -> bool:
    """Return False when any raw reseller name occurs verbatim in text."""
    return not any(name and name in text for name in reseller_names)
