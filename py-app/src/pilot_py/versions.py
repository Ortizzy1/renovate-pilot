from packaging.specifiers import SpecifierSet
from packaging.version import InvalidVersion, Version


def is_compatible(version: str, spec: str) -> bool:
    """True when `version` satisfies the PEP 440 specifier `spec`."""
    return Version(version) in SpecifierSet(spec)


def newest(versions: list[str]) -> str | None:
    """Highest valid PEP 440 version in the list, or None."""
    valid = []
    for v in versions:
        try:
            valid.append(Version(v))
        except InvalidVersion:
            continue
    return str(max(valid)) if valid else None
