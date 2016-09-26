"""
Routines for reading in and printing out files for results and configuration.
"""

import logging
import xml.etree.ElementTree as ET
import xml.dom.minidom as xdm

import numpy as np

class InputHandler(object):
    """General classs for handling XML input files.

    Parameters
    ----------
    input_filename : `str`
    input_vars : `list`
        List of variables to read from XML file `input_filename`

    Notes
    -----
    A logging instance should be created prior to instantiating
    InputHandler so that relevant log messages can be recorded.
    """

    def __init__(self,input_filename,input_vars=None,**kwargs):
        """Constructor"""
        tree = ET.parse(input_filename)
        self.root = tree.getroot()
        if input_vars is not None:
            self.var_list = input_vars
        else:
            self.var_list = [child.tag for child in self.root]
        self.logger = logging.getLogger(type(self).__name__)


    def lookup_vars(self,**kwargs):
        """Loop over `input_vars` and find XML node value."""

        input_dict = {}
        for var in self.var_list:
            #Find node
            node = self.root.find(var)
            #Check if found
            if node is None:
                self.logger.warning("No value found for input %s. Returning None."%var)
                input_dict[var] = None
            else:
                input_dict[node.tag] = self._read_node(node)

        return input_dict


    def _read_node(self,node):
        """Read in node values for different configurations"""

        if node.getchildren():
            tmp = []
            for child in node.getchildren():
                tmp.append({child.tag:self._read_node(child)})
            return tmp
        else:
            if node.text:
                return self._bool_filter(node.text)
            elif node.attrib:
                return node.attrib
            else:
                self.logger.warning('Unrecognized node format for %s. Returning None.'%(node.tag))
                return None


    def _bool_filter(self,val):
        """Convert true/false string to Python bool"""

        trues = ['True','TRUE','true','yes','Yes',1]
        falses = ['False','FALSE','false','no','No',0]

        if type(val) is not type(''):
            return val
        elif any([val == t for t in trues]):
            return True
        elif any([val == f for f in falses]):
            return False
        else:
            return val



class OutputHandler(object):
    """General class for handling printing of output files from Python dictionaries.
    Can be used to print both configuration files as well as results files. Print to
    either plain text or structured XML files.

    Attributes:
        output_filename -- string containing filename to print to
        output_dict -- dictionary to print to file

    """

    def __init__(self,output_filename,output_dict,**kwargs):
        """Initialize OutputHandler class"""

        self.output_filename = output_filename
        self.output_dict = output_dict
        #configure logger
        self.logger = logging.getLogger(type(self).__name__)


    def print_to_xml(self):
        """Print dictionary to XML file"""

        self.root = ET.Element('root')
        for key in self.output_dict:
            self._set_element_recursive(self.root,self.output_dict[key],key)

        with open(self.output_filename,'w') as f:
            f.write(self._pretty_print_xml(self.root))

        f.close()


    def display_xml(self):
        """Print configured XML to the screen"""

        if not hasattr(self,'root'):
            self.logger.error('No root element found. Run self.print_to_xml() first.')

        print(self._pretty_print_xml(self.root))


    def _set_element_recursive(self,root,node,keyname):
        """Set element tags, values, and attributes. Recursive for arrays/lists."""

        #create subelement
        element = ET.SubElement(root,keyname)
        if type(node) is list:
            for item in node:
                sub_keyname = [k for k in item][0]
                self._set_element_recursive(element,item[sub_keyname],sub_keyname)
        elif type(node) is dict:
            for key in node:
                if key == '_val':
                    element.text = str(node[key])
                else:
                    element.set(key,str(node[key]))
        else:
            element.text = str(node)


    def _pretty_print_xml(self,element):
        """Formatted XML output for writing to file."""

        unformatted = ET.tostring(element)
        xdmparse = xdm.parseString(unformatted)
        return xdmparse.toprettyxml(indent="    ")
