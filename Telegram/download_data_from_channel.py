import pandas as pd
import os
from tqdm import tqdm

def create_channel_directory(path, channel_name):
    """
    Create a directory structure for a channel, including subdirectories for different types of content
    and a 'new' directory with subdirectories for new content.

    Parameters:
    path (str): The base path where the channel directory will be created.
    channel_name (str): The name of the channel directory to be created.

    Returns:
    None

    Directory Structure:
    - channel_name
      - files
      - photos
      - videos
      - text
      - music
      - unknown
      - faces
      - photos_from_videos
      - total_files.txt (Contains the integer 0)
      - new
        - new_photos
        - new_videos
        - new_text
        - new_music
        - new_unknown
        - new_faces
        - new_photos_from_videos

    Example:
    path = "/your/desired/path"
    channel_name = "my_channel"
    create_channel_directory(path, channel_name)
    """

    # Create the main channel directory
    channel_directory = os.path.join(path, channel_name)
    os.makedirs(channel_directory)

    # Create subdirectories: files, photos, videos, text, music, unknown, faces
    subdirectories = ["files", "photos", "videos", "text", "music", "unknown", "faces","photos_from_videos"]
    for subdir in subdirectories:
        subdir_path = os.path.join(channel_directory, subdir)
        os.makedirs(subdir_path)

    # Create the 'total_files.txt' file with the integer 0
    total_files_file = os.path.join(channel_directory, "total_files.txt")
    with open(total_files_file, "w") as file:
        file.write("0")

    # Create a 'new' directory and subdirectories inside it
    new_directory = os.path.join(channel_directory, "new")
    os.makedirs(new_directory)
    new_subdirectories = ["new_photos", "new_videos", "new_text", "new_music", "new_faces","new_unknown","new_photos_from_videos"]
    for subdir in new_subdirectories:
        subdir_path = os.path.join(new_directory, subdir)
        os.makedirs(subdir_path)







'''this function will tell how many files we have in total'''
def update_integer_in_file(new_integer,channel_name,PATH_DIR,filename='total_files.txt'):

    """
    Update an integer value in a text file.

    Parameters:
    new_integer (int): The integer value to be added to the current value.
    channel_name (str): The name of the channel directory.
    PATH_DIR (str): The base path where the channel directory is located.
    filename (str): The name of the text file to update (default is 'total_files.txt').

    Returns:
    int: The updated integer value.

    Example:
    new_integer = 5
    channel_name = "my_channel"
    PATH_DIR = "/your/desired/path"
    updated_value = update_integer_in_file(new_integer, channel_name, PATH_DIR)
    """
        
    filename = os.path.join((os.path.join(PATH_DIR,  channel_name)),"total_files.txt")
    try:
        with open(filename, 'r') as file:
            current_integer = int(file.read())
    except (FileNotFoundError, ValueError):
        # Handle cases where the file doesn't exist or doesn't contain a valid integer
        print(f"Could not read a valid integer from {filename}")
        return

    # Perform the desired operation (e.g., add a new_integer)
    updated_integer = current_integer + new_integer

    try:
        with open(filename, 'w') as file:
            file.write(str(updated_integer))
        print(f"Updated integer in {filename} to {updated_integer}")
    except IOError:
        print(f"Error writing to {filename}")

    return updated_integer

'''this function creates a list with counted duplicates'''
def add_copy_order(strings,):

    """
    Create a list with counted duplicates for strings.

    Parameters:
    strings (list): A list of strings.

    Returns:
    list: A list of strings with copy orderings.

    Example:
    strings = ["apple", "banana", "apple", "cherry"]
    result = add_copy_order(strings)
    # Resulting list: ['apple', 'banana', 'apple(2)', 'cherry']
    """

    counts = {}  # Dictionary to store the counts of each string
    result = []  # List to store the strings with copy orderings

    for s in strings:
        if s in counts:
            counts[s] += 1
            s_copy = f"{s}({counts[s]})"
            result.append(s_copy)
        else:
            counts[s] = 1
            result.append(s)
    return result

'''here we rename the files that we download according to the date that they were sent
because you can not put : int file name we will change : to _ '''
def switch_chars(input_string,char_map = {':': '_'}):
    """
    Replace characters in a string based on a character map.

    Parameters:
    input_string (str): The input string to process.
    char_map (dict): A dictionary mapping characters to their replacements (default is {':': '_'}).

    Returns:
    str: The modified string.

    Example:
    input_string = "file:example.txt"
    result = switch_chars(input_string)
    # Resulting string: "file_example.txt"
    """

    # Define a dictionary to map characters to their replacements

    # Initialize an empty result string
    result = ""

    # Iterate through the characters in the input string
    for char in input_string:
        # If the character is in the char_map, add its replacement to the result
        if char in char_map:
            result += char_map[char]
        else:
            # Otherwise, add the original character to the result
            result += char
    return result


'''given a file_name, this function creates a text_file, that will be saved in the PATH DIR of the channel
normally each channel will have its own directory of files. this txt file normally will contain the dates of the 
dates of the downloaded fies.'''
def create_text_date_file(PATH_DIR,file_name):

    """
    Create a text file for storing dates of messages in a channel.

    Parameters:
    PATH_DIR (str): The base path where the channel directory is located.
    file_name (str): The name of the text file to create.

    Returns:
    file: A file object for writing dates.

    Example:
    file = create_text_date_file(PATH_DIR, "my_channel")
    # Creates a text file for storing dates in 'my_channel'.
    """

    path = os.path.join(PATH_DIR, file_name + ".txt")
    file = open(path,"w")  # opening date traffiking text
    return file


'''this function will open the text file  given an input file_name
that will be opened in the PATH DIR of the channel
normally each channel will have its own directory of files. this txt file normally will contain the dates of the 
dates of the downloaded fies.'''

def open_text_file(PATH_DIR,file_name):
    """
    Open an existing text file for reading and writing.

    Parameters:
    PATH_DIR (str): The base path where the channel directory is located.
    file_name (str): The name of the text file to open.

    Returns:
    file: A file object for reading and writing dates.

    Example:
    file = open_text_file(PATH_DIR, "my_channel")
    # Opens an existing text file for 'my_channel'.
    """

    path = os.path.join(PATH_DIR, file_name + ".txt")
    file = open(path, "r+")  # opening date traffiking text
    return file


'''this function will read the text file  given an input file_name
that will be opened in the PATH DIR of the channel
normally each channel will have its own directory of files. this txt file normally will contain the dates of the 
dates of the downloaded fies.'''
def read_from_file(PATH_DIR,file_name):
    """
    Read and open a text file for reading.

    Parameters:
    PATH_DIR (str): The base path where the channel directory is located.
    file_name (str): The name of the text file to open.

    Returns:
    file: A file object for reading dates.

    Example:
    file = read_from_file(PATH_DIR, "my_channel")
    # Opens an existing text file for reading in 'my_channel'.
    """

    path = os.path.join(PATH_DIR, file_name + ".txt")
    file = open(path, "r")  # opening date-traffciking text
    return file

''' this function will take an input a date (type datetime) and a file that will contain all the dates of messages
 that were created in the channel , and it will write the date that the message was created to the file'''
def wrtie_date(date,file):
    """
    Write a date to a text file.

    Parameters:
    date (str): The date to be written to the file.
    file (file): The file object for writing dates.

    Returns:
    None

    Example:
    date = "2023-10-16 12:00:00"
    file = open_text_file(PATH_DIR, "my_channel")
    write_date(date, file)
    # Writes the date to the text file.
    """

    file.write(str(date) + "\n")

def check_if_dates_exists(min_date,curr_date):

    """
    Check if a current date is greater than a minimum date.

    Parameters:
    min_date (datetime): The minimum date to compare.
    curr_date (datetime): The current date to compare.

    Returns:
    bool: True if the current date is greater, False otherwise.

    Example:
    min_date = datetime(2023, 10, 15, 0, 0, 0)
    curr_date = datetime(2023, 10, 16, 12, 0, 0)
    result = check_if_dates_exist(min_date, curr_date)
    # Returns True.
    """

    return min_date < curr_date

'''this function converts a column of a dataframe to a list'''
def convert_column_to_list(df,column='date'):

    # """
    # Convert a column of a DataFrame to a list.

    # Parameters:
    # df (DataFrame): The DataFrame containing the column.
    # column (str): The name of the column to convert (default is 'date').

    # Returns:
    # list: A list of values from the specified column.

    # Example:
    # df = pd.DataFrame({"date": ["2023-10-16", "2023-10-17", "2023-10-18"]})
    # result = convert_column_to_list(df)
    # # Returns: ["2023-10-16", "2023-10-17", "2023-10-18"]
    # """

    return df[column].tolist()

'''this function will sort files by creating by creating order that they were created 
the default that it will be DESCENDING how ever you could change it to ACENDING'''
def sort_files_by_order(dir_path,DESCENDING=True):

    """
    Sort files in a directory based on their order.

    Parameters:
    dir_path (str): The path of the directory to sort files.
    DESCENDING (bool): Whether to sort in descending order (default is True).

    Returns:
    list: A list of sorted file paths.

    Example:
    dir_path = "/path/to/files"
    files = sort_files_by_order(dir_path)
    # Returns a list of file paths sorted by order.
    """

    os.chdir(dir_path)
    files = filter(os.path.isfile, os.listdir(dir_path))
    files = [os.path.join(dir_path, f) for f in files]  # add path to each file
    files.sort(key=lambda x: os.path.getmtime(x))

    if DESCENDING:
        files.sort(reverse=True)
    return files



'''this function will rename the files. the name of each new file will the date that it was sent
moreover, we will sort the files of the directory by descending order that they were downloaded
the function returns the total files that are in the directory'''
def rename_files(FILES_PATH,frame, num_of_old_files,channel_name):
    """
    Rename files in a directory based on dates and the order in which they were created.

    Parameters:
    FILES_PATH (str): The path of the directory containing the files.
    frame (DataFrame): A DataFrame containing date information for files.
    num_of_old_files (int): The number of old files before renaming.
    channel_name (str): The name of the channel directory.

    Returns:
    int: The total number of files after renaming.

    Example:
    num_of_old_files = 10
    frame = pd.DataFrame({"date": ["2023-10-16", "2023-10-17", "2023-10-18"]})
    channel_name = "my_channel"
    result = rename_files(FILES_PATH, frame, num_of_old_files, channel_name)
    # Renames and returns the total number of files after renaming.
    """

    dates = convert_column_to_list(frame)
    files = sort_files_by_order(FILES_PATH)
    num_new_files = len(files) - num_of_old_files

    dates = add_copy_order(dates)

    # Iterate through the files and move each one to the destination directory
    for i in range(num_new_files): #we are going to rename only the new files that we have added to the directory
        after_suffix = switch_chars(dates[i][0:-1] + "." + files[i].lower().split('.')[-1])
        os.rename(files[i], FILES_PATH + "\\" + channel_name  + "_" +  after_suffix) #rename the files
    return len(files)

'''this funciton will create to new dates dataframe'''
def save_new_date_datafrmae(num_of_files,frame,channel_name,PATH_DIR,column='date'):

    """
    Save a new DataFrame containing date information for files.

    Parameters:
    num_of_files (int): The total number of files.
    frame (DataFrame): A DataFrame containing date information.
    channel_name (str): The name of the channel directory.
    PATH_DIR (str): The base path where the channel directory is located.
    column (str): The name of the column containing dates (default is 'date').

    Returns:
    None

    Example:
    num_of_files = 20
    frame = pd.DataFrame({"date": ["2023-10-16", "2023-10-17", "2023-10-18"]})
    channel_name = "my_channel"
    PATH_DIR = "/your/desired/path"
    save_new_date_dataframe(num_of_files, frame, channel_name, PATH_DIR)
    # Saves the new date DataFrame.
    """
        
    frame = frame[column][0:num_of_files]
    '''convert the dataframe to a .txt file'''
    path = os.path.join(os.path.join(PATH_DIR,channel_name),channel_name + ".txt")
    frame.to_csv(path)



'''this function checks if a certain file exists
    this is for text file'''
def file_exists(file_name,PATH_DIR):
    
    """
    Check if a text file exists in a specified directory.

    Parameters:
    file_name (str): The name of the text file to check.
    PATH_DIR (str): The base path where the channel directory is located.

    Returns:
    bool: True if the file exists, False otherwise.

    Example:
    file_name = "my_channel"
    PATH_DIR = "/your/desired/path"
    result = file_exists(file_name, PATH_DIR)
    # Returns True if the file exists.
    """



    
    path = os.path.join(os.path.join(PATH_DIR, file_name),file_name + ".txt")
    #print(path)
    return os.path.isfile(path)

'''this function removes a file given its path '''
def remove_file(file_path):

    """
    Remove a file at the specified path.

    Parameters:
    file_path (str): The path of the file to be removed.

    Returns:
    None

    Example:
    file_path = "/path/to/file.txt"
    remove_file(file_path)
    # Removes the file at the specified path.
    """
    os.remove(file_path)

'''this function creates from a text file that containts dates (the dates are the dates of the messages that
 were sent from the channel) and converts it to a dataframe. the dates are written in descending order
  meaning the first line is the latest date and so in and on....
  the dataframe has only 1 collumn by the name "date" and it will store the dates of the messages'''
def create_pd_df_from_text(path,channel):
    
    """
    Create a DataFrame from a text file containing dates of messages.

    Parameters:
    path (str): The path of the text file.
    channel (str): The name of the channel directory.

    Returns:
    DataFrame: A DataFrame containing dates.

    Example:
    path = "/path/to/file.txt"
    channel = "my_channel"
    df = create_pd_df_from_text(path, channel)
    # Creates a DataFrame from the text file.
    """

    df_path = os.path.join(os.path.join(path,channel),channel + ".txt")
    in_storage = pd.read_csv(df_path)
    return in_storage

'''this function returns to us how many files we have in each directory'''
def num_of_files_in_directory(dir_path):
    
    """
    Get the number of files in a directory.

    Parameters:
    dir_path (str): The path of the directory to count files.

    Returns:
    int: The number of files in the directory.

    Example:
    dir_path = "/path/to/directory"
    result = num_of_files_in_directory(dir_path)
    # Returns the number of files in the directory.
    """
    
    return len(os.listdir(dir_path))

'''this function will create a new dataframe with the date of the new messaages, it has a parameter LIMIT
(20 is defualt) , and it will take the dates of the last LIMIT messages of the channel
we will use it for identifying if we have took too many or too less files before the most updated file that 
 we have downloaded to avoid duplicates'''
def create_dataframe_of_new_messages(messages,LIMIT=40):
       
    """
    Create a DataFrame with date information for new messages in a channel.

    Parameters:
    messages: A list of messages.
    LIMIT (int): The limit of messages to consider (default is 20).

    Returns:
    DataFrame: A DataFrame containing date information.

    Example:
    messages = [...]
    LIMIT = 30
    df = create_dataframe_of_new_messages(messages, LIMIT)
    # Creates a DataFrame with date information for new messages.
    """
       
    return pd.DataFrame({"date": [str(messages[i].date) for i in range(LIMIT)]})  # new storage dframe


'''this file returns the head of a column of a dataframe'''
def get_head_of_column_df(df,column='date'):
    return df[column][0]

'''this fucntion will the number of messages that it has given to download'''
def download_files(messages,num_of_files,FILES_PATH):
    sliced_messages = [message for message in messages[0:num_of_files]  if (message.media != None)] #taking only media
    for msg in tqdm(sliced_messages): 
        msg.download_media(file=FILES_PATH)

'''returns how many column there is in '''
def column_size(df,column='date'):
    return len(df[column])

'''we will download all the media in this function, it will take the last LIMIT messages that were sended by
the channel and it will download the the last files'''
def download_media(channel_name,group, cl,PATH_DIR,FILES_PATH,LIMIT=2):
    num_of_files_before = num_of_files_in_directory(FILES_PATH)
    if_file_exists = file_exists(channel_name,PATH_DIR=PATH_DIR)

    messages = cl.get_messages(group, limit=LIMIT)

    if if_file_exists:
        old_dates = create_pd_df_from_text(PATH_DIR,channel_name)
        possible_new_dates = create_dataframe_of_new_messages(messages,LIMIT=2)
        old_head = get_head_of_column_df(old_dates)

        new_dates = possible_new_dates[possible_new_dates['date'] > old_head] #classifying duplicated dates
        if new_dates['date'].empty == False:

            final_dates = pd.concat([new_dates, old_dates]).reset_index(drop=True)
            remove_file(os.path.join(PATH_DIR,  channel_name) +  ".txt")
            



        else:
            final_dates = old_dates

    else:
        # this will happened when the date file of the channel does not exists
        possible_new_dates = create_dataframe_of_new_messages(messages,LIMIT=2)
        new_dates = possible_new_dates
        final_dates = new_dates

    download_files(messages,len(new_dates),FILES_PATH=FILES_PATH) #we download only the new messages/files to avoid duplictes
    num_of_files_added = rename_files(FILES_PATH,new_dates,num_of_files_before,channel_name=channel_name)
    total_files = update_integer_in_file(num_of_files_added,channel_name=channel_name,PATH_DIR=PATH_DIR)
    save_new_date_datafrmae(total_files,final_dates,channel_name=channel_name,PATH_DIR=PATH_DIR)

    return num_of_files_added




 


