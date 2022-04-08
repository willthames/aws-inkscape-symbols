#!/usr/bin/env python

import os
import re
import sys
import xml.etree.ElementTree as ET

FILENAME_PREFIX = r'^(?:Amazon-|AWS-)'
FILENAME_SUFFIX = r'_[0-9]*(?:_light|_dark)?\.svg'
TEMPLATE_FILE = 'symbols_template.xml'


def create_svg_file(componentname, filename, components):
    tree = ET.parse(TEMPLATE_FILE)
    root = tree.getroot()
    title = root.find('{http://www.w3.org/2000/svg}title')
    title.text = f'AWS {componentname}'
    desc = root.find('{http://www.w3.org/2000/svg}desc')
    desc.text = f'AWS {componentname} symbols'
    defs = root.find('{http://www.w3.org/2000/svg}defs')
    for component in components:
        defs.append(component)
    with open(filename, 'wb') as out:
        out.write(ET.tostring(root))


def read_component(io, symbol_id: str):
    tree = ET.parse(io)
    root = tree.getroot()
    component = ET.Element('symbol', attrib=dict(id=symbol_id))
    title = ET.SubElement(component, 'title')
    title.text = symbol_id
    defs = root.find('{http://www.w3.org/2000/svg}defs')
    if defs is not None:
        for defn in defs:
            defnid = defn.get('id')
            if defnid:
                defn.set('id', f'{symbol_id}-{defnid}')
        component.extend(defs)
    for defs in root.findall('{http://www.w3.org/2000/svg}defs'):
        root.remove(defs)
    for rt in root.findall('{http://www.w3.org/2000/svg}title'):
        root.remove(rt)
    for desc in root.findall('{http://www.w3.org/2000/svg}desc'):
        root.remove(desc)
    for group in root.find('{http://www.w3.org/2000/svg}g'):
        fill = group.get('fill')
        if fill and fill.startswith('url(#'):
            group.set('fill', fill.replace('url(#', f'url(#{symbol_id}-'))
    gcontainer = root
    if gcontainer is not None:
        component.extend(gcontainer)
    return component
