import os
import shutil
from deepface import DeepFace
import cv2
from vid2img import extract_images_from_mp4
from search_faces import find_users_from_image




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



def crop_and_save_image(image_path, facial_area, face_number, destination_folder, margin=20):
    # Load the image
    image = cv2.imread(image_path)

    # Extract the coordinates
    x, y, w, h = facial_area['x'], facial_area['y'], facial_area['w'], facial_area['h']

    # Expand the cropping region by the margin
    x -= margin
    y -= margin
    w += 2 * margin
    h += 2 * margin

    # Ensure that the new coordinates stay within image boundaries
    x = max(0, x)
    y = max(0, y)
    w = min(w, image.shape[1] - x)
    h = min(h, image.shape[0] - y)

    # Crop the image
    cropped_image = image[y:y+h, x:x+w]

    # Get the filename from the original image path
    original_filename = os.path.basename(image_path)

    # Construct the new filename with the face number
    new_filename = f"{os.path.splitext(original_filename)[0]}_face_{face_number}.jpg"

    # Create the full path for the new image
    new_image_path = os.path.join(destination_folder, new_filename)

    # Save the cropped image to the destination folder
    cv2.imwrite(new_image_path, cropped_image)
    

    return new_image_path



def get_faces(image_path,destination_dir):
    all_faces = DeepFace.extract_faces(img_path= image_path,enforce_detection=False,detector_backend= 'retinaface')
    num_of_faces = len(all_faces)
    if num_of_faces == 0:
        print("no face_detected\n")
        return
    
    
    
    for face_number, face in enumerate(all_faces):
        facial_area = face['facial_area']
        crop_and_save_image(image_path = image_path, facial_area= facial_area, face_number = face_number,
                             destination_folder =destination_dir , margin=20)


def process_images_in_folder(source_dir,destination_dir):
    # List all files in the folder
    files = os.listdir(source_dir)


    # Define a list of image file extensions to filter for
    image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]

    # Process each file in the folder
    for file in files:
        file_extension = os.path.splitext(file)[1].lower()

        # Check if the file has a valid image extension
        if file_extension in image_extensions:
            # Construct the full path of the image file
            image_path = os.path.join(source_dir, file)

            # Call your get_faces function on the image
            get_faces_result = get_faces(image_path,destination_dir)  # Replace with your actual function

            # Process the result as needed


def identify_people_from_new_photos_or_videos(collectionId,sending_ready_faces_folder,database_path,new_photos_folder,creating_faces_folder,video=None):
    if video != None:
        extract_images_from_mp4(video_file=video,output_folder=new_photos_folder)
    photos = os.listdir(new_photos_folder)
    for photo in photos:
        photo_path = os.path.join(new_photos_folder,photo)

        get_faces(image_path=photo_path,destination_dir=creating_faces_folder)

        find_users_from_image(data_base_path=database_path,image_path=photo_path,
                             image_faces_folder=creating_faces_folder,collectionId=collectionId)

        move_all_files(source_directory=creating_faces_folder,destination_directory=sending_ready_faces_folder)
    

                
 
 

if __name__ == "__main__":

    collectionId = ''
    database = r''
    video = r''
    new_photos = r''
    new_faces = r''
    faces = r''

    identify_people_from_new_photos_or_videos(collectionId=collectionId,sending_ready_faces_folder=faces,database_path=database,new_photos_folder=new_photos,creating_faces_folder=new_faces,video=video)
    


