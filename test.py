from string import Template
import sys
import os

print(sys.executable)
plugin_file = "components/plugin.txt"
def readTemplate( filename):
            # Returns a Template object comprising the contents of the 
            # file specified by filename.
            with open(filename, 'r', encoding='utf-8') as template_file:
                template_file_content = template_file.read()
            return Template(template_file_content) 

plugin_template = readTemplate(plugin_file)
python_location = sys.executable
script_location = os.path.join(os.getcwd(),"main.py")
plugin_template = plugin_template.safe_substitute(python_location = python_location,script_location = script_location)

with open(plugin_file, 'w') as file:
    file.write(plugin_template)
