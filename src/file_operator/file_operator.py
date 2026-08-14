import os
import shutil

def remove_public() -> None:
    public_filepath =  "public"
    is_exist = os.path.exists(public_filepath)
    if not is_exist:
        raise Exception("public directory doesnt exist")
    for item in os.listdir(public_filepath):
        item_path = os.path.join(public_filepath, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        else:
            shutil.rmtree(item_path)

def copy_filepath(relative_path: str="") -> None:
    public_filepath = "public"
    static_filepath = "static"
    joined_public_path = os.path.join(public_filepath, relative_path)
    joined_static_path = os.path.join(static_filepath, relative_path)
    is_public_exist = os.path.exists(joined_public_path)
    is_static_exist = os.path.exists(joined_static_path)

    if is_public_exist and is_static_exist:
        for item in os.listdir(joined_static_path):
            joined_public_item_path = os.path.join(joined_public_path, item)
            joined_static_item_path = os.path.join(joined_static_path, item)
            joined_item = os.path.join(relative_path, item)


            if os.path.isfile(joined_static_item_path):
                shutil.copy(joined_static_item_path, joined_public_item_path)
            else:
                os.makedirs(joined_public_item_path, exist_ok=True)
                copy_filepath(joined_item)
