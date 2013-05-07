import os
import re

class Property:
    def __init__(self, class_name):
        self.__class_name = class_name
        self.__name = ""
        self.__type = ""
        self.__has_read = False
        self.__has_write = False
        self.__has_notify = False
        self.__has_final = False
        
    def gen_qproperty_code(self):
        extras = ""
        extras += " READ {0}".format(self.__name) if self.__has_read else ""
        extras += " WRITE set{0}".format(self.__name.title()) if self.__has_write else ""
        extras += " NOTIFY {0}Changed".format(self.__name) if self.__has_notify else ""
        extras += " FINAL" if self.__has_final else ""
        result = "    Q_PROPERTY({0} {1}{2})\n".format(self.__type, self.__name, extras)
        return result

    def gen_member_attribute(self):
        return "    {0} m_{1};\n".format(self.__type, self.__name);

    def gen_signal(self):
        return "    void {0}Changed();\n".format(self.__name)

    def gen_read_method_signature(self):
        return "    Q_INVOKABLE {0} {1}();\n".format(self.__type, self.__name)
    
    def gen_read_method_implementation(self):
        return "{0} {1}::{2}() {{\n    return m_{2};\n}}\n".format(self.__type, self.__class_name, self.__name)
        
    def gen_write_method_signature(self):
        return "    Q_INVOKABLE void set{0}({1} new{0});\n".format(self.__name.title(), self.__type)
    
    def gen_write_method_implementation(self):
        signal = "        emit {0}Changed();\n".format(self.__name)
        return "void {0}::set{3}({2} new{3}){{\n    if(m_{1} != new{3})\n        m_{1} = new{3};\n{4}}}\n".format(self.__class_name, self.__name, self.__type, self.__name.title(), signal if self.__has_notify else "")

    def extract_qsteroid_property_information(self, line_content):
        property_search = re.search('Q_STEROID_PROPERTY\((.*)\)', line_content, re.IGNORECASE)
        if property_search:
            values = [x.strip() for x in property_search.group(1).split(",")]
            type_name = values[0].split(" ")
            if len(type_name) == 2:
                self.__type, self.__name = type_name
            elif len(type_name) == 3:
                #print type_name[:2:]
                self.__type = " ".join(type_name[:2:])
                self.__name = type_name[2]
            if len(values) > 1:
                actions = values[1]
                for v in actions:
                    if v not in "rwnf":
                        print "QSTEROID_ERROR: Problem in property: Q_STEROID_PROPERTY({0})".format(property_search.group(1))
                        print "    There is no {0} flag for code generation. Use ONLY: r-READ, w-WRITE, n-NOTIFY, f-FINAL".format(v)
                        raise KeyboardInterrupt()
                #print actions
                self.__has_read = "r" in actions
                self.__has_write = "w" in actions
                self.__has_notify = "n" in actions
                self.__has_final = "f" in actions
                #print self.__has_read, self.__has_write, self.__has_notify, self.__has_final


class CPPHeader:
    def __init__(self, file_name):
        self.__file_name = file_name
        self.__class_name = ""
        self.__properties = [] #List of Property
        self.__position_dic = {"property": [],
                               "signals": 0,
                               "private": 0,
                               "class_end": 0
        }
        self.__file_lines = []
        self.__current_position = 0

    def digest(self):
        self.parse_file()
        self.inject_code()

    def extract_class_name(self):
        for line, content in enumerate(self.__file_lines):
            if ";" not in content and content.find("class") >= 0:
                line_content = self.__file_lines[line]
                if line_content:
                    self.__class_name = line_content.split(" ")[1]
                break

    def find_positions_of(self, text):
        ret = []
        for line, content in enumerate(self.__file_lines):
            if content.find(text) >= 0:
                print "Found current text: ", text, "at line: ", line
                ret.append(line)
        return ret

    def find_position_of(self, *text):
        for line, content in enumerate(self.__file_lines):
            for t in text:
                if content.find(t) >= 0:
                    return line
        return -1
    
    def parse_file(self):
        f = open(self.__file_name)
        self.__file_lines = f.readlines()
        print "QSTEROID INFO: start to parse the file: ", self.__file_name
        self.extract_class_name()
        self.__position_dic["property"] = self.find_positions_of("Q_STEROID_PROPERTY")
        self.__position_dic["signals"] = self.find_position_of("signals:", "Q_SIGNALS")
        self.__position_dic["private"] = self.find_position_of("public slots:")
        self.__position_dic["class_end"] = self.find_position_of("};")
        #print  self.__position_dic
        
        
    def create_new_cpp(self, methods_implematation):
        cpp_file = open(self.__file_name.replace("hpp", "cpp"), "r")
        cpp_content = cpp_file.read()
        cpp_file.close()
        cpp_content += methods_implematation
        new_cpp = open(self.__file_name.replace("hpp", "cpp_qsteroided"), "w+")
        new_cpp.write(cpp_content)
        new_cpp.close()

    def create_new_hpp(self):
        new_hpp = open(self.__file_name.replace("hpp", "hpp_qsteroided"), "w+")
        new_hpp.write("".join(self.__file_lines))
        new_hpp.close()
        
    def inject_code(self):
        properties = []
        signals = "" if self.__position_dic["signals"] > 0 else "signals:\n"
        methods_signature = ""
        methods_imp = ""
        attributes = "" if self.__position_dic["private"] > 0 else "private:\n"
        for prop in self.__position_dic["property"]:
            new_property = Property(self.__class_name)
            new_property.extract_qsteroid_property_information(self.__file_lines[prop])
            signals += new_property.gen_signal()
            methods_signature += new_property.gen_read_method_signature() + new_property.gen_write_method_signature()
            methods_imp += new_property.gen_read_method_implementation() + new_property.gen_write_method_implementation()
            attributes += new_property.gen_member_attribute()
            self.__file_lines[prop] = new_property.gen_qproperty_code()
        #print methods_signature, signals, methods_imp, attributes
        if len(self.__position_dic["property"]) > 0:
            self.create_new_cpp(methods_imp)
            if self.__position_dic["private"] > 0:
                self.__file_lines.insert(self.__position_dic["private"], attributes)
            else:
                self.__file_lines.insert(self.__position_dic["class_end"], attributes)
            if self.__position_dic["signals"] > 0:
                self.__file_lines.insert(self.__position_dic["signals"] + 1, signals)
                self.__file_lines.insert(self.__position_dic["signals"], methods_signature)
            else:
                self.__file_lines.insert(self.__position_dic["class_end"] - 1, signals)
                self.__file_lines.insert(self.__position_dic["class_end"] - 1, methods_signature)
            self.create_new_hpp()
        else:
            print "QSTEROID WARNING: nothing to process."
    
if __name__ == "__main__":
    try:
        for source in os.listdir("./src"):
            if(source.endswith(".hpp")):
                if os.path.exists(os.path.join(os.path.abspath("./src"),source + "_qsteroided")):
                     print "QSTEROID INFO: File already processed."
                else:
                    target = CPPHeader(os.path.join(os.path.abspath("./src"),source)) 
                    target.digest()
    except:
        pass
            
