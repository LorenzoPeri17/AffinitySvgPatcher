from AffinitySvgPatcher import AffinitySvgPatcher

import sys
from argparse import ArgumentParser

parser = ArgumentParser(description="Affinity SVG Patcher")
parser.add_argument("input", help="The input SVG file")
parser.add_argument("--postfix", help="patched SVG postfix", required=False, default="patched", type=str)
parser.add_argument("--dir", help="The directory to save the patched SVG file", required=False, default=None)

def main() -> None:
    
    args = parser.parse_args()
    
    patcher = AffinitySvgPatcher(args.input)
    patcher.patch_svg(save = True, save_dir = args.dir, postfix = '-'+args.postfix)
    
if __name__ == "__main__":
    main()