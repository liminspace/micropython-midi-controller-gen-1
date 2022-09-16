import sys

import micropython

# noinspection PyUnreachableCode
if False:  # sourcery skip: remove-redundant-if
    from typing import Any, Optional


def load_module_object(
    path: str,
    dot_number: int = -1,
    expected_type: Optional[type] = None,
) -> Any:
    if dot_number > -1 and path.count(".") != dot_number:
        raise ValueError(f"invalid path: it must contain {dot_number} dot(s)")

    module_path, variable_name = path.rsplit(".", 1)
    if not module_path or not variable_name:
        raise ValueError("invalid path: parts of path cannot be empty")

    try:
        mod = __import__(module_path)
    except ImportError as e:
        raise ValueError(f"invalid path: module `{module_path}` not found: {e}")

    for n, path_part in enumerate(module_path.split(".")):
        if n == 0:
            continue
        mod = getattr(mod, path_part)

    if not hasattr(mod, variable_name):
        raise ValueError(f"invalid path: variable `{variable_name}` not found in module `{module_path}`")

    obj = getattr(mod, variable_name)
    del mod
    del sys.modules[module_path]

    if expected_type is not None and not isinstance(obj, expected_type):
        raise ValueError(f"invalid path: imported object is not a {expected_type.__name__}")

    return obj


@micropython.native
def async_partial(_func_: callable, *default_args, **default_kwargs) -> callable:
    @micropython.native
    async def _async_partial(*args, **kwargs):
        kw = default_kwargs.copy()
        kw.update(kwargs)
        return await _func_(*(default_args + args), **kw)

    return _async_partial
