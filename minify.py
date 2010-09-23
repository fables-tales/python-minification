import inspect
import sys

#generates a skeleton class listing
def generate_skeleton_class(class_name, class_type):
    class_dict = class_type.__dict__
    class_text = "class " + class_name + ":\n"

    for key in class_dict:
        if key == "__init__" or not "__" in key:
            if type(class_dict[key]).__name__ != "function":
                class_text += "  " + key + " = 0\n"
            else:
                class_text += "  def " + key + "():\n"
                class_text += "    return None\n"

    return class_text

#prints skeleton vars
def print_vars(var_list):
    for name in var_list:
        print name + " = None"

#prints the passed class list
def print_classes(class_list):
    for name,class_obj in class_list:
        print generate_skeleton_class(name,class_obj)


#generates a string representing the skeleton of this function
def generate_skeleton_function(name, function):
    argspec = inspect.getargspec(function).args
    argstring = ""
    for i in xrange(0,len(argspec)):
        argstring += argspec[i]
        if (i != len(argspec)-1):
            argstring += ","
    return "def %s (%s):\n   return None\n" % (name,argstring)

def print_functions(function_list):
    for name,function in function_list:
        print generate_skeleton_function(name,function)

#analyses the passed library for things
def analyse(libraryname):
    imp = __import__(libraryname, fromlist="*")
    interface = dir(imp)

    functions = []
    vars = []
    classes = []

    for item in interface:
        if not "__" in item:
            typename = type(imp.__dict__[item]).__name__

            if typename == "classobj":
                classes.append((item, imp.__dict__[item]))
            elif typename == "function":
                functions.append((item, imp.__dict__[item]))
            else:
                vars.append(item)

    return {"functions":functions, "classes":classes, "variables":vars}

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage is: ./minify <modulespec> where modulespec is a description of a python module"
        sys.exit(1)
    else:
        interface = analyse(sys.argv[1])
        print_vars(interface["variables"])
        print_classes(interface["classes"])
        print_functions(interface["functions"])

