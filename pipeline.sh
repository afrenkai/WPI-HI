#!/bin/bash
pip install -r requirements.txt
python3 get_data_locally.py
python3 normalize_csv.py
python3 create_ds.py
