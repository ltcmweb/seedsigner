from .constants import FIELDS_NAME
from .field import Field


class TransformSpec:
    init: bool
    post_init: bool
    repr: bool
    eq: bool
    order: bool
    frozen: bool
    hash: bool | None
    """Tri-state value for adding a __hash__ method.

    If True, add a __hash__ method.
    If False, don't add a __hash__ method.
    If None, set __hash__ to None
    """

    fields: list[Field]
    """Fields sorted alphabetically by name."""

    def __init__(
        self,
        cls: type,
        *,
        init: bool = False,
        repr: bool = False,
        eq: bool = False,
        order: bool = False,
        unsafe_hash: bool = False,
        frozen: bool = False,
    ) -> None:
        self.init = init and ("__init__" not in cls.__dict__)
        self.post_init = hasattr(cls, "__post_init__")
        self.repr = repr and ("__repr__" not in cls.__dict__)
        self.eq = eq
        self.order = order
        self.frozen = frozen

        self.hash = False
        if eq:
            if frozen:
                self.hash = True
            else:
                self.hash = None
        if unsafe_hash:
            self.hash = True

        fields: dict[str, Field] = {}
        # Propagate any existing fields from base class.
        index = 0
        for base in reversed(cls.__bases__):
            idx = index
            for name, field in getattr(base, FIELDS_NAME, {}).items():
                fields[name] = Field(
                    order=field.order + idx,
                    name=field.name,
                    default=field.default,
                    default_factory=field.default_factory,
                    init=field.init,
                    repr=field.repr,
                    hash=field.hash,
                    compare=field.compare,
                    init_only=field.init_only,
                )
                index = max(index, field.order + idx + 1)

        for name, value in cls.__dict__.items():
            if isinstance(value, Field):
                value.name = name
                value.order += index
                fields[name] = value
        self.fields = sorted(fields.values(), key=lambda f: f.order)
