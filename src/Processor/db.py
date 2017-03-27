import os
import sqlite3
from datetime import datetime

class DB:
    def __init__(self, database_file_path):
        self.conn = sqlite3.connect(database_file_path)
        self.conn.row_factory = sqlite3.Row

    def create_db(self):
        c = self.conn.cursor()
        c.execute('''    CREATE TABLE IF NOT EXISTS VIDEOS
                            (VIDEO_ID               INTEGER PRIMARY KEY AUTOINCREMENT,
                            VIDEO_NAME              TEXT NOT NULL,
                            START_DATETIME          DATETIME NOT NULL);
        ''')

        c.execute('''    CREATE TABLE IF NOT EXISTS BEES
                            (BEE_ID                 INTEGER PRIMARY KEY AUTOINCREMENT,
                            VIDEO_ID                INTEGER UNSIGNED NOT NULL,
                            CLASS_CLASSIFIED        INTEGER UNSIGNED NOT NULL,

                            FOREIGN KEY             (VIDEO_ID)                                  REFERENCES VIDEOS(VIDEO_ID));
        ''')

        c.execute('''    CREATE TABLE IF NOT EXISTS PATHS
                            (BEE_ID                 INTEGER UNSIGNED NOT NULL,
                            X                       FLOAT NOT NULL,
                            Y                       FLOAT NOT NULL,
                            FRAME_NUM               INTEGER UNSIGNED NOT NULL,

                            PRIMARY KEY             (BEE_ID, FRAME_NUM),
                            FOREIGN KEY             (BEE_ID)                                    REFERENCES BEES(BEE_ID));
        ''')

        c.execute('''    CREATE TABLE IF NOT EXISTS FRAME_CLASSIFICATIONS
                            (BEE_ID                 INTEGER UNSIGNED NOT NULL,
                            FRAME_NUM               INTEGER UNSIGNED NOT NULL,
                            CLASSIFIED              INTEGER UNSIGNED NOT NULL,

                            PRIMARY KEY             (BEE_ID, FRAME_NUM),
                            FOREIGN KEY             (BEE_ID)                                    REFERENCES BEES(BEE_ID));
        ''')

        c.close()

    def insert_video_info(self, experiment_name, video_filename):
        self.create_db()

        dt = datetime.strptime(video_filename, "%Y-%m-%d_%H-%M-%S")
        c = self.conn.cursor()
        c.execute("INSERT INTO VIDEOS (VIDEO_NAME, START_DATETIME) VALUES ('{}', '{}')".format(experiment_name, dt));
        self.video_id = (c.lastrowid)
        c.close()
        self.conn.commit()

    def insert_bee(self, class_classified):
        c = self.conn.cursor()
        c.execute("INSERT INTO BEES (VIDEO_ID, CLASS_CLASSIFIED) VALUES ({}, {})".format(self.video_id, class_classified));
        bee_id = (c.lastrowid)
        c.close()
        self.conn.commit()

        return bee_id

    def insert_path(self, bee_id, x, y, frame_num):
        c = self.conn.cursor()
        c.execute("INSERT INTO PATHS (BEE_ID, CLASS_CLASSIFIED) VALUES ({}, {}, {}, {})".format(bee_id, x, y, frame_num));
        bee_id = (c.lastrowid)
        c.close()
        self.conn.commit()

    def insert_classifications(self, bee_id, classified, frame_num):
        c = self.conn.cursor()
        c.execute("INSERT INTO FRAME_CLASSIFICATIONS (BEE_ID, CLASSIFIED, FRAME_NUM) VALUES ({}, {}, {})".format(bee_id, classified, frame_num));
        bee_id = (c.lastrowid)
        c.close()
        self.conn.commit()

    def get_video_id(self, video_filename):
        c = conn.cursor()
        c.execute("SELECT VIDEO_ID FROM VIDEOS WHERE VIDEO_NAME='{}'".format(video_filename))
        row = c.fetchone()
        video_id = row['VIDEO_ID']
        c.close()
        return video_id

    def close_conn(self):
        conn.close()
