import os
import json
import itertools


def get_path_from_rel(rel_path):
    cwd = os.getcwd()
    return os.path.join(cwd, rel_path)


def get_configs():
    config_path = get_path_from_rel("configs.json")
    with open(config_path, 'r') as config_json:
        config_data = json.load(config_json)
    return config_data


def yield_base_url(keywords, locations):
    """ Yields the job search urls, sorted by date """
    # for kwd, loc in itertools.product(keywords, locations):
    for loc, kwd in itertools.product(locations, keywords):
        yield "https://stackoverflow.com/jobs?sort=p&q={}&l={}&mxs=MidLevel".format(kwd, loc)


def add_to_taboo(taboo_path, url):
    with open(taboo_path, 'a+') as f:
        f.write(url + "\n")


def load_json(fpath):
    with open(fpath, 'r') as f:
        data = json.load(f)
    return data


def load_txt_to_list(fpath):
    with open(fpath, 'r') as f:
        content = f.readlines()
    #content = [x.strip() for x in content]
    content = [strip_string(x.strip()) for x in content]
    return content


def strip_string(s):
    pos = s.find("?")
    s = s[:pos] if pos != -1 else s
    return s


def is_in_file(f_path, item):
    content = load_txt_to_list(f_path)
    if item in content:
        return True
    return False


def is_taboo(taboo_path, url):
    """ returns True if url is in Tabu list """
    content = load_txt_to_list(taboo_path)
    if url in content:
        return True
    return False


def append_to_file(f_path, item):
    """ Adds an item to the file, together with a newline """
    with open(f_path, 'a+') as f:
        f.write(item + "\n")
    return


def overwrite_file(f_path, list_items):
    """ Overwrites a file with a given list """
    with open(f_path, 'w') as f:
        for item in list_items:
            f.write(item + "\n")
    return


if __name__ == "__main__":
    targets_path = "C:\\Users\\Y\\PycharmProjects\\StackJobs\\docs\\targets.txt"
    item = "Rafa"
    list_items = ["Rafa", "is", "cool"]
    append_to_file(targets_path, item)
    overwrite_file(targets_path, list_items)
