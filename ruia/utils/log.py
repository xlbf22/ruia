#!/usr/bin/env python

import logging


def get_logger(name="Ruia"):
    # logging_format = "[%(asctime)s] %(levelname)-5s %(name)-8s"
    # logging_format += "%(module)-7s::l%(lineno)d: "
    # logging_format += "%(module)-7s: "
    # logging_format += "%(message)s"
    # logging.basicConfig(
    #     format=logging_format, level=logging.INFO, datefmt="%Y:%m:%d %H:%M:%S"
    # )
    logging_format = "[%(asctime)s] [%(process)d] [%(levelname)s] [%(pathname)s:%(lineno)d]: %(message)s"
    logging.basicConfig(format=logging_format, level=logging.INFO)
    logging.getLogger("asyncio").setLevel(logging.INFO)
    logging.getLogger("websockets").setLevel(logging.INFO)
    return logging.getLogger(name)
