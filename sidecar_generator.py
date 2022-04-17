#! /usr/local/bin/python3
import os
import re
import shutil
import sys


class PrintColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class SidecarGenerator:

    def __init__(self, file_name):
        self.mhl_file_name = os.path.abspath(file_name)
        self.md5_dictionary = self.load_source_mhl()
        self.volume_name = self.get_volume_name()
        print('Volume name: ' + self.volume_name)

        self.save_txt_file()
        self.save_md5_file()
        self.copy_mhl_file()

    def load_source_mhl(self):

        with open(self.mhl_file_name, 'r') as f:
            contents = f.readlines()

        files_list = [strip_xml_tags(x) for x in contents if x.strip().startswith('<file>')]
        md5_list = [strip_xml_tags(x).lower() for x in contents if x.strip().startswith('<md5>')]

        md5_dictionary = dict(zip(files_list, md5_list))

        return md5_dictionary

    def get_volume_name(self):

        split = list(self.md5_dictionary.keys())[0].split('/')

        if split[1] == 'Volumes':

            return split[2]
        else:
            return os.path.basename(self.mhl_file_name).replace('.mhl', '')

    def save_md5_file(self):
        directory = os.path.dirname(self.mhl_file_name)

        md5_file_name = os.path.join(directory, self.volume_name + '.md5')
        print('Saving md5 file: ' + md5_file_name)

        with open(md5_file_name, 'w') as f:
            for key, value in self.md5_dictionary.items():
                f.write(value + '  ' + key + '\n')

    def save_txt_file(self):
        directory = os.path.dirname(self.mhl_file_name)

        txt_file_name = os.path.join(directory, self.volume_name + '.txt')
        print('Saving txt file: ' + txt_file_name)

        with open(txt_file_name, 'w') as f:
            for key in self.md5_dictionary.keys():
                f.write(key + '\n')

    def copy_mhl_file(self):

        directory = os.path.dirname(self.mhl_file_name)

        mhl_file_name = os.path.join(directory, self.volume_name + '.mhl')

        print('Saving mhl file: ' + mhl_file_name)
        shutil.copy(self.mhl_file_name, mhl_file_name)


def strip_xml_tags(string):
    string = string.strip()
    string = re.sub(r'<.*?>', '', string)

    return string


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print('{}Usage: python3 sidecar_generator.py <mhl_file_name>{}'.format(PrintColors.FAIL, PrintColors.ENDC))
        sys.exit(1)

    mhl_files = [os.path.abspath(x) for x in sys.argv[1:] if os.path.isfile(x) and x.endswith('.mhl')]

    if mhl_files:
        for mhl_file in mhl_files:

            print('{}Processing: {}{}'.format(PrintColors.OKBLUE, os.path.basename(mhl_file), PrintColors.ENDC))

            try:
                SidecarGenerator(mhl_file)
            except shutil.SameFileError:
                print('{}MHL file is already named the volume name{}'.format(PrintColors.WARNING, PrintColors.ENDC))
            except Exception as e:
                print('{}Error: {}{}'.format(PrintColors.FAIL, e, PrintColors.ENDC))

    else:
        print('{}No mhl files found{}'.format(PrintColors.FAIL, PrintColors.ENDC))
        sys.exit(1)
