import sys

from . import generator, parser, util

def save_nifs(c_code):
    print(c_code)
    
def main():
    if len(sys.argv) != 3:
        util.die('usage: cproto2nif.py mymodule-proto.h mymodule');

    protof = sys.argv[1]
    modname = sys.argv[2]

    protos = parser.load_protos(protof, modname)
    output_code = generator.generate_enclosure(protos, modname)
    save_nifs(output_code)
    
