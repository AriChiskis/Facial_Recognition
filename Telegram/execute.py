import os
import sys
import shutil
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import InputPeerEmpty

from download_data_from_channel import download_media
from download_data_from_channel import create_channel_directory 
from file_classifier import move_files_from_directory


from get_faces import identify_people_from_new_photos_or_videos



def create_directory_structure(base_path, channel_name):
    """
    Create a dictionary that maps directory names to their corresponding paths.

    Parameters:
    base_path (str): The base path where the channel directory is located.
    channel_name (str): The name of the channel directory.

    Returns:
    dict: A dictionary where keys are directory names (photos, videos, text, files, music, faces, new, new_photos, new_music, new_videos, new_text, new_faces)
          and values are the joined paths to those directories within the specified base path.

    Example:
    base_path = "/your/base/path"
    channel_name = "my_channel"
    directories = create_directory_structure(base_path, channel_name)
    # The 'directories' dictionary will contain the following mappings:
    # {
    #     "photos": "/your/base/path/my_channel/photos",
    #     "videos": "/your/base/path/my_channel/videos",
    #     "text": "/your/base/path/my_channel/text",
    #     "files": "/your/base/path/my_channel/files",
    #     "music": "/your/base/path/my_channel/music",
    #     "faces": "/your/base/path/my_channel/faces",
    #     "new": "/your/base/path/my_channel/new",
    #     "new_photos": "/your/base/path/my_channel/new/new_photos",
    #     "new_videos": "/your/base/path/my_channel/new/new_videos",
    #     "new_text": "/your/base/path/my_channel/new/new_text",
    #     "new_music": "/your/base/path/my_channel/new/new_music",
    #     "new_faces": "/your/base/path/my_channel/new/new_faces"
          "new_unknown": "/your/base/path/my_channel/new/new_unknown"
    # }
    """

    channel_directory = os.path.join(base_path, channel_name)
    new_directory = os.path.join(channel_directory, "new")

    directory_structure = {
        "photos": os.path.join(channel_directory, "photos"),
        "videos": os.path.join(channel_directory, "videos"),
        "text": os.path.join(channel_directory, "text"),
        "files": os.path.join(channel_directory, "files"),
        "music": os.path.join(channel_directory, "music"),
        "faces": os.path.join(channel_directory, "faces"),
        "unknown": os.path.join(channel_directory, "unknown"),
        "photos_from_videos":os.path.join(channel_directory, "photos_from_videos"),
        "new": new_directory,
        "new_photos": os.path.join(new_directory, "new_photos"),
        "new_videos": os.path.join(new_directory, "new_videos"),
        "new_text": os.path.join(new_directory, "new_text"),
        "new_music": os.path.join(new_directory, "new_music"),
        "new_faces": os.path.join(new_directory, "new_faces"),
        "new_unknown":os.path.join(new_directory, "new_unknown"),
        "new_photos_from_videos":os.path.join(new_directory, "new_photos_from_videos"),
    }
    return directory_structure


def move_all_files(source_directory, destination_directory):
   
    # Ensure that both source and destination directories exist
    if not os.path.exists(source_directory):
        print(f"Source directory '{source_directory}' does not exist.")
        return
    if not os.path.exists(destination_directory):
        print(f"Destination directory '{destination_directory}' does not exist.")
        return

    try:
        for filename in os.listdir(source_directory):
            source_file = os.path.join(source_directory, filename)
            if os.path.isfile(source_file):
                destination_file = os.path.join(destination_directory, filename)
                shutil.move(source_file, destination_file)
        print(f"All files from '{source_directory}' have been moved to '{destination_directory}'.")
    except Exception as e:
        print(f"An error occurred: {e}")


def read_download_details_from_user(filename):
    try:
        with open(filename, 'r') as file:
            # Read the first line as an integer
            first_line = file.readline().strip()
            api_id = int(first_line)

            # Read the second line as a string
            api_hash = file.readline().strip()

            # You can return both values or use them as needed
            return api_id, api_hash
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except ValueError:
        print("The first line of the file should contain an integer.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def download_media_from_telegram_channel(channel_link,channel_name,user_details_file,PATH_DIR,PATH_dictionary):
     api_id,api_hash = read_download_details_from_user(user_details_file)
     with TelegramClient('name',api_id, api_hash) as client:
        result = client(GetDialogsRequest(
            offset_date=None,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=500,
            hash=0,
        ))

        '''dwonaloading media from telegram'''

        channel = client(GetFullChannelRequest(channel_link))
        num_files_added = download_media(channel_name,channel.full_chat, client,PATH_DIR=PATH_DIR,
                                        FILES_PATH=PATH_dictionary['files'])
     return num_files_added


def detecting_users_from_photos_folder(collectionId,PATH_dictionary,database_path):
        identify_people_from_new_photos_or_videos(collectionId=collectionId,sending_ready_faces_folder=PATH_dictionary['faces'],
                                database_path=database_path,new_photos_folder=PATH_dictionary['new_photos'],
                                creating_faces_folder=PATH_dictionary['new_faces'])


def detecting_users_from_videos_folder(collectionId,PATH_dictionary,database_path):
        new_videos = os.listdir(PATH_dictionary['new_videos'])
        for video in new_videos:
            video_path = os.path.join(PATH_dictionary['new_videos'],video)
            identify_people_from_new_photos_or_videos(collectionId=collectionId,sending_ready_faces_folder=PATH_dictionary['faces'],
                                                      database_path=database_path,new_photos_folder=PATH_dictionary['new_photos_from_videos'],
                                                      creating_faces_folder=PATH_dictionary['new_faces'],video=video_path)
            #cleans new_photos_from_videos for every video
            move_all_files(PATH_dictionary['new_photos_from_videos'],PATH_dictionary['photos_from_videos'])
            


'''CONSTANTS '''
channel_link = 'https://t.me/francefckais' # the title of the channel (this is an example of a chennel link)
PATH_DIR = r'C:\Users\USER\Desktop\Project\Telegram\Channels' #where to put the media
channel_name = sys.argv[1]
collectionId = 'your_collection_id'
database_path = r'C:\Users\USER\Desktop\Project\DataBase'
user_details_file = r'C:\Users\USER\Desktop\Project\Telegram\download_user_detalis\user_details.txt'
categories = [('photos', 'new_photos'), ('videos', 'new_videos'), ('text', 'new_text'), ('unknown', 'new_unknown'),
                ('music', 'new_music'), ('faces', 'new_faces'),("photos_from_videos","new_photos_from_videos")]







if __name__ == '__main__':

    if not os.path.exists(os.path.join(PATH_DIR,channel_name)):
        create_channel_directory(path=PATH_DIR,channel_name=channel_name)
    else:
        print('dir ',channel_name,' exists\n')

    PATH_dictionary = create_directory_structure(base_path=PATH_DIR,channel_name=channel_name)
    num_files_added = download_media_from_telegram_channel(channel_link=channel_link,channel_name=channel_name,
                                         user_details_file=user_details_file,PATH_DIR=PATH_DIR,PATH_dictionary=PATH_dictionary)


    if (num_files_added != 0): #checks if we download media
        move_files_from_directory(source_dir=PATH_dictionary['files'],main_folder=PATH_dictionary['new'])

        '''starting activate aws services (rekognition)'''
        ''' detecting faces from photos'''

        detecting_users_from_photos_folder(collectionId=collectionId,PATH_dictionary=PATH_dictionary,database_path=database_path)


        '''detecting faces from videos'''
        detecting_users_from_videos_folder(collectionId=collectionId,PATH_dictionary=PATH_dictionary,database_path=database_path)


        identify_people_from_new_photos_or_videos(collectionId=collectionId,sending_ready_faces_folder=PATH_dictionary["faces"],
                                         database_path=database_path,new_photos_folder=PATH_dictionary["new_photos"],
                                         creating_faces_folder=PATH_dictionary['new_faces'])


        '''move all files to new files'''
        for category in categories:
            move_all_files(PATH_dictionary[category[1]],PATH_dictionary[category[0]])
            







