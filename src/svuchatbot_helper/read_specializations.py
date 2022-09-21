from os.path import join
from src.svuchatbot_helper.utils import get_project_root
import pandas as pd


def get_specializations():
    f_path = join(get_project_root(), 'assets', "Specializations_of_the_Syrian_Virtual_University.csv")
    df = pd.read_csv(f_path, names=["name0", "name1", "name2", "name3"])
    df = df.applymap(str.strip)
    return df
