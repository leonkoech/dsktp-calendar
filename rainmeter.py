# this script writes onto main.ini in the folder called dsktp calendar
from string import Template
import os
import subprocess

class RainMeterService:
        def __init__(self, event_details, destination, rainmeter):
            self.event_details = event_details
            self.destination_dir = destination
            self.rainmeter_exe = r'{rainmeter}'.format(rainmeter)
            self.skin_folder = r'{skin_folder}'.format(destination)

        def createSkin(self):
            #the event contains some properties as listed below 
            # {
            # status
            # start
            # end
            # summary
            # description
            # } 

            # important variables for populating events
            light = { 'theme': "Light", "image":"open.png" }
            dark = { 'theme': "Dark", "image":"openlight.png" }
            
            with open('dsktp calendar/main.ini', 'a') as skin, open('components/metadata.txt','r') as metadata:
                # write metadata
                for data in metadata:
                        skin.write(data)
                metadata.close()
                event_details = sorted(self.event_details, key=lambda x: x['start'])
                print(event_details)
                # write events
                for event in event_details:
                    event_template = self.read_template("components/event.txt")
                    # # index, title, description, theme, start_time, end_time, theme_container
                    # # mama victor
                    index = event_details.index(event)
                    start_time = event.get("start")
                    end_time = event.get("end")
                    title = event.get("title")
                    description= event.get("description")
                    theme = dark["theme"] if (event.get("status", "") == "confirmed") else light["theme"]
                    image = dark["image"] if (event.get("status", "") == "confirmed") else light["image"]
                    theme_container = theme+"Container"
                    link = event.get("htmlLink")
                    event_data = event_template.safe_substitute(index=index, 
                                                        start_time = start_time, 
                                                        end_time= end_time, 
                                                        title=title, 
                                                        description= description, 
                                                        theme=theme, 
                                                        link=link,
                                                        image=image,
                                                        theme_container= theme_container)
                    skin.write(event_data+'\n\n')
                skin.close()
            self.copySkinFolder()

        def read_template(self, filename):
            # Returns a Template object comprising the contents of the 
            # file specified by filename.
            with open(filename, 'r', encoding='utf-8') as template_file:
                template_file_content = template_file.read()
            return Template(template_file_content)   
         
        def copySkinFolder(self):
            source_dir = os.getcwd() + "\\dsktp calendar"
            if not os.path.exists(self.destination_dir):
                os.makedirs(self.destination_dir)
            copy_command = "xcopy /s /e /y \"{source}\" \"{destination}\"".format(source=source_dir, destination=self.destination_dir)
            subprocess.call(copy_command, shell = True)

        def refreshSkin(self):
            ini_files = [file for file in os.listdir(self.skin_folder) if file.endswith('.ini')]
            for ini_file in ini_files:
                refresh_command = r'"{rainmeter}" !Refresh "{skin}"'.format(
                    rainmeter=self.rainmeter_exe, skin=os.path.join(self.skin_folder, ini_file)
                )
                subprocess.run(refresh_command, shell=True)
