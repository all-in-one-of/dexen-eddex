import os
import platform
import ctypes
# --------------------------------------------------------------------------------
# SetEnv tool
# --------------------------------------------------------------------------------
#http://www.codeproject.com/Articles/12153/SetEnv

# --------------------------------------------------------------------------------
# Functions
# --------------------------------------------------------------------------------
def fix_path(path):
    path = os.path.expandvars(path)
    path = os.path.normcase(path)
    #I found that if there is a ~ in the path, it does not work
    #http://stackoverflow.com/questions/2738473/compare-two-windows-paths-one-containing-tilde-in-python
    if "~" in path:
        path = unicode(path)
        GetLongPathName = ctypes.windll.kernel32.GetLongPathNameW
        buffer = ctypes.create_unicode_buffer(GetLongPathName(path, 0, 0))
        GetLongPathName(path, buffer, len(buffer))
        path = buffer.value
    return path

def setenv_add_paths(name, paths, prepend = True):
    name = name.upper()
    if type(paths) == str:
        paths = [paths]
    paths = [fix_path(i) for i in paths]
    for path in paths:
        if prepend:
            os.system('SetEnv -uap ' + name + ' %"' + path + '"')
        else:
            os.system('SetEnv -ua ' + name + ' %"' + path + '"')
        print
        print "Added '" + path + "'"
        print "to the '" + name + "' environment variable."
        
def setenv_add_values(name, values, prepend = True):
    name = name.upper()
    for value in values:
        if prepend:
            os.system('SetEnv -uap ' + name + ' %"' + value + '"')
        else:
            os.system('SetEnv -ua ' + name + ' %"' + value + '"')
        print
        print "Added '" + value + "'"
        print "to the '" + name + "' environment variable."
        
def is_houdini_dir(path):
    if os.path.isdir(path):
        dir_contents = os.listdir(path)
        if "houdini" in dir_contents:
            return True
    return False
    
# --------------------------------------------------------------------------------
# MAIN SCRIPT
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Get paths
# --------------------------------------------------------------------------------

current_dir =  os.path.split(os.getcwd())[0] #go back one dir
platform = platform.architecture()[0]

# --------------------------------------------------------------------------------
# Set up Houdini libs paths
# --------------------------------------------------------------------------------

#set PYTHONPATH
lib_python_dir = current_dir + "\\python_libs"
setenv_add_paths("PYTHONPATH", [lib_python_dir])

#set HOUDINI_OTLSCAN_PATH
setenv_add_values("HOUDINI_OTLSCAN_PATH", ["&"])
lib_otls_dir = current_dir + "\\otls"
setenv_add_paths("HOUDINI_OTLSCAN_PATH", [lib_otls_dir])

# --------------------------------------------------------------------------------
# Set up Houdini paths
# --------------------------------------------------------------------------------

houdini_dir = os.getenv("HFS")

#if dir is None or if it not a dir, get it from the user
if not houdini_dir or not os.path.isdir(houdini_dir) or not is_houdini_dir(houdini_dir):
    valid_path = False
    while not valid_path:
        houdini_dir = raw_input("\nType the path where Houdini is installed (you can use cut and paste):\n>")
        print "Checking the path that you entered: " + houdini_dir
        valid_path = is_houdini_dir(houdini_dir)
        if valid_path:
            print "The path looks good :)"
        else:
            print "The path you entered was not valid :("
    

#set HFS
setenv_add_paths("HFS", [houdini_dir])

#set PATH
houdini_bin = houdini_dir + "\\bin"
setenv_add_paths("PATH", [houdini_bin])

#set PYTHONPATH
houdini_python_libs = houdini_dir + "\\houdini\\python2.7libs"
setenv_add_paths("PYTHONPATH", [houdini_python_libs])

# --------------------------------------------------------------------------------
#print
#raw_input("Press any key to exit...")
#print "Bye..."