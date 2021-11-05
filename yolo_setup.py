import os

# Get the absolute path of the file
file_dir = os.path.dirname(os.path.abspath(__file__))

base_data_path = os.path.join(file_dir, "data")

classes=1
classnames_file = os.path.join(base_data_path, "class.names")
with open(classnames_file, "w") as f:
    f.write("kidney")

train_data_file = os.path.join(base_data_path, "train.txt")
val_data_file = os.path.join(base_data_path, "val.txt")

data_config_file = os.path.join(file_dir, "config", "kidney.data")

writestring = f"""classes={classes}
train={train_data_file}
valid={val_data_file}
names={classnames_file}"""
with open(data_config_file, "w") as f:
    f.write(writestring)
    
    