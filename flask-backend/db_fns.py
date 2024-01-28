import psycopg2

# connect to database
def connect_to_db():
    conn = psycopg2.connect(
        database="test2_db", user='postgres', password='12345678', host='localhost', port= '5432'
    )

    cursor = conn.cursor()

    cursor.execute("select version()")

    data = cursor.fetchone()
    print("Connection established to: ",data)

    conn.close()

def create_table():
    conn = psycopg2.connect(
        database="test2_db", user='postgres', password='12345678', host='127.0.0.1', port= '5432'
    )
    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    #Doping videos table if already exists.
    cursor.execute("DROP TABLE IF EXISTS VIDEO_LIBRARY;")

    #Creating table as per requirement
    sql ='''CREATE TABLE VIDEO_LIBRARY(
    VIDEO_ID VARCHAR(500) NOT NULL,
    Link VARCHAR(500) NOT NULL,
    Tag VARCHAR (200) NOT NULL,
    TT_Times integer[] NOT NULL,
    TT_Tags text[] NOT NULL,
    Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )'''
    cursor.execute(sql)
    print("Table created successfully........")
    conn.commit()
    #Closing the connection
    conn.close()


def add_to_table(video_id, link, tag, ttt_dict):
    #Establishing the connection
    conn = psycopg2.connect(
    database="test2_db", user='postgres', password='12345678', host='localhost', port= '5432'
    )
    #Setting auto commit false
    conn.autocommit = True

    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    tt_times = []
    tt_tags = []

    for i in ttt_dict.keys():
        tt_times.append(i)
        tt_tags.append(ttt_dict[i])

    postgres_insert_query = """ INSERT INTO VIDEO_LIBRARY (VIDEO_ID, Link, Tag, TT_Times, TT_Tags) VALUES (%s,%s,%s,%s,%s)"""
    record_to_insert = (video_id, link, tag, tt_times, tt_tags)
    cursor.execute(postgres_insert_query, record_to_insert)

    # Commit your changes in the database
    conn.commit()
    print("Records inserted........")

    # Closing the connection
    conn.close()


# demo

video_id = "00000001"
link = "lindsay.xie"
tag = "happy"
ttt_dict = {
    5648: "bedge",
    12359: "happyge",
    15623: "sadge",
    32472: "bedge",
    46829: "cryge"
}

connect_to_db()
create_table()
add_to_table(video_id, link, tag, ttt_dict)