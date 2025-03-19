import os
import shutil
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


def copy_directory(source, destination):
    if os.path.exists(destination):
        logging.info(f"Deleting existing destination directory: {destination}")
        shutil.rmtree(destination)

    logging.info(f"Creating destination directory: {destination}")
    os.makedirs(destination)

    for item in os.listdir(source):
        source_item = os.path.join(source, item)
        destination_item = os.path.join(destination, item)

        if os.path.isfile(source_item):
            logging.info(f"Copying file: {source_item} to {destination_item}")
            shutil.copy2(source_item, destination_item)  # copy2 preserves metadata
        elif os.path.isdir(source_item):
            logging.info(f"Copying directory: {source_item} to {destination_item}")
            copy_directory(source_item, destination_item)
