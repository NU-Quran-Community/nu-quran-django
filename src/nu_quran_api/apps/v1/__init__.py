import pathlib
import pkgutil

_pkg_path = pathlib.Path(__file__).parent
_pkg_name = __name__

APPS = [
    f"{_pkg_name}.{name}"
    for _, name, is_pkg in pkgutil.iter_modules([str(_pkg_path)])
    if is_pkg and (_pkg_path / name / "apps.py").exists()
]
