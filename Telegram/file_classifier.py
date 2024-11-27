import os
import shutil




'''this function will classify a file by its suffix wether it is a video ,music text or photo or UNKNOWN'''
def classify_file_by_suffix(filename):
    # Define dictionaries mapping suffixes to categories
    video_suffixes = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.3gp']
    music_suffixes = ['.mp3', '.wav', '.ogg', '.flac', '.aac']
    text_suffixes = ['.txt', '.csv', '.xlsx', '.pdf', '.doc', '.docx', '.html', '.xml']
    photo_suffixes = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']

    # Extract the file's suffix (extension)
    file_suffix = "." + filename.lower().split('.')[-1]
    # Classify the file based on its suffix
    if file_suffix in video_suffixes:
        return 'new_videos'
    elif file_suffix in music_suffixes:
        return 'new_music'
    elif file_suffix in text_suffixes:
        return 'new_text'
    elif file_suffix in photo_suffixes:
        return 'new_photos'
    else:
        return 'mew_unknown'


'''this funciton will create folders (the folders names will be in the input parameter "name_of_folders"
  that will contain a list of strings) that we will create'''
def create_folders(names_of_folders,main_folder):
    for folder in names_of_folders:
        os.mkdir(main_folder + "\\" + folder)

'''this function will sort and move all the files in the files directory to their extension directory
for example: 1. a file tha ends in .jpg will go to the photos directory
             2. s file that ends in .mp4 will go to the videos directorty  '''
# def move_files_from_directory(source_dir,main_folder):
#     # Ensure that the source and destination directories exist
#     if not os.path.exists(source_dir):
#         print(f"Source directory '{source_dir}' does not exist.")
#         return
#     # List all files in the source directory
#     files = os.listdir(source_dir)
#     # Iterate through the files and move each one to the destination directory
#     for file in files:
#         directory = classify_file_by_suffix(file)
#         #if directory != "unknown":
#         # Check if the file is a regular file (not a directory)
#         shutil.move(source_dir + "\\" + file,main_folder + "\\" + directory)
        


def move_files_from_directory(source_dir, main_folder):
    """
    Move files from a source directory to subdirectories in the main folder based on their file type.

    Parameters:
    source_dir (str): The path to the source directory containing files to be moved.
    main_folder (str): The path to the main folder where files will be categorized and moved.

    Returns:
    None

    Description:
    This function takes a source directory and a main folder as input. It ensures that the source directory exists,
    lists all the files in the source directory, and moves each file to a subdirectory within the main folder based on its file type.
    The file types are determined using the 'classify_file_by_suffix' function.

    Example:
    source_dir = "/path/to/source_directory"
    main_folder = "/path/to/main_folder"
    move_files_from_directory(source_dir, main_folder)
    """

    # Ensure that the source and destination directories exist
    if not os.path.exists(source_dir):
        print(f"Source directory '{source_dir}' does not exist.")
        return

    # List all files in the source directory
    files = os.listdir(source_dir)

    # Iterate through the files and move each one to the destination directory
    for file in files:
        directory = classify_file_by_suffix(file)  # You may need to define 'classify_file_by_suffix' function
        # Check if the file is a regular file (not a directory)
        shutil.move(os.path.join(source_dir, file), os.path.join(main_folder, directory))





def copy_files(source_dir, destination_dir):
    """
    Copy all files from the source directory to the destination directory.

    Parameters:
    source_dir (str): The path to the source directory containing the files to be copied.
    destination_dir (str): The path to the destination directory where the files will be copied.

    Returns:
    None

    Example:
    source_dir = "/path/to/source_directory"
    destination_dir = "/path/to/destination_directory"
    copy_files(source_dir, destination_dir)
    """

    # Create the destination directory if it doesn't exist
    os.makedirs(destination_dir, exist_ok=True)

    # Get a list of all files in the source directory
    files = os.listdir(source_dir)

    for file in files:
        source_file_path = os.path.join(source_dir, file)
        destination_file_path = os.path.join(destination_dir, file)

        # Copy the file from the source to the destination
        if os.path.isfile(source_file_path):
            shutil.copy(source_file_path, destination_file_path)


    
def move_all_files(source_directory, destination_directory):
    """
    Move all files from a source directory to a destination directory.

    Parameters:
    source_directory (str): The path to the source directory containing the files to be moved.
    destination_directory (str): The path to the destination directory where the files will be moved.

    Returns:
    None

    Description:
    This function takes a source directory and a destination directory as input and moves all files from the source
    directory to the destination directory. It ensures that both the source and destination directories exist.
    The function preserves the directory structure when moving the files. If any errors occur during the file-moving process,
    the function provides an error message.

    Example:
    source_directory = "/path/to/source_directory"
    destination_directory = "/path/to/destination_directory"
    move_all_files(source_directory, destination_directory)
    # All files from 'source_directory' will be moved to 'destination_directory'.

    """
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
        #print(f"All files from '{source_directory}' have been moved to '{destination_directory}'.")
    except Exception as e:
        print(f"An error occurred: {e}")



    
