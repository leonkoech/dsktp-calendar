# this script writes onto main.ini in the folder called dsktp calendar

import datetime
from string import Template

def read_template(filename):

    # Returns a Template object comprising the contents of the 
    # file specified by filename.
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def createSkin(event_details):
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
        print(event_details)
        # write events
        for event in event_details:
            event_template = read_template("components/event.txt")
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