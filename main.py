from flask import Flask, request
from mutagen.mp3 import MP3
import numpy as np
import datetime, pymongo
import json

app = Flask(__name__)

def file_duration(audio_file):
    audio_file = MP3(audio_file)
    song_info = audio_file.info
    return np.ceil(song_info.length)

# Connect to MongoDB and create database
db_connect_url = "mongodb://localhost:27017/"
mongo_connector = pymongo.MongoClient(host=db_connect_url)
db_names = mongo_connector.list_database_names()

#if "audio_server_db" not in db_names:
database = mongo_connector["audio_server_db"]
collection = database["audio_collection"]

@app.route('/Create', methods=['POST', 'GET'])
def CREATE():
    if request.method == 'POST':
        file_ = request.files['file']
        file_name = file_.filename
        duration = file_duration(file_)
        upload_time = datetime.datetime.now()
        id_ = request.form['ID']
        if request.form['audioFileType'] == 'Song':
            record ={"ID": id_, "audioFileMetadata": {"Name of the song": file_name, "Duration in number of seconds": duration, "Uploaded time": upload_time},
                     "audioFileType": "Song"}
            collection.insert_one(record)
            return {"Message": "Song added successfully to collection"}

        elif request.form['audioFileType'] == 'Podcast':
            Host_name = request.form['HOST']

            record ={"ID": id_, "audioFileMetadata": {"Name of the Podcast": file_name, "Duration in number of seconds": duration, "Uploaded time": upload_time,
                                           "HOST": Host_name}, "audioFileType": "Podcast"}
            collection.insert_one(record)

            return {"Message": "Podcast added successfully to collection"}

        elif request.form['audioFileType'] == 'Audio book':
            title_author = request.form['author of title']
            narrator = request.form['narrator']
            record ={"ID": id_, "audioFileMetadata": {"Title of the audiobook": file_name, "Author of the title ": title_author, "Narrator": narrator,
                                           "Duration in number of seconds": duration, "Uploaded time": upload_time},
                     "audioFileType": "Audio book"}
            collection.insert_one(record)
            return {"Message": "Audio book added successfully to collection"}

        else:
            return {"Message": "No record added"}

@app.route('/Delete', methods = ['POST', 'GET'])
def delete():
    if request.method == 'POST':
        request_id = request.form['audioFileID']
        audio_file_type = request.form['audioFileType']
        query_to_delete = {"ID": request_id, "audioFileType": audio_file_type}
        collection.delete_one(query_to_delete)
        return {"Message": "Audio file deleted successfully from collection"}

@app.route('/update', methods = ['POST', 'GET'])
def update():

    if request.method == 'POST':
        file_ = request.files['file']
        file_name = file_.filename
        duration = file_duration(file_)
        upload_time = datetime.datetime.now()
        id_ = request.form['ID']
        if request.form['audioFileType'] == 'Song':

            collection.update_one({"ID": id_}, {"$set": {"audioFileMetadata": {"Name of the song": file_name, "Duration in number of seconds": duration,
                                                                               "Uploaded time": upload_time}}})
            return {"Message": "Song updated successfully"}

        elif request.form['audioFileType'] == 'Podcast':
            Host_name = request.form['HOST']

            collection.update_one({"ID": id_}, {"$set": {"audioFileMetadata": {"Name of the Podcast": file_name, "Duration in number of seconds": duration, "Uploaded time": upload_time,
                                           "HOST": Host_name}}})

            return {"Message": "Podcast updated successfully"}

        elif request.form['audioFileType'] == 'Audio book':
            title_author = request.form['author of title']
            narrator = request.form['narrator']

            collection.update_one({"ID": id_}, {"$set": {"audioFileMetadata": {"Title of the audiobook": file_name, "Author of the title ": title_author, "Narrator": narrator,
                                           "Duration in number of seconds": duration, "Uploaded time": upload_time}}})

            return {"Message": "Audio book updated successfully"}

        else:
            return {"Message": "No record Updated"}


@app.route('/get', methods = ['POST', 'GET'])
def GET():
    if request.method =='POST':
        id = request.form['audioFileID']
        audio_file_type = request.form['audioFileType']
        lis = []
        if id == 'NA':
            result = collection.find({"audioFileType": audio_file_type})
            for i in result:
                lis.append(str(i))
            return {"Message": lis}
        else:
            result = collection.find({"audioFileType": audio_file_type, "ID": id})
            for i in result:
                lis.append(str(i))
            return {"Message": lis}
        # result = collection.find({"audioFileType": audio_file_type, "ID": id})
        # for k in result:
        #     lis.append(str(k))
        #     print(k)
        # return {"Message": lis}


if __name__ == "__main__":
    app.run(debug=True)