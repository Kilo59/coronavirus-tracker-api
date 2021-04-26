"""Profiling utilites"""
import logging

import pyloot
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware

LOGGER = logging.getLogger("profiling")


def add_profiler(app: FastAPI, mount: str = "/_pyloot"):
    try:

        from pyloot import PyLoot

        pyloot = PyLoot()

        def pyloot_wrapper(wsgi_environ, start_response):
            pyloot_environ = wsgi_environ.copy()
            pyloot_environ["wsgi.multiprocess"] = False
            wsgi = pyloot.get_wsgi()
            return wsgi(pyloot_environ, start_response)

        app.on_event("startup")(pyloot.start)
        app.mount(mount, WSGIMiddleware(pyloot_wrapper))
        LOGGER.info(f"pyloot mounted at {mount}")

    except ImportError as err:
        LOGGER.info(f"Profiler could not be added {err}")
