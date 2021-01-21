#!/usr/bin/env python3

import os
# import yaml
import ruamel.yaml
from pprint import pprint

CM = ruamel.yaml.comments.CommentedMap

repo_root = "/home/tamal/go/src/stash.appscode.dev/stash"
directory = os.path.join(repo_root, ".github", "workflows")

for filename in os.listdir(directory):
    if not filename.endswith(".yml"):
        continue

    with open(os.path.join(directory, filename), 'r+') as f:
        yaml = ruamel.yaml.YAML(typ='rt')
        yaml.preserve_quotes = True
        yaml.width = 4096
        data = yaml.load(f)
        for job in data['jobs']:
            for i, step in enumerate(data['jobs'][job]['steps']):
                # print(type(step))
                # pprint(step)

                if 'id' in step.keys() and step['id'] == 'buildx':
                    data['jobs'][job]['steps'].pop(i)

                    e1 = CM({
                        'name': 'Set up Docker Buildx',
                        'uses': 'docker/setup-buildx-action@v1'
                    })
                    # e1.ca.items[1] = [None, None, None, 'ff']
                    # e1.ca.items = list(None)
                    e1.yaml_set_comment_before_after_key(
                        'uses', after='fhhfhfghfghgfh')
                    e1.yaml_set_start_comment('fggggggggggg')
                    data['jobs'][job]['steps'].insert(i, e1)

                    e2 = CM({
                        'name': 'Available platforms',
                        'run': 'echo ${{steps.qemu.outputs.platforms}}'
                    })
                    #e2.ca.items = list(None)
                    # e2.yaml_set_start_comment('\n')
                    data['jobs'][job]['steps'].insert(i, e2)

                    data['jobs'][job]['steps'].insert(i, CM({
                        'name': 'Set up QEMU',
                        'id': 'qemu',
                        'uses': 'docker/setup-qemu-action@v1'
                    }))

                    # print(type(data['jobs'][job]['steps'][i]))
                    # exit(1)
        f.seek(0)
        # yaml.dump(data, f, width=2, indent=2, sort_keys=False)
        yaml.indent(mapping=2, sequence=4, offset=2)
        yaml.dump(data, f)
