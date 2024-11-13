import os
import configparser


# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Navigate up one directory
parent_dir = os.path.dirname(current_dir)
# Specify the relative path to the "Databases" directory
databases_dir = os.path.join(parent_dir, "databases1")



database_path = os.path.join(databases_dir, "flight_flow.db")
config_path = os.path.join(databases_dir, "config.ini")

config = configparser.ConfigParser()
config.add_section("databases1")
config.set("databases1", "Name", "flight_flow.db")

with open(config_path, "w") as config_file:
    config.write(config_file)