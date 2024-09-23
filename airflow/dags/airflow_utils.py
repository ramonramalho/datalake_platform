import os
import yaml

class Utils:
    @staticmethod
    def find_yml_files(directory):
        yml_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.yml') or file.endswith('.yaml'):
                    yml_files.append(os.path.join(root, file))
        return yml_files
    
    @staticmethod
    def load_yml(directory):
        yml_files = Utils.find_yml_files(directory)
        for yml_file in yml_files:
            with open(yml_file) as f:
                yield yaml.safe_load(f)
