from os import PathLike
import re
from sys import exit
import zipfile
from awssymbols import io
import argparse
import pathlib
import xml.etree.ElementTree as ET

def read_zipfile(filename: PathLike) -> zipfile.ZipFile:
    with zipfile.ZipFile(filename, mode="r") as zf:
        for fn in zf.namelist():
            if fn.startswith("._") or fn.startswith("GRAYSCALE") or "__MACOSX" in fn:
                continue
            if not fn.endswith(".svg"):
                continue
            if "48" not in fn:
                continue
            with zf.open(fn) as inner_file:
                yield inner_file

def componentname(z: zipfile.ZipExtFile) -> str:
    path = pathlib.Path(z.name)
    componentname = "aws-"
    if path.parts[0].startswith("Architecture-Service"):
        componentname += "service-"
        sname = path.parts[1][5:].lower()
        componentname += sname
    elif path.parts[0].startswith("Category"):
        componentname += "category"
    elif path.parts[0].startswith("Resource"):
        componentname += "resource-"
        sname = path.parts[1][4:].lower()
        componentname += sname + "-"
        ld = path.parts[2][7:].lower()
        componentname += ld
    
    return componentname


def symbolname(z: zipfile.ZipExtFile) -> str:
    path = pathlib.Path(z.name)
    filename = path.name
    filename = re.sub(io.FILENAME_PREFIX, '', filename).lower()
    filename = re.sub(io.FILENAME_SUFFIX, '', filename)
    symbol_id = filename.replace('_', '-')
    return symbol_id

def main(zipfile: PathLike, output: PathLike = pathlib.Path("./target")):
    zipfile = pathlib.Path(zipfile)
    output = pathlib.Path(output)
    if not zipfile.exists() or not zipfile.is_file():
        print("ERROR: required argument 'zipfile' must exist and be a regular file")
        PARSER.print_usage()
        exit(1)
    if output.exists() and not output.is_dir():
        print("ERROR: output path exists but is not a directory.")
        PARSER.print_usage()
        exit(1)
    if not output.exists():
        output.mkdir(parents=True, exist_ok=True)
    
    components = {}
    for z in read_zipfile(zipfile):
        cn = componentname(z)
        sn = symbolname(z)
        comp = io.read_component(z, sn)
        # TODO: can I use the array ref in a smarter way?
        components[cn] = components.get(cn, []) + [comp]
    
    for cn,comps in components.items():
        outfile = output / (cn + ".svg")
        io.create_svg_file(cn, outfile, comps)


PARSER = argparse.ArgumentParser()
PARSER.add_argument("zipfile", type=pathlib.Path)
PARSER.add_argument("--output", "-o", type=pathlib.Path, required=False, default="target")

if __name__ == "__main__":
    args = PARSER.parse_args()
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    main(**vars(args))