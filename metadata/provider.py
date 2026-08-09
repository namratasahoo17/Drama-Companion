"""Metadata provider interface.

No external metadata service is configured yet. Returning ``None`` avoids
inventing facts while keeping the graph ready for a real provider.
"""


def fetch_metadata(title_name: str) -> dict | None:
    """Return metadata when a real metadata provider is configured."""
    return None
