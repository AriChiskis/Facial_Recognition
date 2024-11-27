import os
import sys
import shutil
import io
import boto3
from PIL import Image


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
        print(f"Image '{image_path}' copied to '{destination_directory}' successfully.")
    except FileNotFoundError:
        print(f"Image file '{image_path}' not found.")
    except IsADirectoryError:
        print(f"'{destination_directory}' is not a valid directory.")
    except PermissionError:
        print(f"You don't have permission to copy the file to '{destination_directory}'.")
    except Exception as e:
        print(f"An error occurred: {e}")


def find_users_from_image(data_base_path,image_path,image_faces_folder,collectionId,video=None):
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
            directory = os.path.join(os.path.join(data_base_path,user),dest_folder)
            copy_image_to_directory(image_path=image_path,destination_directory=directory)

        return




