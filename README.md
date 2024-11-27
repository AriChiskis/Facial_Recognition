# Facial Recognition System

## Introduction

This project develops a dynamic, automated program designed to facilitate the collection and analysis of media from various social platforms, such as Telegram and TikTok. It integrates cutting-edge technologies and programming languages to detect and categorize individuals based on facial recognition.

### Core Functionality

The system automates the process of downloading media files from specified social platforms. Utilizing advanced algorithms alongside OpenCV, the program identifies faces within these media files. Each newly identified individual's data is stored in a unique folder created by the system, which includes detailed documentation of the recognized data. For individuals previously recognized, the system updates their existing data folder with new information, ensuring all records are comprehensive and up-to-date.

### Technologies Used

#### Python
Python is the primary programming language for this project, selected for its flexibility and robust support in data manipulation and machine learning.

#### DeepFace
We employ the DeepFace library for deep learning-based face recognition, enhancing our application's ability to perform complex facial recognition tasks efficiently.

#### Amazon AWS Services
Our system utilizes several AWS services to boost its performance:
- **AWS S3**: For secure and scalable storage of media files and accompanying documentation.
- **DynamoDB**: Optionally used for efficient management of structured data across distributed servers.
- **AWS Facial Recognition Services**: These services are critical for providing precise facial analysis and recognition capabilities.

#### Telethon
The Telethon library plays a crucial role in enabling our program to interact seamlessly with Telegram, facilitating the access and download of media from various Telegram sources.

## Conclusion

This Facial Recognition System is engineered not just as a technological tool, but as a reliable resource aimed at improving safety and information accessibility, whether for identifying missing persons or for cataloging attendees at an event. It stands as a testament to the powerful synergy between technology and practical application.
