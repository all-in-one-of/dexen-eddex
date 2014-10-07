"""
Executor classes used for executing tasks.
"""
import sys, os
import hou
from bson.binary import Binary

#Current working directory
HOU_FOLDER_PATH = os.getcwd()

#Helper functions

def _load_hip_file(hip_file_name):
    """Attempt to load a hip file in Houdini """
    hou_file_path = os.path.join(HOU_FOLDER_PATH, hip_file_name)
    try:
        result = hou.hipFile.load(hou_file_path)
    except hou.LoadWarning as e:
        print "hou.LoadWarning exception loading hip file"
        print str(e)
        raise
    except hou.OperationFailed as e:
        print "hou.OperationFailed exception loading hip file"
        print str(e)
        raise
    except Exception as e:
        print "Exception loading hip file"
        print str(e)
        raise
    except:
        print "Unrecognised exception loading hip file"
        raise
    if result:
        print "Warnings loading hip file: ", result

def _get_hou_node(node_path):
    """Attempt to get a node from hou """
    node = hou.node(node_path)
    if not node:
        print "ERROR: Houdini node " + node_path + " does not exist."
        raise Exception()
    return node

def _cook_hou_node(node, animate = None):
    """cook a node in a houdini file"""
    if animate is not None:
        node.cook(force=True, frame_range=animate)
    else:
        node.cook(force=True)
        
def _set_hou_node_parameters(node, prefix, values, start_index=1):
    """set parameter values of a houdini node"""
    for i, v in enumerate(values):
        node.setParms({prefix+str(i+start_index):v})
        
def _get_hou_node_attributes(node, attribute_names):
    """get the attribute values of a houdini node (detail attributes)"""
    results = []
    for attribute_name in attribute_names:
        result = node.geometry().attribValue(attribute_name)
        results.append(result)
    return results
    
def _temp_dir():
    """Create an empty folder. (If the folder exists, delete it.) """
    temp_dir = os.path.join(os.getcwd(), "temp")
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)
    else:
        for the_file in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception, e:
                print e
    return temp_dir

# Functions for executing tasks

def houdini_develop(ind, hip_file_name, in_path, out_path, animate=None):
    #get the genotype
    genotype = ind.get_genotype()
    #open the hipnc file
    _load_hip_file(hip_file_name)
    #set the parameters using the individual's genes
    genotype_node = _get_hou_node(in_path)
    _set_hou_node_parameters(genotype_node, "gene_", genotype)
    #save phenotype to file
    phen_file_path = os.path.join(_temp_dir(), "temp.bgeo")
    phenotype_node = _get_hou_node(out_path)
    phenotype_node.setParms(dict([["file",phen_file_path]]))
    _cook_hou_node(phenotype_node, animate)
    # get and save the phenotype
    with open(phen_file_path, "rb") as f:
        phenotype = f.read()
    return Binary(phenotype)

def houdini_evaluate(ind, score_names, hip_file_name, in_path, out_path, animate=None):
    #get the phenotype
    phenotype = ind.get_phenotype()
    #write the phenotype to a temporary file
    phen_file_path = os.path.join(_temp_dir(), "temp.bgeo")
    with open(phen_file_path, "wb") as f:
        f.write(phenotype)
    #open the phenotype hipnc file
    _load_hip_file(hip_file_name)
    #load the geometry into the phenotype node
    phenotype_node = _get_hou_node(in_path)
    phenotype_node.setParms(dict([["file",phen_file_path]]))
    #cook the score node
    score_node = _get_hou_node(out_path)
    _cook_hou_node(score_node, animate)
    #get and save all the scores
    score_values = []
    for score_name in score_names:
        score_value = score_node.geometry().attribValue(score_name)
        score_values.append(score_value)
    return score_values
