import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import ffmpeg
import create_tags, db_fns
from create_tags import make_overall_tag, make_tt_dict#, db_fns
from db_fns import connect_to_db, create_table, add_to_table, fetch_from_table
from upload_gc import upload_to_gc
import json

app = Flask(__name__)
CORS(app)

def convert_mp4_to_wav(input_file, output_file):
    try:
        # Convert MP4 to WAV using ffmpeg-python
        ffmpeg.input(input_file).output(output_file, acodec='pcm_s16le', ac=1, ar='44100', **{'y': None}).run()
        print(f"Conversion successful. Output file: {output_file}")
    except ffmpeg.Error as e:
        print(f"An error occurred: {e.stderr.decode()}")

# members API
@app.route("/receive", methods=['post'])
def form():
    # files = request.files
    # file = files.get('somethingelse')
    # print(file.content_length)

    data = request.get_data()

    print("request.get_data()")

    # return {}

    with open(os.path.abspath(f'./audios/test.mp4'), 'wb') as f:
        f.write(data)
        
        convert_mp4_to_wav("./audios/test.mp4", "./audios/output.wav")


    # -----------------------------------------------------
    cohere_and_store()
    video_data = fetch_from_table()[3:5]
    
    data_ext_result = {
        'data' : [video_data[0][0], video_data[1][0]]
    }
    
    print("DATAEXTR")
    print(data_ext_result)


    json_string = json.dumps(data_ext_result)
    print("JSONSTR")
    print(json_string)

    return jsonify(data_ext_result), 201

    # response = jsonify("File received and saved!")
    # response.headers.add('Access-Control-Allow-Origin', '*')

    # return response


# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return 'No file part', 400
#     file = request.files['file']
#     # Process the file as needed, for example, save it to a directory

#     file.save('./audios/output.wav')
#     return 'File uploaded successfully', 200


def cohere_and_store():
    SOURCE_FILE_PATH = "./audios/output.wav"
    DESTINATION_BLOB_NAME = "./audios/output.wav"

    upload_to_gc(SOURCE_FILE_PATH, DESTINATION_BLOB_NAME)
    tt_dict = make_tt_dict()
    tag = make_overall_tag()
    video_id = "00000001"

    print(tt_dict)
    print("\n\n\n\n")
    print(tag)

    # database
    connect_to_db()
    create_table()
    add_to_table(video_id, "lindsay.xie", tag, tt_dict)


if __name__ == "__main__":
    app.run(debug=True)

    
    

# connect_to_db()
# create_table()
# add_to_table(video_id, link, tag, ttt_dict)