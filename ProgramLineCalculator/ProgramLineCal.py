#coding: utf-8
"""
    The program is to calculate the number of lines of
    code in the .py .cpp .c .h code files in the specific
    folder.
"""
import os
import re


def cal_file(file_path):
    """
    The func to analyse the file and
    calculate the number of code lines
    """
    file_comment_line = 0
    file_blank_line = 0

    suffix = os.path.splitext(file_path)[1]

    file_in = open(file_path)
    lines = file_in.readlines()

    file_total_line = len(lines)
    line_index = 0
    if suffix == ".py":
        while line_index < file_total_line:
            line = lines[line_index]
            if line.startswith("#"):
                file_comment_line += 1
            elif re.match("\s*'''", line) is not None:
                file_comment_line += 1
                line_index += 1
                while re.match(".*'''$", line) is None:
                    line = lines[line_index]
                    file_comment_line += 1
                    line_index += 1
            elif line == "\n":
                file_blank_line += 1
            line_index += 1
    elif suffix == ".c":
        while line_index < file_total_line:
            line = lines[line_index]
            if re.match("\s*/\*", line) is not None:
                file_comment_line += 1
                line_index += 1
                while re.match(".*\*/$", line) is None:
                    line = lines[line_index]
                    file_comment_line += 1
                    line_index += 1
            elif line == "\n":
                file_blank_line += 1
            line_index += 1
    elif suffix == ".cpp" or ".h":
        while line_index < file_total_line:
            line = lines[line_index]
            if re.match("\s*//", line) is not None:
                file_comment_line += 1
            elif re.match("\s*/\*", line) is not None:
                file_comment_line += 1
                line_index += 1
                while re.match(".*\*/$", line) is None:
                    line = lines[line_index]
                    file_comment_line += 1
                    line_index += 1
            elif line == "\n":
                file_blank_line += 1
            line_index += 1

    file_line = [file_total_line,
                 file_comment_line, file_blank_line]

    return file_line


def cal_dir(dir_path):
    """
    The func to walk the dir
    """
    dir_total_line = [0,0,0]

    if os.access(dir_path, os.F_OK):
        os.chdir(dir_path)
        file_dir = os.listdir(dir_path)

        for file_name in file_dir:
            file_path = os.path.join(dir_path, file_name)
            if os.path.isdir(file_path):
                dir_line = cal_dir(file_path)
                dir_total_line[0] += dir_line[0]
                dir_total_line[1] += dir_line[1]
                dir_total_line[2] += dir_line[2]
            else:
                dir_line = cal_file(file_path)
                dir_total_line[0] += dir_line[0]
                dir_total_line[1] += dir_line[1]
                dir_total_line[2] += dir_line[2]

    return dir_total_line


def run(top_path):
    """
    The func to start calculate
    """
    total_line = cal_dir(top_path)
    print "The total number of code lines  is %d,\n" \
          "The total number of comment lines is %d,\n" \
          "The total number of blank lines is %d " \
          % (total_line[0], total_line[1], total_line[2])

if __name__ == '__main__':
    target_path = raw_input("Entry the file path")
    run(target_path)