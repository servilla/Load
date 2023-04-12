#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: load

:Synopsis:

:Author:
    servilla

:Created:
    6/23/20
"""
import asyncio
from datetime import datetime
import logging
import os

import aiohttp
import click
import daiquiri


global loop, success, failure, runtime

cwd = os.path.dirname(os.path.realpath(__file__))
logfile = cwd + "/load.log"
daiquiri.setup(
    level=logging.INFO, outputs=(daiquiri.output.File(logfile), "stdout",)
)
logger = daiquiri.getLogger(__name__)


async def do_requests(requests: int, url: str, verbose: bool):
    tasks = []
    for r in range(requests):
        tasks.append((r, loop.create_task(url_get(r, url, verbose))))
    for r, t in tasks:
        resp = await t


async def url_get(r: int, url: str, verbose: bool) -> int:
    global success, failure
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            status = resp.status
            if status < 400:
                await resp.text()
                success += 1
            else:
                failure += 1
            if verbose:
                print(f"  Request {r+1} status for {url} is: {status}")
            return status


help_requests = "Number of concurrent requests to be made (default 1)"
help_sets = (
    "Number of times set of concurrent requests should "
    "be executed (default 1, -1 for continuous)"
)
help_verbose = "Make output verbose"

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("url")
@click.option("-r", "--requests", default=1, help=help_requests)
@click.option("-s", "--sets", default=1, help=help_sets)
@click.option("-v", "--verbose", is_flag=True, help=help_verbose)
def main(url: str, requests: int, sets: int, verbose: bool):
    """
        load

        \b
        Load test web service

        \b
        URL: URL of the web service to be load tested
    """
    global loop, success, failure, runtime
    loop = asyncio.get_event_loop()

    count = 0
    while sets != 0:
        count += 1
        sets -= 1
        print(f"Running set: {count}")
        success = 0
        failure = 0
        start = datetime.now()
        loop.run_until_complete(do_requests(requests, url, verbose))
        finish = datetime.now()
        runtime = finish - start
        print(f"  Requests: {requests:4d}, Successes: {success:4d}, Failures: {failure:4d}, Runtime: {runtime}")
    return 0


if __name__ == "__main__":
    main()
