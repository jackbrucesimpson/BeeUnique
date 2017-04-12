import os
import sqlite3
from datetime import datetime
import pandas as pd

class DB:
    def __init__(self, database_file_path):
        self.conn = sqlite3.connect(database_file_path)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.row_factory = sqlite3.Row

    def create_db(self):
        c = self.conn.cursor()
        c.execute('''    CREATE TABLE IF NOT EXISTS VIDEOS
                            (VIDEO_ID               INTEGER PRIMARY KEY AUTOINCREMENT,
                            START_DATETIME          DATETIME NOT NULL);
        ''')

        c.execute('''    CREATE TABLE IF NOT EXISTS BEES
                            (BEE_ID                 INTEGER PRIMARY KEY,
                            VIDEO_ID                INTEGER UNSIGNED NOT NULL,
                            CLASS_CLASSIFIED        INTEGER UNSIGNED NOT NULL,

                            FOREIGN KEY             (VIDEO_ID)                                  REFERENCES VIDEOS(VIDEO_ID) ON DELETE CASCADE);
        ''')

        c.execute('''    CREATE TABLE IF NOT EXISTS PATHS
                            (BEE_ID                 INTEGER UNSIGNED NOT NULL,
                            X                       FLOAT NOT NULL,
                            Y                       FLOAT NOT NULL,
                            FRAME_NUM               INTEGER UNSIGNED NOT NULL,
                            CLASSIFIED              INTEGER UNSIGNED,

                            PRIMARY KEY             (BEE_ID, FRAME_NUM),
                            FOREIGN KEY             (BEE_ID)                                    REFERENCES BEES(BEE_ID) ON DELETE CASCADE);
        ''')

        c.close()

    def insert_video_info(self, video_filename):
        self.create_db()
        video_id, dt = self.get_video_id_start_datetime(video_filename)
        if video_id is not None:
            c = self.conn.cursor()
            c.execute("DELETE FROM VIDEOS WHERE START_DATETIME = '{}'".format(dt))
            c.close()
            self.conn.commit()
        c = self.conn.cursor()
        c.execute("INSERT INTO VIDEOS (START_DATETIME) VALUES ('{}')".format(dt))
        video_id = (c.lastrowid)
        c.close()
        self.conn.commit()
        return video_id

    def get_video_id_start_datetime(self, video_filename):
        dt = datetime.strptime(video_filename, "%Y-%m-%d_%H-%M-%S")
        c = self.conn.cursor()
        c.execute("SELECT VIDEO_ID FROM VIDEOS WHERE START_DATETIME='{}'".format(dt))
        query_result = c.fetchone()
        if query_result is None:
            return (None, dt)
        video_id = query_result['VIDEO_ID']
        c.close()
        return (video_id, dt)

    def get_next_bee_id(self, video_id):
        c = self.conn.cursor()
        c.execute("SELECT MAX(BEE_ID) FROM BEES")
        query_result = c.fetchone()
        if query_result['MAX(BEE_ID)'] is None:
            next_bee_id = 0
        else:
            next_bee_id = query_result['MAX(BEE_ID)'] + 1
        c.close()
        return next_bee_id

    def insert_bees_and_paths(self, bees_df, paths_df):
        bees_df.to_sql('BEES', self.conn, if_exists='append', index=False)
        paths_df.to_sql('PATHS', self.conn, if_exists='append', index=False)

    def get_bees_paths_dfs(self, video_id):
        bees_df = pd.read_sql_query("SELECT BEE_ID, CLASS_CLASSIFIED FROM BEES WHERE VIDEO_ID={}".format(video_id), self.conn)
        extract_ids_list_minus_brackets = str(list(bees_df['BEE_ID']))[1:-1]
        paths_df = pd.read_sql_query("SELECT BEE_ID, X, Y, FRAME_NUM, CLASSIFIED FROM PATHS WHERE BEE_ID IN ({})".format(extract_ids_list_minus_brackets), self.conn)
        return (bees_df, paths_df)

    def close_conn(self):
        self.conn.close()
