from subprocess import Popen, PIPE, CREATE_NEW_CONSOLE
import tkinter as tk
from datetime import datetime, timedelta
import time
import logging
import config
from sqlalchemy import select, update
from models import Processes
import threading
from pathlib import Path
import os

# /K remains the window, /C executes and dies (popup)
""" os.system("start cmd /K dir") """

logging.basicConfig(filename="main.log",
                    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

main = config.main


def Main():
    logging.info("Starting Main")

    while datetime.now().hour >= 0 and datetime.now().hour < 24:
        logging.info(f"Running {datetime.now().hour} PIPELINE")
        # Statement to fetch processes with a next runtime of the current hour
        statement = select(Processes).where((Processes.next_runtime >= datetime(datetime.now().year, datetime.now(
        ).month, datetime.now().day, datetime.now().hour, 0, 0)) & (Processes.next_runtime <= datetime(datetime.now().year, datetime.now(
        ).month, datetime.now().day, datetime.now().hour, 59, 59)))

        processes = Processes()
        result = processes.Read(statement)
        if result['status'] == []:
            logging.info(f"0 Processes to run...")
        else:
            logging.info(
                f"{len(result['status'])} Processe(s) to run...")
            threadController = threading.Thread(
                target=ThreadController, args=(result['status'],))
            threadController.start()

        logging.info("Sleeping...")
        time.sleep(((datetime.now() + timedelta(hours=1)).replace(microsecond=0,
                   second=0, minute=2)-datetime.now()).seconds)
        logging.info("Cleaning...")

        logging.info("Completed PIPELINE")


def RunProcess(process, name):
    logging.info(f'{name} is running...')
    running = Popen(process, creationflags=CREATE_NEW_CONSOLE)
    running.wait()
    logging.info(f'{name} is closed...')


def ThreadController(processes):
    logging.info(f"{datetime.now().hour} Thread Controller started...")
    for row in processes:
        process = row[0].Serializer()
        processThread = threading.Thread(
            target=RunProcess, args=(Path.cwd() / process['batch_location'][2:], process['name']))
        processThread.start()
    logging.info(f"{datetime.now().hour} Thread Controller Done...")


if __name__ == "__main__":
    Main()
