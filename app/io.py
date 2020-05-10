"""app.io.py"""
import json
import pathlib
from typing import Dict, List, Union

import aiofiles

HERE = pathlib.Path(__file__)
DATA = HERE.joinpath("..", "data").resolve()


def save(
    name: str,
    content: Union[str, Dict, List],
    write_mode: str = "w",
    indent: int = 2,
    data: bool = False,
    **json_dumps_kwargs,
) -> pathlib.Path:
    """Save content to a file. If content is a dictionary, use json.dumps()."""
    if data:
        path = DATA / name
    else:
        path = pathlib.Path(name)
    if isinstance(content, (dict, list)):
        content = json.dumps(content, indent=indent, **json_dumps_kwargs)
    with open(DATA / name, mode=write_mode) as f_out:
        f_out.write(content)
    return path


def load(name: str, data: bool = False, **json_kwargs) -> Union[str, Dict, List]:
    """Loads content from a file. If file ends with '.json', call json.load() and return a Dictionary."""
    if data:
        path = DATA / name
    else:
        path = pathlib.Path(name)
    with open(path) as f_in:
        if path.suffix == ".json":
            return json.load(f_in, **json_kwargs)
        return f_in.read()


class AIO:
    """Asynsc compatible file io operations."""

    @classmethod
    async def save(
        cls,
        name: str,
        content: Union[str, Dict, List],
        write_mode: str = "w",
        indent: int = 2,
        data: bool = False,
        **json_dumps_kwargs,
    ):
        """Save content to a file. If content is a dictionary, use json.dumps()."""
        if data:
            path = DATA / name
        else:
            path = pathlib.Path(name)
        if isinstance(content, (dict, list)):
            content = json.dumps(content, indent=indent, **json_dumps_kwargs)
        async with aiofiles.open(DATA / name, mode=write_mode) as f_out:
            await f_out.write(content)
        return path

    @classmethod
    async def load(cls, name: str, data: bool = False, **json_kwargs) -> Union[str, Dict, List]:
        """Loads content from a file. If file ends with '.json', call json.load() and return a Dictionary."""
        if data:
            path = DATA / name
        else:
            path = pathlib.Path(name)
        async with aiofiles.open(path) as f_in:
            content = await f_in.read()
        if path.suffix == ".json":
            content = json.loads(content, **json_kwargs)
        return content
