import os, kgit_utils, hashlib, zlib


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


def hash_object(data, obj_type, write=True):
    """Hash object with header information regarding its type and store it."""
    header = "{} {}".format(obj_type, len(data)).encode()
    full_data = header + b"\x00" + data
    full_data_sha1 = hashlib.sha1(full_data).hexdigest()
    if write:
        path = os.path.join(GIT_DIR, "objects", full_data_sha1[:2], full_data_sha1[2:])
        if not os.path.exists(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            kgit_utils.write_file(path, zlib.compress(full_data))
    return full_data_sha1


def find_object(sha1_prefix):
    """Find an object given is sha1 hash or hash prefix and return its path"""
    assert len(sha1_prefix) >= 2, "Sha1 prefix was less than 2"
    object_path = os.path.join(GIT_DIR, "objects", sha1_prefix[:2])
    assert os.path.exists(object_path), "Object not found"
    filename_starts_with = sha1_prefix[2:]
    objects = [
        obj for obj in os.listdir(object_path) if obj.startswith(filename_starts_with)
    ]
    assert len(objects) == 1, "The number of objects found was not 1"
    return os.path.join(object_path, objects[0])


def read_object(sha1_prefix):
    """Read an object with a given sha1 prefix and return is object type and data in bytes"""
    path = find_object(sha1_prefix)
    full_data = zlib.decompress(kgit_utils.read_file(path))
    null_index = full_data.find(b"\x00")
    header = full_data[:null_index]
    [obj_type, data_len] = header.decode().split()
    data_len = int(data_len)
    data = full_data[null_index + 1 :]
    print(data)
    assert (
        len(data) == data_len
    ), "Object was not hashed properly: Incorrect data length"
    return (obj_type, data)


def main():
    init()
    print(read_object("cbb918f93e0b6c"))


main()
