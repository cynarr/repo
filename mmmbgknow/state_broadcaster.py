import os
from os.path import join as pjoin
from .utils.csv import read_csv_map


DIR_PATH = os.path.dirname(os.path.realpath(__file__))
STATE_BROADCASTERS = read_csv_map(pjoin(DIR_PATH, "data/state_broadcasters.csv"))
