#!/usr/bin/env python3

import sys
import json
from os.path import basename
from objcclass import ObjCClass, TYPE_TYPE_MAP

def to_singular(s):
    # TODO ask interactively for singular form
    if s[-1] == 's':
        return s[0:-1]
    return s


def traverse_node(node, name):
    result = []

    current = ObjCClass(name)

    def is_container(x):
        return isinstance(x, dict) or isinstance(x, list)

    def update_result(result, k, v):
        if isinstance(v, dict):
            child_class_name = (k.title()+'Model')
            result = result + traverse_node(v, child_class_name)
            current.add_field(k, child_class_name+'*')
        elif isinstance(v, list):
            result = result + traverse_node(v[0], to_singular(k).title())
            current.add_field(k, "NSArray*")
        else:
            current.add_field(k, TYPE_TYPE_MAP[type(v)])
        return result

    for k, v in node.items():
        result = update_result(result, k, v)

    result.append(current)
    return result


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} Foo.json".format(sys.argv[0]))

    filename = sys.argv[1]
    class_name = basename(filename).split('.')[0].title()

    with open(filename) as fi:
        root = json.load(fi)

    if not isinstance(root, dict):
        raise RuntimeError("input must be json dict")

    objc_classes = traverse_node(root, class_name)

    # XXX: test code
    print("\n".join(map(str, objc_classes)))

    for c in objc_classes:
        print('===================================')
        print(c.dump_header())
        print('-----------------------------------')
        print(c.dump_implementation())

