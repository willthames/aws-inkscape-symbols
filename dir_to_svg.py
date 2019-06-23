#!/usr/bin/env python

import os
import re
import sys
import xml.etree.ElementTree as ET

#FILENAME_PREFIX = r'^[^_]*_(?:.*)?'
FILENAME_PREFIX = r'^(?:Amazon-|AWS-)'

DIR_TO_CATEGORY = {
    'AWS Cost Management': 'cost',
    'Game Development': 'game-dev',
    'Game Tech': 'game-dev',
    '_General': 'general',
    '_Group Icons': 'group-icons',
    'AR & VR': 'vr',
    'Management Tools': 'management',
    'Management & Governance': 'management',
    'Migration & Transfer': 'migration',
    'Networking & Content Delivery': 'network',
    'Application Services': 'application-services',
    'On Demand Workforce': 'workforce',
    'Artificial Intelligence': 'ai',
    'Machine Learning': 'ai',
    'Desktop App Streaming': 'desktop',
    'Business Productivity': 'business',
    'Business Applications': 'business',
    'Developer Tools': 'dev-tools',
    'Internet of Things': 'iot',
    'Mobile Services': 'mobile',
    'Security Identity & Compliance': 'iam',
    'Security, Identity, & Compliance': 'iam',
}


TEMPLATE_FILE = 'symbols_template.xml'


def create_svg_file(componentname, filename, components):
    tree = ET.parse(TEMPLATE_FILE)
    root = tree.getroot()
    title = root.find('{http://www.w3.org/2000/svg}title')
    title.text = 'AWS ' + componentname
    desc = root.find('{http://www.w3.org/2000/svg}desc')
    desc.text = 'AWS %s symbols' % componentname
    defs = root.find('{http://www.w3.org/2000/svg}defs')
    for component in components:
        defs.append(component)
    with open(filename, 'w') as out:
        out.write(ET.tostring(root))


def read_component(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    filename = os.path.basename(filename)
    filename = re.sub(FILENAME_PREFIX, '', filename).lower()
    filename = filename.replace('_', '-')
    symbol_id = filename[:-4]
    component = ET.Element('symbol', attrib=dict(id=symbol_id))
    title = ET.SubElement(component, 'title')
    title.text = symbol_id
    defs = root.find('{http://www.w3.org/2000/svg}defs')
    if defs is not None:
        for style in defs.iter():
            component.extend(style)
    # Explicitly set stroke-width otherwise symbols can be
    # a little heavy
    for defs in root.findall('{http://www.w3.org/2000/svg}defs'):
      root.remove(defs)
    for rt in root.findall('{http://www.w3.org/2000/svg}title'):
      root.remove(rt)
    gcontainer = root
    if gcontainer is not None:
        component.extend(gcontainer)
    return component


def read_subdir(srcdir):
    components = list()
    for maybe_filename in os.listdir(srcdir):
        print("Maybe filename is {}".format(maybe_filename))
        if not os.path.isdir(os.path.join(srcdir, maybe_filename)):
            components.append(read_component(os.path.join(srcdir, maybe_filename)))
        else:
            new_srcdir = "{}/{}".format(srcdir, maybe_filename)  # not really a filename
            components.extend(read_subdir(new_srcdir))
    return components

def main(args):
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    srcdir = args[0]
    subdir = os.path.basename(srcdir)
    destdir = args[1]
    componentname = DIR_TO_CATEGORY.get(subdir, subdir.lower())
    destfile = os.path.join(destdir, 'aws-%s.svg' % componentname)

    components = read_subdir(srcdir)

    create_svg_file(componentname, destfile, components)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
