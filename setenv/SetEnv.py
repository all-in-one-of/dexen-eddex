import os
import ctypes
import subprocess
# --------------------------------------------------------------------------------
# SetEnv tool
# --------------------------------------------------------------------------------
#http://www.codeproject.com/Articles/12153/SetEnv

# --------------------------------------------------------------------------------
# Functions
# --------------------------------------------------------------------------------
def run_setenv(*args):
    args = ['SetEnv'] + list(args)
    p = subprocess.Popen(
        args, 
        shell=False, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        print "    ", line,
    retval = p.wait()    

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

def setenv_add_values(name, values, are_paths=True, prepend=True):
    name = name.upper()
    if type(values) == str:
        values = [values]
    if are_paths:
        values = [fix_path(i) for i in values]
    for value in values:
        if prepend:
            run_setenv('-uap', name, '%' + value)
        else:
            run_setenv('-ua', name, '%' + value)
        print
        print "Added '" + value + "'"
        print "to the '" + name + "' environment variable."
        
def setenv_del_variable(name):
    name = name.upper()
    run_setenv('-ud', name)
    print 
    print "Deleted '" + name + "' environment variable."

def setenv_del_matches(name, matches):
    name = name.upper()
    if type(matches) == str:
        matches = [matches]
    existing_values = os.getenv(name)
    if existing_values:
        existing_values = existing_values.split(";")
    else:
        existing_values = []
    for match in matches:
        for existing_value in existing_values:
            if match.lower() in existing_value.lower():
                run_setenv('-ud', name, '%' + existing_value)
                print 
                print "Deleted '" + existing_value + "'"
                print "from the '" + name + "' environment variable."

# --------------------------------------------------------------------------------
# MAIN SCRIPT
# --------------------------------------------------------------------------------
def main():
    # --------------------------------------------------------------------------------
    # Get paths
    # --------------------------------------------------------------------------------

    #the setenv parent folder
    current_dir =  os.path.split(os.getcwd())[0] #go back one dir

    #get the houdini path from the user
    def is_houdini_path(path):
        exe_file = os.path.join(path, 'bin', 'houdini.exe')
        if os.path.isfile(exe_file):
            return True
        return False

    valid_path = False
    while not valid_path:
        houdini_dir = raw_input("\nType the path where Houdini is installed (you can use cut and paste):\n>")
        print "Checking the path that you entered: " + houdini_dir
        valid_path = is_houdini_path(houdini_dir)
        if valid_path:
            print "The path looks good :)"
        else:
            print "The path you entered was not valid :("

    # --------------------------------------------------------------------------------
    # Set up Eddex paths
    # --------------------------------------------------------------------------------

    #set PYTHONPATH
    setenv_del_matches("PYTHONPATH", "eddex")
    setenv_add_values("PYTHONPATH", current_dir + "\\houdini\\python_libs")

    #set HOUDINI_OTLSCAN_PATH
    setenv_del_matches("HOUDINI_OTLSCAN_PATH", "eddex")
    setenv_add_values("HOUDINI_OTLSCAN_PATH", "&", are_paths=False)
    setenv_add_values("HOUDINI_OTLSCAN_PATH", current_dir + "\\houdini\\otls")

    # --------------------------------------------------------------------------------
    # Set up Houdini paths
    # --------------------------------------------------------------------------------

    #set PATH
    setenv_add_values("PATH", houdini_dir + "\\bin")

    # --------------------------------------------------------------------------------

main()