import os

# Ideally, a user would import nina_app and then instantiate
# this class and call .run()
class nina_app:
    def __init__(self, app_name, entry_page):
        self.app_name = app_name
        self.entry_page = entry_page

    def run(self):
        try:
            # Instead of formatting to the .py file, we could call
            # nina.router in here to handle routes as normal (such as "/")
            os.system(f"streamlit run pages/{self.entry_page}.py")
        except:
            print(f"Something went wrong when trying to start your nina app")

    
etan_app = nina_app("nina-nutrition", "Home")
etan_app.run()
