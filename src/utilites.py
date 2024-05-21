import os
import shutil


def copy_directory(source_path, destination_path):
    if not os.path.exists(source_path):
        raise Exception("Source directory does not exist")

    if os.path.exists(destination_path):
        shutil.rmtree(destination_path)
    os.mkdir(destination_path)

    contents = os.listdir(source_path)
    for item in contents:
        item_src_path = os.path.join(source_path, item)
        item_dest_path = os.path.join(destination_path, item)
        if os.path.isfile(item_src_path):
            shutil.copy(item_src_path, item_dest_path)
            print(f"Source: {item_src_path}; Destination: {item_dest_path}")
        else:
            os.mkdir(item_dest_path)
            copy_directory(item_src_path, item_dest_path)
