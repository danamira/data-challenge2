import aiohttp
import aiofiles
import sys
import asyncio
from pathlib import Path
from aiohttp.client_exceptions import ServerDisconnectedError
import traceback

import os
import glob
from zipfile import ZipFile
import pandas as pd

async def get_file(yr, month, data_path, session: aiohttp.ClientSession):
    if month < 10:
        month = "0" + str(month)
    addr = f"https://policeuk-data.s3.amazonaws.com/archive/{yr}-{month}.zip"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    print(f"getting addr: {addr}")
    while True:
        try:
            async with session.get(addr, allow_redirects=True, headers=headers) as resp:
                file_path = data_path / f"{yr}-{month}.zip"
                async with aiofiles.open(file_path, "wb") as f:
                    print(f"writing file: {file_path}")
                    async for chunk in resp.content.iter_any():
                        await f.write(chunk)
            return
        except (ServerDisconnectedError, asyncio.TimeoutError):
            print(traceback.format_exc())
            print(f"{addr} download failed, retrying")
            await asyncio.sleep(10)
            pass

async def get_all_files(data_path):
    yr_range = range(2017, 2023)
    mth_range = range(1, 13)
    max_con = 20
    connector = aiohttp.TCPConnector(limit=max_con)
    timeout = aiohttp.ClientTimeout(60*60)
    async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
        tasks = []
        for yr in yr_range:
            for mth in mth_range:
                tasks.append(get_file(yr, mth, data_path, session))
        #additional not caught in the files:
        tasks.append(get_file(2024, 1, data_path, session))
        tasks.append(get_file(2024, 2, data_path, session))
        await asyncio.gather(*tasks)

def is_file_metro_and_unseen(name, seen_files):
    if name in seen_files:
        return False
    if "metropolitan" in name:
        return True
    return False

def rmtree(f: Path):
    if f.is_file():
        f.unlink()
    else:
        for child in f.iterdir():
            rmtree(child)
        f.rmdir()

if __name__ == "__main__":
    try: 
        p = Path.cwd()
        data_path = p / sys.argv[1]
        print(data_path)
        if not data_path.exists():
            raise Exception()
        zip_path = data_path/"mpdzips"
    except Exception as e:
        print(e)
        print("invalid relative data path. call as follows: python download_metro_police_data.py data/ \nfrom project root")
        sys.exit()

    if not zip_path.exists():
        print("here")
        zip_path.mkdir()
        asyncio.run(get_all_files(zip_path))

    extr = zip_path/"extracted"
    if not extr.exists():
        extr.mkdir()
        files = zip_path.glob("*.zip")

        seen_files = set()
        for file in sorted(files, reverse=True):
            zf = ZipFile(file)
            names = zf.namelist()
            to_extract = [*filter(lambda name: is_file_metro_and_unseen(name, seen_files), names)]
            seen_files = seen_files.union(set(to_extract))
            for e in to_extract:
                zf.extract(e, path=str(extr))

    files = sorted(extr.glob("*/*.csv"))

    street = [*filter(lambda x: "street" in str(x) , files)]
    outcomes = [*filter(lambda x: "outcome" in str(x) , files)]
    stop_and_search = [*filter(lambda x: "stop-and" in str(x) , files)]

    streetconc = pd.concat([pd.read_csv(s) for s in street])
    outcomeconc = pd.concat([pd.read_csv(s) for s in outcomes])
    sandsconc = pd.concat([pd.read_csv(s) for s in stop_and_search])

    streetconc.to_pickle(path=data_path/"street_concat.pkl")
    outcomeconc.to_pickle(path=data_path/"outcomes_concat.pkl")
    sandsconc.to_pickle(path=data_path/"stop_and_search_concat.pkl")

    rmtree(zip_path)