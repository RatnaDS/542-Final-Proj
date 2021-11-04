import os
from data_utils.preprocessing import Preprocessor

save_dir = os.path.join("data", "preprocessed_data")
dir = "D:\\Desktop\\ECE_542\\ECE_542_Course_Project\\kits19\\data"
preprocessor = Preprocessor(dir)
preprocessor.run(save_dir)
