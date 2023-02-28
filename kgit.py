import os, kgit_utils

GIT_DIR = ".kgit"


def init():
    """Create GIT_DIR directory"""
    try:
        os.mkdir(GIT_DIR)
    except FileExistsError:
        print("\nAlready a git repository")
        return
    for name in ["objects", "refs", "refs/heads"]:
        os.mkdir(os.path.join(GIT_DIR, name))
    kgit_utils.write_file(os.path.join(GIT_DIR, "HEAD"), b"ref: refs/heads/master")
    print(f"initialiazed empty repository: {os.path.join(os.getcwd(), GIT_DIR)}")


def main():
    init()


main()
