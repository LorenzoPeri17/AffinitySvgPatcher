from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element

# from matplotlib/backends/backend_svg.py [ensure_metadata]
ET.register_namespace("","http://www.w3.org/2000/svg")
ET.register_namespace("xlink","http://www.w3.org/1999/xlink")
ET.register_namespace("cc","http://creativecommons.org/ns#")
ET.register_namespace("dc","http://purl.org/dc/elements/1.1/")
ET.register_namespace("rdf","http://www.w3.org/1999/02/22-rdf-syntax-ns#")

import re
import os

from typing import Optional, Union

class AffinitySvgPatcher:
    """
    A class for patching matplotlib-generated SVG files to make them work Affinity Designer.

    This class provides methods to patch SVG files by separating the font-size and font-family properties in the 'font' style attribute, and fixing the placement of 'xlink:href' attributes.

    Attributes:
        file_path (Union[str, os.PathLike]): The path to the SVG file to be patched.
        patched_svg (str): The patched SVG text.

    Methods:
        patch_svg(self, save: bool = True, save_path: Optional[Union[str, os.PathLike]] = None, postfix: str = '-patched') -> None: Patches (and saves) the SVG file.
        save_svg(self, save_dir: Optional[Union[str, os.PathLike]] = None, postfix: str = '-patched') -> None: Saves the patched SVG file.

    Raises:
        ValueError: If the file is not an SVG file.
        
    Usage:
        patcher = AffinitySvgPatcher('path/to/file.svg')
        patcher.patch_svg(save = True, save_dir = 'dir/to/save', postfix = '-patched')
    """
    
    def __init__(self, file_path : Union[str, os.PathLike]) -> None:
        self.file_path = file_path
        self._style_pattern = re.compile(r'font: ([0-9.]+)px ([^;]+);')
        self.patched_svg = ''
        
        self.fname = os.path.basename(self.file_path)
        self.fname_no_ext, ext = os.path.splitext(self.fname) # remove .svg extension
        self.dirname = os.path.dirname(self.file_path)
        
        if ext != '.svg':
            raise ValueError('File must be an SVG file.')
        
        with open(self.file_path, 'r') as f:
            self.svg_text = f.read()
            
    def _patch_text(self, elem : Element) -> None:
        style = elem.attrib['style']
        
        res = self._style_pattern.match(style)
        if res:
            # Change font style to separate font-size and font-family properties
            patched_style = self._style_pattern.sub(r'font-size: \1px; font-family: \2;', style)
            elem.attrib['style'] = patched_style
            
    def _patch_xlink(self, elem : Element) -> None:
        
        # find xlink:href attribute - buggy placement in Affinity Designer
        if r'{http://www.w3.org/1999/xlink}href' in elem.attrib:

            # turn x and y attributes into translate(x y) attribute
            x = elem.attrib.get('x', '0')
            y = elem.attrib.get('y', '0')

            if 'x' in elem.attrib or 'y' in elem.attrib:
                transform = f'translate({x} {y})'
                elem.attrib['transform'] = transform

            if 'x' in elem.attrib:
                del elem.attrib['x']
            if 'y' in elem.attrib:
                del elem.attrib['y']
                
    def patch_svg(self, *, 
                  save : bool = True, 
                  save_dir : Optional[Union[str, os.PathLike]] = None,
                  postfix : str = '-patched') -> None:
        
        root = ET.fromstring(self.svg_text)

        for elem in root.iter():

            if 'text' in elem.tag:
                self._patch_text(elem)
                
            elif 'use' in elem.tag:
                self._patch_xlink(elem)

        self.patched_svg = ET.tostring(root, encoding='unicode', xml_declaration=True)
        
        if save:
            self.save_svg(save_dir, postfix)
        
    def save_svg(self, save_dir : Optional[Union[str, os.PathLike]] = None,
                postfix : str = '-patched') -> None:
        
        if save_dir is None:
            save_dir = self.dirname
            
        save_path = os.path.join(save_dir, self.fname_no_ext + postfix + '.svg')
        
        with open(save_path, 'w') as f:
            f.write(self.patched_svg)
    