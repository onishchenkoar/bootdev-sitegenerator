import os
import os.path as op
import shutil


def copy_tree(source: str, destination: str):
    for each in os.listdir(source):
        new_source = op.join(source, each)
        new_dest = op.join(destination, each)
        if op.isfile(new_source):
            shutil.copy(new_source, new_dest)
        else:
            os.makedirs(new_dest, exist_ok=True)
            copy_tree(new_source, new_dest)


def clean_directory_and_copy_files(source: str, destination: str) -> None:
    os.makedirs(destination, exist_ok=True)
    shutil.rmtree(destination)
    copy_tree(source, destination)


def main():
    clean_directory_and_copy_files("static", "public")


if __name__ == "__main__":
    main()
