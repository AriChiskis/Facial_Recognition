import os
import sys
import shutil
import io
import boto3
from PIL import Image

    
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




def get_user_information(collection_id, face_id):
    session = boto3.Session(profile_name='default')
    client = session.client('rekognition')
    response = client.list_faces(CollectionId=collection_id)
    # Iterate through the faces to find the one with the matching FaceId
    for face in response['Faces']:
        if face['FaceId'] == face_id:
            if 'UserId' in face:
                return face['UserId']
            else:
                return 'Unowkn -yet'



def search_face(client,image_binary,collectionId):

    '''response search_faces_by_iamge syntax'''

    """
    {
    'SearchedFaceBoundingBox': {
        'Width': ...,
        'Height': ...,
        'Left': ...,
        'Top': ...
    },
    'SearchedFaceConfidence': ...,
    'FaceMatches': [
        {
            'Similarity': ...,
            'Face': {
                'FaceId': 'string',
                'BoundingBox': {
                    'Width': ...,
                    'Height': ...,
                    'Left': ...,
                    'Top': ...
                },
                'ImageId': 'string',
                'ExternalImageId': 'string',
                'Confidence': ...,
                'IndexFacesModelVersion': 'string',
                'UserId': 'string'
            }
        },
    ],
    'FaceModelVersion': 'string'
    }

    """

    try:
        response = client.search_faces_by_image(
            CollectionId=collectionId,
            Image={'Bytes': image_binary}
        )

        faceMatches = response['FaceMatches']
        return faceMatches
    except Exception as e:

        #print("not matches found returing an empty list")
        return []     #returns an empty list



def identify_all_user_ids_from_faceMatches(collectionId,faceMatches):

    """
    Extract and collect user IDs from a list of face match results.

    Parameters:
    - faceMatches (list of dict): A list of dictionaries containing face match results. Each dictionary should include a 'User_ids' key
      representing the user ID associated with the recognized face.

    Returns:
    - User_ids (set): A set containing unique user IDs extracted from the 'faceMatches' list.

    Description:
    This function iterates through a list of face match results and attempts to extract user IDs associated with recognized faces.
    The 'faceMatches' parameter should be a list of dictionaries, each of which should contain a 'User_ids' key.

    The function collects the unique user IDs into a set and returns the set containing these user IDs.

    If any errors occur during the extraction process, they are caught, and the function continues processing the remaining entries.

    Example:
     faceMatches = [
         {'User_ids': 'user1', 'confidence': 0.95},
         {'User_ids': 'user2', 'confidence': 0.92},
         {'confidence': 0.89},  # This entry does not have a 'User_ids' key
     ]
     user_ids = identify_all_user_ids_from_faceMatches(faceMatches)
     print(user_ids)
    Output: {'user1', 'user2'}

    Notes:
    - The function iterates over the 'faceMatches' list, attempting to extract user IDs from each dictionary.
    - If a dictionary in 'faceMatches' does not contain a 'User_ids' key, it is skipped, and the function continues to the next entry.
    - Any exceptions raised during the extraction process are caught and may be handled according to the specific requirements of your application.
    - The extracted user IDs are stored in a set to ensure uniqueness.

    Please make sure that the 'faceMatches' parameter contains dictionaries with a 'User_ids' key, as the function relies on this key to extract user IDs.
    Additionally, the function returns a set, ensuring that the user IDs are unique in the result set.
    """

    User_ids = set()
    for match in faceMatches: #try to add al the User_id 

        try: 
            face_id = match['Face']['FaceId']
            user_name = get_user_information(collection_id=collectionId,face_id=face_id)
            User_ids.add(user_name)

        except Exception as e:
            #print(f"An error occurred: {e}")
            #print("Let's improve ourselves for next time :(")
            continue
    #print(User_ids)
    return User_ids


def copy_image_to_directory(image_path, destination_directory):

    try:
        shutil.copy(image_path, destination_directory)
        #print(f"Image '{image_path}' copied to '{destination_directory}' successfully.")
    except FileNotFoundError:
        print(f"Image file '{image_path}' not found.")
    except IsADirectoryError:
        print(f"'{destination_directory}' is not a valid directory.")
    except PermissionError:
        print(f"You don't have permission to copy the file to '{destination_directory}'.")
    except Exception as e:
        print(f"An error occurred: {e}")


def find_users_from_image(data_base_path,image_path,image_faces_folder,collectionId):
        Users = set()
        dest_folder = ''
        client=boto3.client('rekognition')
        #image_name = os.path.basename(image_path)
        '''each image has a directory that contains all the images
          of faces that were identified in the image
        '''
        faces = os.listdir(image_faces_folder)
        

        for face in faces:
            face_path = os.path.join(image_faces_folder,face)
            image = Image.open(face_path)
            stream = io.BytesIO()
            image.save(stream,format="JPEG")
            image_binary = stream.getvalue()

            faceMatches = search_face(client = client,image_binary=image_binary,
                    collectionId=collectionId)
            User_ids = identify_all_user_ids_from_faceMatches(collectionId=collectionId,faceMatches=faceMatches)
            Users = Users.union(User_ids)
        
        ''' now we have all the users that are has been identified from the image
            and we want to upload all the images to the users database folder:
            'photos_to_inspect
        '''

        for user in Users:
            directory = os.path.join(data_base_path,user)
            copy_image_to_directory(image_path=image_path,destination_directory=directory)

        return




