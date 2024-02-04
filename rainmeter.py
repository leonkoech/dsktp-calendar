# this script writes onto main.ini in the folder called dsktp calendar
from string import Template
import os
import subprocess
import sys

"""
A class that brings all rainmeter services into one 
the parameters are event_details, destination_directory, and rainmeter directory
"""
class RainMeterService:

        @classmethod  
        def createSkin(cls, event_details, destination, rainmeter, skin_name, max_events):
             cls().defineSkin(event_details, destination, rainmeter, skin_name, max_events)

        def defineSkin(self, event_details, destination, rainmeter, skin_name, max_events):
            self.event_details = event_details
            self.destination_dir = destination
            self.rainmeter_exe = rainmeter
            self.skin_folder = destination
            self.skin_name = skin_name
            self.max_events = max_events
            #the event contains some properties as listed below 
            # {
            # status
            # start
            # end
            # summary
            # description
            # } 
            # important variables for populating events
            self.deletePrevious()
            with open('{skin_name}/main.ini'.format(skin_name=self.skin_name), 'a') as skin, open('components/metadata.txt','r') as metadata:
                # light_color, dark_color, and any other custom
                # write metadata
                # plugin_file = "components/plugin.txt"
                # plugin_template = self.readTemplate(plugin_file)
                # python_location = sys.executable
                # script_location = os.path.join(os.getcwd(),"main.py")
                # plugin_template = plugin_template.safe_substitute(python_location = python_location,script_location = script_location)
       
                for data in metadata:
                    
                    skin.write(data)
                # for data in plugin_template:
                #     skin.write(data)
                metadata.close()
                event_details = sorted(self.event_details, key=lambda x: x['start'])
                # write events
                active_event_length = len(event_details) 
                prev_height = 0
                padding = 15
                for event_index in range(self.max_events):
                    
                    if (event_index < self.max_events and event_index < active_event_length):
                        event = event_details[event_index]
                        event_template = self.readTemplate("components/event.txt")
                        # # index, title, description, theme, start_time, end_time, theme_container
                        index = event_details.index(event)
                        start_time = event.get("start").split(":")
                        start_time_hh = start_time[0]
                        start_time_mm = start_time[-1]
                        end_time = event.get("end").split(":")
                        end_time_hh = end_time[0]
                        end_time_mm = end_time[-1]
                        title = event.get("title")
                        description= event.get("description")
                        container_height = 130 if description != "" else 90
                        description_height = 60 if description != "" else 1
                        link = event.get("htmlLink")
                        event_data = event_template.safe_substitute(index=index, 
                                                            start_time_hh = start_time_hh, 
                                                            start_time_mm = start_time_mm, 
                                                            end_time_hh= end_time_hh, 
                                                            end_time_mm= end_time_mm,
                                                            title=title, 
                                                            description= description, 
                                                            hidden = 0,
                                                            height = container_height,
                                                            description_height = description_height,
                                                            y_position = prev_height,
                                                            link=link)
                        
                        prev_height += container_height + padding
                        skin.write(event_data+'\n\n')
                    elif (event_index >= active_event_length and event_index < self.max_events):
                        event_template = self.readTemplate("components/event.txt")
                        
                        hidden_event_data = event_template.safe_substitute(index=active_event_length+event_index, 
                                                            start_time_hh = "00", 
                                                            start_time_mm = "00", 
                                                            end_time_hh= "23", 
                                                            end_time_mm= "59",
                                                            title="no title", 
                                                            description= "no description", 
                                                            hidden = 1,
                                                            height = 1,
                                                            description_height = 0,
                                                            y_position = prev_height,
                                                            link="no link")
                        prev_height += 1 + padding
                        skin.write(hidden_event_data+'\n\n')
                skin.close()
            self.copySkinFolder()
            self.loadSkin()
            self.refreshSkin()

        def readTemplate(self, filename):
            # Returns a Template object comprising the contents of the 
            # file specified by filename.
            with open(filename, 'r', encoding='utf-8') as template_file:
                template_file_content = template_file.read()
            return Template(template_file_content)   
        
        def deletePrevious(self):
            current_directory = os.getcwd()
            relative_path = "{skin_name}\main.ini".format(skin_name=self.skin_name)
            file_to_delete = os.path.join(current_directory, relative_path)
            try:
                os.remove(file_to_delete)
                print(f"File '{file_to_delete}' has been deleted successfully.")
            except FileNotFoundError:
                # ignore if the file is missing because for new systems, the plugin is not installed
                pass
            except Exception as e:
                print(f"An error occurred: {e}")
                # pass
         
        def copySkinFolder(self):
            source_dir = os.getcwd() + "\\{skin_name}".format(skin_name=self.skin_name)
            if not os.path.exists(self.destination_dir):
                os.makedirs(self.destination_dir)
            copy_command = "xcopy /s /e /y \"{source}\" \"{destination}\"".format(source=source_dir, destination=self.destination_dir)
            subprocess.call(copy_command, shell = True)

        def loadSkin(self):
            command = r'"C:\Program Files\Rainmeter\Rainmeter.exe" !ActivateConfig "{skin_name}" "main.ini"'.format(skin_name=self.skin_name)
            try:
                subprocess.run(command, shell=True)
            except Exception as e:
                print("Error, failed to load skin {}".format(e))


        def refreshSkin(self):
            print("attempting to refresh skin at {}".format(self.skin_folder))
            ini_files = [file for file in os.listdir(self.skin_folder) if file.endswith('.ini')]
            for ini_file in ini_files:
                refresh_command = r'"{rainmeter}" !Refresh "{skin}"'.format(
                    rainmeter=self.rainmeter_exe, skin=os.path.join(self.skin_folder, ini_file)
                )
                try:
                    subprocess.run(refresh_command, shell=True)
                except Exception as e:
                    print("Error, failed to load skin {}".format(e))
