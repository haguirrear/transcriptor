import logging
import os
import typing
from dataclasses import dataclass

from fastapi import Response
from fastapi.staticfiles import StaticFiles
from starlette.staticfiles import PathLike
from starlette.types import Scope

logger = logging.getLogger(__name__)


@dataclass
class CacheControl:
    max_age: str
    no_cache: bool = False
    no_store: bool = False
    private: bool = False
    public: bool = False
    inmutable: bool = False

    def to_str(self) -> str:
        resp = ""
        if self.max_age:
            resp += f"max-age={self.max_age}"
        if self.no_cache:
            resp += " no-cache"
        if self.no_store:
            resp += " no-store"
        if self.private:
            resp += " private"
        if self.public:
            resp += " public"
        if self.inmutable:
            resp += " inmutable"

        return resp


class CachedStatic(StaticFiles):
    def __init__(
        self,
        *,
        cache_control: typing.Optional[CacheControl] = None,
        directory: typing.Optional[PathLike] = None,
        packages: typing.Optional[
            typing.List[typing.Union[str, typing.Tuple[str, str]]]
        ] = None,
        html: bool = False,
        check_dir: bool = True,
        follow_symlink: bool = False,
    ) -> None:
        self.cache_control = cache_control
        super().__init__(
            directory=directory,
            packages=packages,
            html=html,
            check_dir=check_dir,
            follow_symlink=follow_symlink,
        )

    def file_response(
        self,
        full_path: PathLike,
        stat_result: os.stat_result,
        scope: Scope,
        status_code: int = 200,
    ) -> Response:
        response = super().file_response(full_path, stat_result, scope, status_code)
        if self.cache_control is not None:
            response.headers["Cache-Control"] = self.cache_control.to_str()
        return response
