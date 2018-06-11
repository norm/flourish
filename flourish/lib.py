import os


def relative_list_of_files_in_directory(directory):
    _file_list = []
    _trim = len(directory) + 1
    for _root, _dirs, _files in os.walk(directory):
        _dirs = sorted(_dirs)
        _subdir = _root[_trim:]
        for _file in sorted(_files):
            if len(_subdir):
                _file_list.append('%s/%s' % (_subdir, _file))
            else:
                _file_list.append(_file)
    return _file_list
