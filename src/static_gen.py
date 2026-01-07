import os, sys, shutil, logging
logging.basicConfig(level=logging.INFO)

def copy_dir_static(src, dest):
    source, destination = os.path.abspath(src), os.path.abspath(dest)
    if not os.path.exists(destination):
        os.mkdir(destination)
        logging.info(f"Folder '{destination}' created.")
    else:
        shutil.rmtree(destination)
        logging.info(f"Folder '{destination}' removed.")
        os.mkdir(destination)
    if not (os.path.isdir(source) and os.path.isdir(destination)):
        raise Exception("Either arguement is not a directory")
    copy_dir_recursive(source, destination)

def copy_dir_recursive(source, destination):
    files = os.listdir(source)
    logging.info(f"Copying files in {source}")
    for file in files:
        logging.info(f"File name: {file}, isDir: {os.path.isdir(os.path.join(source, file))}")
        if os.path.isdir(os.path.join(source, file)):
            if file not in os.listdir(destination):
                os.mkdir(os.path.join(destination, file))
            copy_dir_recursive(os.path.join(source, file), os.path.join(destination, file))
        else:
            shutil.copy(os.path.join(source, file), destination)
            logging.info(f"Copying {file} to {destination}")
    return
           
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Requires 2 positional arguements: source dir, destination dir")
        sys.exit()
    src, dest = sys.argv[1], sys.argv[2]
    copy_dir_static(src, dest)
