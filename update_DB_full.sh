#!/bin/bash

source py3/bin/activate

python build_DB_posts.py

python add_dbPosts_avant7avril.py

python build_DB_occurences.py

python build_DB_statistics.py

python stats2json.py
