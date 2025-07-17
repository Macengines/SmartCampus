#region imports from python in-buit and installed modules
import json
import os
import textwrap
import mysql.connector
from threading import Thread
import requests
import pymysql
#endregion

#region kivy & kivymd imports
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import  ColorProperty, StringProperty, ObjectProperty, NumericProperty, ListProperty
from kivy.utils import rgba, QueryDict
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.filemanager import MDFileManager
from kivy.properties import Clock
from kivy.clock import Clock
from kivy.clock import mainthread
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.uix.image import AsyncImage
from kivymd.uix.fitimage import FitImage
from kivy.uix.image import Image
from kivy.uix.screenmanager import RiseInTransition
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivy.uix.modalview import ModalView
from kivymd.toast import toast
from datetime import datetime
from kivy.uix.spinner import Spinner, SpinnerOption
#endregion

#region Custome Widgets By Mactechholdings
from cwidgets.draw import DrawWidget
from cwidgets.box2 import BackBox2
from cwidgets.box import BackBox
from cwidgets.textfields import FlatField
from cwidgets.labels import Text
#endregion

#region Requests to online resources
API_URL = "http://127.0.0.1:5000/api/news"
API_URL2 = "http://127.0.0.1:5000/api/zuva"
API_URL3 = "http://127.0.0.1:5000/api/news2"
API_URL4 = "http://127.0.0.1:5000/api/files"
API_URL5 = "http://127.0.0.1:5000/api/videos"
API_URL6 = "http://127.0.0.1:5000/api/images"
API_URL7 = "http://localhost:5000/api/store_student"
API_URL8 = "http://localhost:5000/api/update_level"
#endregion

class ColoredSpinnerOption(SpinnerOption):
    color = ColorProperty(rgba('#733700')) 
    background_normal = "" 
#screen manager
class MainWindow(MDBoxLayout):   
    def __init__(self, **kw):
        super().__init__(**kw)

#Loading screen
class LoadingScreen(MDBoxLayout):   
    def __init__(self, **kw):
        super().__init__(**kw)

#signup screen
class SignupScreen(MDBoxLayout):
    departments = ListProperty()
    error = StringProperty()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #load departments and courses json file locally
        with open("dep.json", "r") as f:
            self.dept_courses = json.load(f)
        #displays departments
        self.departments = list(self.dept_courses.keys())

    #displays course for selected department
    def choose_course(self, selected_depart):
        courses = self.dept_courses.get(selected_depart, [])
        course_spinner = self.ids.course_spinner
        course_spinner.values = courses
        course_spinner.text = "Choose a Course"
    
    # get, push, store user details in json file and db
    def store_details(self):
        # Get user input
        fname = self.ids.fname.text.strip()
        sname = self.ids.sname.text.strip()
        dept = self.ids.dept.text.strip()
        sid = self.ids.sid.text.strip()
        cname = self.ids.course_spinner.text.strip()
        level = self.ids.level_save.text.strip()
        #validate user input 
        if fname == "":
            self.error= "Fill the name please!"
        elif sname =="":
            self.error ="Fill the surname please!"
        elif sid == "":
            self.error= "Please input school id number!"
        elif dept == "Click to choose Department":
            self.error= "Please select your department!"
        elif cname == "Choose a Course":
            self.error= "Please select your course!"
        elif level == "LEVEL":
            self.error= "Please select your level!"        
        else:
        # Create a student dictionary
            student = {
                "NAME": fname,
                "SURNAME": sname,
                "STUDENT ID": sid,
                "DEPARTMENT": dept,
                "COURSE": cname,
                "LEVEL": level
            }

            # Save the student data to a JSON file
            with open("students.json", "w") as f:
                json.dump(student, f)
            # Save the student data to a db
            try:
                response = requests.post(API_URL7, json=student)
                if response.status_code == 200:
                    self.error = "successfully saved"
                else:
                    self.error = response.json().get("message")
            except Exception as e:
                print("❌ Connection error:", str(e))


            # Update HomeScreen with details
            app = MDApp.get_running_app()
            home_screen = app.root.ids.hscreen
            home_screen.update_details(student)

            # Navigate to home screen
            app.root.ids.scrn_mngr.current = "home_scrn"
            app.root.ids.scrn_mngr.transition.direction = "left"
                
#home screen
class HomeScreen(MDBoxLayout):
    name = StringProperty("")
    course = StringProperty("")
    sid = StringProperty("")
    level = StringProperty("")
    #home screen
    def update_details(self, student):
        self.name = student.get("NAME", "")
        self.course = student.get("COURSE", "")
        self.sid = student.get("STUDENT ID", "")
        self.level = student.get("LEVEL", "")
        
    def __init__(self, *args, **kwargs, ):
        super().__init__(*args, **kwargs)
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,

        )

    
    def update_level(self, new_level):
        print("Updating level to:", new_level)
        
        # Load user data
        with open("students.json", "r") as f:
            data = json.load(f)
        
        # Update the level
        data["LEVEL"] = new_level
        
        # Save it back
        with open("students.json", "w") as f:
            json.dump(data, f, indent=4)
        
        Thread(target=self.send_level_to_server, args=(new_level,)).start()
    def send_level_to_server(self, level):
        try:
            response = requests.post(API_URL8, timeout=5)
            if response.status_code == 200:
                print("✅ level changed in DB")
            else:
                print("❌ DB error:", response.json().get("message"))
        except Exception as e:
            print("❌ Offline or server error:", str(e))

    def file_chooser(self, *args):
        self.file_manager.show("/")
    
    def exit_manager(self, *args):
        self.file_manager.close() 

    def nav_nts(self):
        MDApp.get_running_app().root.ids.scrn_mngr.current = "notes_scrn"
        MDApp.get_running_app().root.ids.scrn_mngr.transition.direction = "left"
    
    def nav_imgs(self):
        MDApp.get_running_app().root.ids.scrn_mngr.current = "imgs_scrn"
        MDApp.get_running_app().root.ids.scrn_mngr.transition.direction = "left"
    
    def nav_vds(self):
        MDApp.get_running_app().root.ids.scrn_mngr.current = "vds_scrn"
        MDApp.get_running_app().root.ids.scrn_mngr.transition.direction = "left"

    def nav_tims(self):
        MDApp.get_running_app().root.ids.scrn_mngr.current = "tims_scrn"
        MDApp.get_running_app().root.ids.scrn_mngr.transition.direction = "left"

    def nav_assng(self):
        MDApp.get_running_app().root.ids.scrn_mngr.current = "assng_scrn"
        MDApp.get_running_app().root.ids.scrn_mngr.transition.direction = "left"
    
    def nav_nwz(self):
        MDApp.get_running_app().root.ids.scrn_mngr.current = "nwz_scrn"
        MDApp.get_running_app().root.ids.scrn_mngr.transition.direction = "left"

    #downloaded screen
    def add(self):
        bk = MDBoxLayout(
            size_hint_y = None,
            height = ("35dp"),
            bcolor =rgba("#FFFFFF"),
            radius = [5,5,5,5]
        )
        ff=FlatField(
            hint_text="FIRST NAME",
            multiline=False,
            hint_text_color= rgba("#7F7F7F")
        )

        ff.focus = True
        bk.add_widget(ff)
        

        if self.ids.sh.icon == "text-box-remove-outline" :
            self.ids.searchb.add_widget(bk)    
        else:
            self.ids.searchb.clear_widgets()
    
#notes screen
class FilesScreen(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_kv_post(self, base_widget):
        self.add_notes()


    def add_notes(self):
        try:
            response = requests.get(API_URL4)
            response.raise_for_status()  
            files_list = response.json()
            for file in files_list:
                self.get_files( file['file_name'], file['file_size'], file['date_added'] , file['downloads'] , file['ratings'])
        except requests.RequestException as e:
            print(f"Error fetching files: {e}")
            return  

    def format_number(self, value):
        if value >= 1_073_741_824:
            return f"{value / 1_073_741_824:.1f}GB"  # Divide by 1,000,000 and keep one decimal
        elif value >= 1_048_576:
            return f"{value / 1_048_576:.1f}MB"  # Divide by 1,000 and keep one decimal
        elif value >= 1_024:
            return f"{value / 1_024:.1f}KB"
        elif value >= 0:
            return f"{value / 1:.0f}Bit"
        else:
            return str(value)
        
    def format_downloads(self, value):
        if value >= 1_000_000:
            return f"{value / 1_000_000:.1f}M"  # Divide by 1,000,000 and keep one decimal
        elif value >= 1_000:
            return f"{value / 1_000:.1f}K"  # Divide by 1,000 and keep one decimal
        else:
            return str(value)
    

    def get_files(self, file_name, file_size, date_added, downloads, ratings):
        print(file_name)
        grid = self.ids.gl_files

        # splitting the date displaying
        try:
            
            formatted_date = datetime.strptime(date_added, "%a, %d %b %Y %H:%M:%S %Z").strftime("%a, %d-%m-%Y")
        except ValueError as e:
            print(f"Error parsing date: {e}")
            formatted_date = date_added  # Fallback to the original value if parsing fails
        #sizing
        try:
            formatted_size = self.format_number(file_size)
        except ValueError as e:
            formatted_size = file_size

        #download formating
        try:
            formatted_download = self.format_downloads(downloads)
        except ValueError as e:
            formatted_download = downloads
        

        ft = FilesTile()
        ft.file_name = file_name
        ft.file_size = formatted_size
        ft.date_added = formatted_date  
        ft.downloads = formatted_download

        grid.add_widget(ft)

    
        
    

    #searchtopbar
    def add(self):
        bk = BackBox(
            size_hint_y = None,
            height = ("35dp"),
            bcolor =rgba("#FFFFFF"),
            radius = [5,5,5,5]
        )
        ff=FlatField(
            hint_text="FIRST NAME",
            multiline=False,
            hint_text_color= rgba("#7F7F7F")
        )

        ff.focus = True
        bk.add_widget(ff)
        

        if self.ids.sh.icon == "text-box-remove-outline" :
            self.ids.searchb.add_widget(bk)    
        else:
            self.ids.searchb.clear_widgets()

#files screen
class FilesTile(MDBoxLayout):
    file_size = ObjectProperty("")
    file_name = ObjectProperty("")
    date_added = ObjectProperty("")
    downloads = ObjectProperty("")
    rating = ObjectProperty("")
    def toggle_like(self):
        # Access the current like counter
        current_likes = int(self.rating)
        
        # Update the counter based on the current icon state
        if self.ids.like.icon == "cards-heart-outline":
            self.ids.like.icon = "cards-heart"
            self.ids.like.text_color = rgba("#0070C0")
            current_likes += 1
        else:
            self.ids.like.icon = "cards-heart-outline"
            self.ids.like.text_color = rgba("#000000")
            current_likes -= 1
        
        # Update the rating text
        self.rating = str(current_likes)
        self.ids.counter.text = self.rating
        print(f"Updated likes to: {self.rating}")


    def add(self):
        bk = MDBoxLayout(
            size_hint_y = None,
            height = ("35dp"),
            bcolor =rgba("#FFFFFF"),
            radius = [5,5,5,5]
        )
        ff=FlatField(
            hint_text="FIRST NAME",
            multiline=False,
            hint_text_color= rgba("#7F7F7F")
        )

        ff.focus = True
        bk.add_widget(ff)
        

        if self.ids.sh.icon == "text-box-remove-outline" :
            self.ids.searchb.add_widget(bk)    
        else:
            self.ids.searchb.clear_widgets()

#images screen
class NotesScreen(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_kv_post(self, base_widget):
        self.add_notes()

    
    def add_notes(self):
        grid = self.ids.image_grid

        
        card = BackBox2(
            size_hint_x=1,
            size_hint_y= None,
            height = ("300dp"),
            orientation="vertical",
            radius = [5]
        )

        note_dis = MDCard(
            orientation = "vertical",
            size_hint_y = .78,
            elevation=1,  
            radius=[10],
            padding = 20
        )
        


        button_dis = MDLabel(
            text=textwrap.shorten(
                text="harare",
                width=1000,  # Limit to 50 characters
                placeholder="..."
            ),
            valign="top"  # Align text to the top
        )

        button_dis.bind(size=button_dis.setter("text_size"))  # Ensure proper alignment

        head = MDLabel(
            size_hint_y = .07,
            text = "title",
            halign = "center"
        )
        date = MDLabel(
            size_hint_y = .05,
            text = "14 feb",
            halign = "center"
            
        )

        
        note_dis.add_widget(button_dis)
        card.add_widget(note_dis)
        card.add_widget(head)
        card.add_widget(date)
        card.bind(on_touch_down=lambda instance, touch: self.show_notes() 
                if instance.collide_point(*touch.pos) else None)
        # Add the card to the grid
        grid.add_widget(card)


    def show_notes(self):
        mw = NotesWrite()
        mw.open()

    
    #searchtopbar
    def add(self):
        bk = BackBox(
            size_hint_y = None,
            height = ("35dp"),
            bcolor =rgba("#FFFFFF"),
            radius = [5,5,5,5]
        )
        ff=FlatField(
            hint_text="FIRST NAME",
            multiline=False,
            hint_text_color= rgba("#7F7F7F")
        )

        ff.focus = True
        bk.add_widget(ff)
        

        if self.ids.sh.icon == "text-box-remove-outline" :
            self.ids.searchb.add_widget(bk)    
        else:
            self.ids.searchb.clear_widgets()

#Creative Space
class NotesWrite(ModalView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def clear(self):
        # Corrected reference to the draw widget
        draw_widget = self.ids.draw_widget  
        draw_widget.clear_canvas()
    def toggle_pencil(self):
        # Toggle drawing mode
        draw_widget = self.ids.draw_widget
        draw_widget.drawing_enabled = not draw_widget.drawing_enabled
        draw_widget.text = "Deactivate Pencil" if draw_widget.drawing_enabled else "Activate Pencil"
           
#videos screen
class VideosScreen(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_kv_post(self, base_widget):
        self.add_videos()

    def add_videos(self):
        try:
            response = requests.get(API_URL5)
            response.raise_for_status()  
            videos_list = response.json()
            for video in videos_list:
                self.get_videos( video['thumbnail_path'], video['file_name'], video['duration'], video['downloads'], video['views'])
        except requests.RequestException as e:
            print(f"Error fetching news: {e}")
            return
 

    def get_videos(self, thumbnail_path, file_name, duration, views, downloads):
        grid = self.ids.gl_videos

        vt =VideosTile()
        vt.name = file_name
        vt.thumbnail = thumbnail_path
        vt.duration = duration 
        vt.views = views
        vt.downloads = downloads
        grid.add_widget(vt)


    def add(self):
        bk = MDBoxLayout(
            size_hint_y = None,
            height = ("35dp"),
            bcolor =rgba("#FFFFFF"),
            radius = [5,5,5,5]
        )
        ff=FlatField(
            hint_text="FIRST NAME",
            multiline=False,
            hint_text_color= rgba("#7F7F7F")
        )

        ff.focus = True
        bk.add_widget(ff)
        

        if self.ids.sh.icon == "text-box-remove-outline" :
            self.ids.searchb.add_widget(bk)    
        else:
            self.ids.searchb.clear_widgets()

#Videos tiles            
class VideosTile(MDBoxLayout):
    name = ObjectProperty("")
    thumbnail = ObjectProperty("")
    duration = ObjectProperty("")
    views = ObjectProperty("")
    downloads = ObjectProperty("")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

#tims screen
class TimsScreen(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def add(self):
        bk = MDBoxLayout(
            size_hint_y = None,
            height = ("35dp"),
            bcolor =rgba("#FFFFFF"),
            radius = [5,5,5,5]
        )
        ff=FlatField(
            hint_text="FIRST NAME",
            multiline=False,
            hint_text_color= rgba("#7F7F7F")
        )

        ff.focus = True
        bk.add_widget(ff)
        

        if self.ids.sh.icon == "text-box-remove-outline" :
            self.ids.searchb.add_widget(bk)    
        else:
            self.ids.searchb.clear_widgets()

#assng screen
class AssngScreen(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def on_kv_post(self, base_widget):
        self.add_notes()


    def add_notes(self):
        try:
            response = requests.get(API_URL4)
            response.raise_for_status()  
            files_list = response.json()
            for file in files_list:
                self.get_notes( file['file_name'], file['file_size'], file['date_added'] , file['downloads'] , file['ratings'])
        except requests.RequestException as e:
            print(f"Error fetching news: {e}")
            return  

    def format_number(self, value):
        if value >= 1_073_741_824:
            return f"{value / 1_073_741_824:.1f}GB"  # Divide by 1,000,000 and keep one decimal
        elif value >= 1_048_576:
            return f"{value / 1_048_576:.1f}MB"  # Divide by 1,000 and keep one decimal
        elif value >= 1_024:
            return f"{value / 1_024:.1f}KB"
        elif value >= 0:
            return f"{value / 1:.0f}Bit"
        else:
            return str(value)
        
    def format_downloads(self, value):
        if value >= 1_000_000:
            return f"{value / 1_000_000:.1f}M"  # Divide by 1,000,000 and keep one decimal
        elif value >= 1_000:
            return f"{value / 1_000:.1f}K"  # Divide by 1,000 and keep one decimal
        else:
            return str(value)
    
    



    def get_notes(self, file_name, file_size, date_added, downloads, ratings):
        grid = self.ids.gl_assgn

        # splitting the date displaying
        try:
            
            formatted_date = datetime.strptime(date_added, "%a, %d %b %Y %H:%M:%S %Z").strftime("%a, %d-%m-%Y")
        except ValueError as e:
            print(f"Error parsing date: {e}")
            formatted_date = date_added  # Fallback to the original value if parsing fails
        #sizing
        try:
            formatted_size = self.format_number(file_size)
        except ValueError as e:
            formatted_size = file_size

        #download formating
        try:
            formatted_download = self.format_downloads(downloads)
        except ValueError as e:
            formatted_download = downloads

        nt = AssngTile()
        nt.file_name = file_name
        nt.file_size = formatted_size
        nt.date_added = formatted_date  
        nt.downloads = formatted_download
        

        grid.add_widget(nt)

    def add(self):
        bk = MDBoxLayout(
            size_hint_y = None,
            height = ("35dp"),
            bcolor =rgba("#FFFFFF"),
            radius = [5,5,5,5]
        )
        ff=FlatField(
            hint_text="FIRST NAME",
            multiline=False,
            hint_text_color= rgba("#7F7F7F")
        )

        ff.focus = True
        bk.add_widget(ff)
        

        if self.ids.sh.icon == "text-box-remove-outline" :
            self.ids.searchb.add_widget(bk)    
        else:
            self.ids.searchb.clear_widgets()

class AssngTile(MDBoxLayout):
    file_size = ObjectProperty("")
    file_name = ObjectProperty("")
    date_added = ObjectProperty("")
    downloads = ObjectProperty("")
    rating = ObjectProperty("")
    def toggle_like(self):
        print("liked")

    def add(self):
        bk = MDBoxLayout(
            size_hint_y = None,
            height = ("35dp"),
            bcolor =rgba("#FFFFFF"),
            radius = [5,5,5,5]
        )
        ff=FlatField(
            hint_text="FIRST NAME",
            multiline=False,
            hint_text_color= rgba("#7F7F7F")
        )

        ff.focus = True
        bk.add_widget(ff)
        

        if self.ids.sh.icon == "text-box-remove-outline" :
            self.ids.searchb.add_widget(bk)    
        else:
            self.ids.searchb.clear_widgets()

#news screen
class NewsScreen(MDBoxLayout):
    date = StringProperty("")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

   #top cards       
    def on_kv_post(self, base_widget):
        self.add_news_card()
        self.add_dates()
        self.add_news_card2()
 
    def add_news_card(self):
        try:
            response = requests.get(API_URL)
            response.raise_for_status()  # Raise an error if the request fails
            news_list = response.json()
            for news in news_list:
                self.gridtake(news['title'], news.get('image_url'), news['detailed1'])
        except requests.RequestException as e:
            print(f"Error fetching news: {e}")
            return  # Exit early on failure

    def gridtake(self, title, image_url, detailed1):
        grid = self.ids.news_grid
        # Card container
        card = MDBoxLayout(
            size_hint_x=None,
            width=("390dp"),
            size_hint_y= 1,
            orientation="vertical", 
            padding = 5,
        )
        
        imgcard = MDCard(
            size_hint_x=None,
            width="380dp",
            size_hint_y= .8,
            orientation="vertical",
            elevation=1,  
            radius=[10],
        )
        
        image = FitImage(
            source=image_url, 
            size_hint=(1, 1), 
            radius= [10]
        )
        
        label = MDLabel(
            size_hint_y= .2,
            text=title,
            halign="left",
            valign="center",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),  
            bold=True,
            font_name = '.venv/assets/fonts/Roboto-Medium.ttf',
        )
        imgcard.add_widget(image)
        card.add_widget(imgcard)
        card.add_widget(label)

        card.bind(on_touch_down=lambda instance, touch: self.show_news_popu(title, detailed1) 
                  if instance.collide_point(*touch.pos) else None)

        # Add the card to the grid
        grid.add_widget(card)

    def show_news_popu(self, title, detailed1):
        md = NewsPop()
        md.heading = title
        md.body = detailed1
        md.open()

    #top section
    def add_dates(self):
        try:
            response = requests.get(API_URL2)
            response.raise_for_status()  
            dats_list = response.json()

        except requests.RequestException as e:
            print(f"Error fetching dates: {e}")
            return  # Exit early on failure
        
        for d in dats_list:
            date = d['dat']
        
        self.date = date
    
    #bottom cards
    def add_news_card2(self):
        try:
            response = requests.get(API_URL3)
            response.raise_for_status()  
            new_list = response.json()
            for new in new_list:
                self.gridtake2( new['title2'], new.get('image_url2'),new['head'], new['detailed'])
        except requests.RequestException as e:
            print(f"Error fetching news: {e}")
            return  

    def gridtake2(self, title2, image_url2, head, detailed):
        grid = self.ids.news_grid2
        # Card container
        card2 = MDBoxLayout(
            size_hint_y= None,
            height="220dp",
            size_hint_x = .2 ,
            orientation="vertical",  # White background
            padding = 10,
            spacing = 10,
        )
        
        imgcard2 = MDCard(
            size_hint_x= None,
            width = "180dp",
            size_hint_y= .5,
            orientation="vertical",
            elevation=0.5,  # Shadow
            radius=[10],
            md_bg_color=[0, 0, 0, 1] 
        )
        
        # Background image
        image2 = FitImage(
            source= image_url2, 
            size_hint=(1, 1), 
            radius= [10]
        )
        

        # Add the title text
        label2 = MDLabel(
            size_hint_y= .4,
            text= title2,
            halign="left",
            valign="center",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),  # White text
            bold=True,
            font_name = '.venv/assets/fonts/Roboto-Medium.ttf',
        )
        heading = MDLabel(
            size_hint_y= None,
            height = dp(15),
            text= head ,
            halign="left",
            valign="center",
            theme_text_color="Custom",
            text_color= rgba("#00B0F0"),  # White text
            bold=True,
            font_name = 'fonts/Roboto-Bold.ttf',
            font_size = dp(16)
        )
        imgcard2.add_widget(image2)
        card2.add_widget(imgcard2)
        card2.add_widget(heading)
        card2.add_widget(label2)
        
        card2.bind(on_touch_down=lambda instance, touch: self.show_news_popup(title2, detailed) 
                  if instance.collide_point(*touch.pos) else None)

        # Add the card to the grid
        grid.add_widget(card2)

    def show_news_popup(self, title2, detailed):
        md = NewsPop()
        md.heading = title2
        md.body = detailed
        md.open()

    def add(self):
        bk = MDBoxLayout(
            size_hint_y = None,
            height = ("35dp"),
            bcolor =rgba("#FFFFFF"),
            radius = [5,5,5,5]
        )
        ff=FlatField(
            hint_text="FIRST NAME",
            multiline=False,
            hint_text_color= rgba("#7F7F7F")
        )

        ff.focus = True
        bk.add_widget(ff)
        

        if self.ids.sh.icon == "text-box-remove-outline" :
            self.ids.searchb.add_widget(bk)    
        else:
            self.ids.searchb.clear_widgets()

#news            
class NewsPop(ModalView):
    heading = StringProperty("")
    body = StringProperty("")


#app properties
class SmartCampus(MDApp):
    
    def build(self):
        # Initialize the MainWindow
        self.load = MainWindow()
        self.load.ids.scrn_mngr.current = "loading_scrn"

        # Schedule switching to the appropriate screen after 3 seconds
        Clock.schedule_once(self.switch_to_main, 3)


        return self.load
    
    def switch_to_main(self, *args):

        # Check if the JSON file exists
        if os.path.exists("students.json"):
            with open("students.json", "r") as f:
                data = json.load(f)

            # Handle both list and dictionary cases
            if isinstance(data, list):  # If it's a list, fetch the first student
                student = data[0] if data else {}
            elif isinstance(data, dict):  # If it's a dictionary, use it directly
                student = data
            else:
                student = {}

            # Update HomeScreen with the student's details
            home_screen = self.load.ids.hscreen
            home_screen.update_details(student)

            # Switch to the HomeScreen
            self.load.ids.scrn_mngr.current = "home_scrn"
        else:
            # Switch to SignupScreen if no data exists
            self.load.ids.scrn_mngr.current = "signup_scrn"
            self.load.ids.scrn_mngr.transition.direction = "left"

            Clock.schedule_once(lambda dt: self.load.ids.scrn_mngr.get_screen("signup_scrn").canvas.ask_update(), 0.1)
 
    # load back to home screen
    def nav_bck(self):
        MDApp.get_running_app().root.ids.scrn_mngr.current = "home_scrn"
        MDApp.get_running_app().root.ids.scrn_mngr.transition.direction = "right"

    

    theme = "light"
    color_bg_cream = ColorProperty(rgba("#E9E3E3"))
    color_bg_white = ColorProperty(rgba("#FFFFFF"))
    color_bg_black = ColorProperty(rgba("#000000"))
    color_light_blue = ColorProperty(rgba("#00B0F0"))
    color_light_blue2 = ColorProperty(rgba("#C1E5F5"))
    color_dark_blue = ColorProperty(rgba("#0070C0"))
    color_bg_grey = ColorProperty(rgba("#EFEFEF"))
    color_bg_dovegrey = ColorProperty(rgba("#3D5F62"))
    color_text_light = ColorProperty(rgba("#7F7F7F"))
    color_stars_yellow = ColorProperty(rgba("#FFFF00"))
    color_primary_bg = ColorProperty(rgba("#FFFFFF"))
    color_bg_orange = ColorProperty(rgba("#FFFFFF"))
    #new to use colors
    white = ColorProperty(rgba("#FFFFFF"))
    Light_Cyan_Blue = ColorProperty(rgba('#00b0f0')) #Primary
    Strong_Blue = ColorProperty(rgba('#007cb8')) #Accent/Dark tone
    Very_Light_Cyan = ColorProperty(rgba('#cdf6ff'))#Background/Highlight
    blue_bg =ColorProperty(rgba("#25E0FF"))
    Deep_Brown = ColorProperty(rgba('#733700'))#Text or Contrast
    Red = ColorProperty(rgba("#FF1317"))



    # font size
    fonts = QueryDict()
    fonts.size = QueryDict()
    fonts.size.extra = dp(38)
    fonts.size.h1 = dp(24)
    fonts.size.h2 = dp(22)
    fonts.size.h3 = dp(18)
    fonts.size.h4 = dp(16)
    fonts.size.h5 = dp(14)
    fonts.size.h6 = dp(12)

    # font name
    fonts.heading = 'fonts/Roboto-Bold.ttf'
    fonts.subheading = '.venv/assets/fonts/Roboto-Medium.ttf'
    fonts.body = '.venv/assets/fonts/Roboto-Regular.ttf'
    fonts.styled = ".venv/assets/fonts/Lobster-Regular.ttf"
    fonts.algeria = ".venv/assets/fonts/ALGER.ttf"
    fonts.romans = ".venv/assets/fonts/Times New Roman.ttf"
    

if __name__ == "__main__":
    SmartCampus().run()