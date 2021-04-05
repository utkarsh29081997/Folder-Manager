import os
import CreateFolder


# Getting or Changing Directory.
def check_directory():
    # Getting Path current Folder and changing it to desktop if it's  not.
    get_desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    os.chdir(get_desktop)
    current_dir = os.getcwd()
    CreateFolder.create_folder()


