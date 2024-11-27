import os
import imageio

def extract_images_from_mp4(video_file, output_folder):
    """
    Extract frames from an MP4 video and save them as images in a folder.

    Parameters:
    video_file (str): The input MP4 video file.
    output_folder (str): The folder where the extracted images will be saved.

    Returns:
    None
    """
    try:
        # Create the output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Open the video file using imageio
        vid = imageio.get_reader(video_file, 'ffmpeg')
        j = 0
        for i, frame in enumerate(vid):
            if i % 20 == 0:
                video_name = os.path.basename(video_file).split(".")[0]
                image_filename = 'video' + video_name + f"{j:04d}.png"  # You can use other image formats like jpg
                image_path = os.path.join(output_folder, image_filename)
                imageio.imwrite(image_path, frame)
                j = j+1

        print(f"Extracted {j + 1} frames to {output_folder}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:


def extract_images_from_mp4_all_videos_in_folder(input_folder, output_folder):
    files = os.listdir(input_folder)
    for file in files:
        file_full_path = os.path.join(input_folder,file)
        extract_images_from_mp4(file_full_path,output_folder)

