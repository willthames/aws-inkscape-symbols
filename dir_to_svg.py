#!/usr/bin/env python

import os
import re
import sys
import xml.etree.ElementTree as ET

#FILENAME_PREFIX = r'^[^_]*_(?:.*)?'
FILENAME_PREFIX = r'^[^_]*_(?:Amazon|AWS)?'

DIR_TO_CATEGORY = {
    'Game Development': 'game-dev',
    'Management Tools': 'management',
    'Networking & Content Delivery': 'network',
    'Application Services': 'application-services',
    'On Demand Workforce': 'workforce',
    'Artificial Intelligence': 'ai',
    'Desktop App Streaming': 'desktop',
    'Business Productivity': 'productivity',
    'Developer Tools': 'dev-tools',
    'Internet of Things': 'iot',
    'Mobile Services': 'mobile',
    'Security Identity & Compliance': 'iam'
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
    #gcontainer = root.find('{http://www.w3.org/2000/svg}g')
    if gcontainer is not None:
        component.extend(gcontainer)
        """
        for gelem in gcontainer.iter():
            # only update leaf elements
            if not list(gelem):
                if 'style' in gelem.attrib:
                    if 'stroke-width' not in gelem.attrib['style']:
                        gelem.attrib['style'] += '; stroke-width: 1'
                else:
                    gelem.attrib['style'] = 'stroke-width: 1'
        """
    return component


def main(args):
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    srcdir = args[0]
    subdir = os.path.basename(srcdir)
    destdir = args[1]
    componentname = DIR_TO_CATEGORY.get(subdir, subdir.lower())
    destfile = os.path.join(destdir, 'aws-%s.svg' % componentname)
    components = [read_component(os.path.join(srcdir, filename))
                  for filename in os.listdir(srcdir)]
    create_svg_file(componentname, destfile, components)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
