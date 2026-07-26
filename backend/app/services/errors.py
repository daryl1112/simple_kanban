"""Domain-level exceptions raised by the service layer.

The API layer translates these into HTTP responses, keeping HTTP concerns out
of the business logic (single responsibility).
"""


class NotFoundError(Exception):
    """Raised when a requested entity does not exist."""


class ValidationError(Exception):
    """Raised when an operation is semantically invalid.

    Examples: creating a dependency cycle, depending on a card in another
    project, or a card depending on itself.
    """
