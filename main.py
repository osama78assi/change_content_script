from os import listdir, getcwd
from os.path import isfile, join, isdir
from typing import List, Callable
from re import sub, Match, Pattern


def is_accepted_extnsion(wanted_exts: str | List[str], extention: str) -> bool:
    """
    ### _summary_
        Check if the passed extension is accepted according to the passed extensions
    ### Args:
        wanted_exts (str | List[str]): List of extensions or single extension
        extention (str): The wanted extension

    ### Returns:
        bool: Wether the passed extension is accepted or not
    """
    if wanted_exts == '*':
        return True
    
    if type(wanted_exts) == str:
        return extention == wanted_exts
    
    if type(wanted_exts) == list:
        return extention in wanted_exts
    
    return False


def read_files_paths_from_dir(dir_path=getcwd(), wanted_exts: str | List[str]='*', ignore: list = [], skip_hidden: bool=True) -> list:
    """
    ### _summary_
        This function return all file paths as a list for giving directory path
    ### Args:
        dir_path (str, optional): Path to the directory. Defaults to getcwd().
        ignore (list, optional): Files names to ignore. Defaults to [].
        wanted_exts (str|list, optional): The wanted extension of files. Defaults to '*'.
        skip_hidden (bool): Wether to skip hidden files or not. Defaults to True

    ### Raises:
        ValueError: When the passed path isn't a directory
        ValueError: When the passed extensions list isn't made of strings

    ### Returns:
        list: a list of paths
    """
    
    if not isdir(dir_path):
        raise ValueError('dir_path should be a path to directory not a file')
    
    if type(wanted_exts) == list:
        for ext in wanted_exts:
            if type(ext) != str:
                raise ValueError("Extensions list must be made of strings")
    
    only_files = []
    
    for file_name in listdir(dir_path):
        if \
        isfile(join(dir_path, file_name)) \
        and (not file_name.startswith('.') if skip_hidden else True) \
        and is_accepted_extnsion(wanted_exts, file_name.split('.')[1]) \
        and file_name not in ignore:
            only_files.append(join(dir_path, file_name))
    
    return only_files


def rec_read_all_files_paths(dir_path=getcwd(), ignore=[], wanted_exts='*', skip_hidden: bool=True) -> list:
    """
    ### _summary_
        Recursively read all files in nested folders and return all paths for the wanted extensions
    ### Args:
        dir_path (str, optional): Path to the directory. Defaults to getcwd().
        ignore (list, optional): Folders or/and Files names to ignore. Defaults to [].
        wanted_ext (str, optional): The wanted extension of files. Defaults to '*'.
        skip_hidden (bool): Wether to skip hidden files or not. Defaults to True

    ### Raises:
        ValueError: When the passed path isn't a directory
        ValueError: When the passed extensions list isn't made of strings

    ### Returns:
        list: a list of paths
    """
    
    if not isdir(dir_path):
        raise ValueError('dir_path should be a path to directory not a file')
    
    if type(wanted_exts) == list:
        for ext in wanted_exts:
            if type(ext) != str:
                raise ValueError("Extensions list must be made of strings")
    all_files = []
    
    for child_dir_name in listdir(dir_path):
        if isdir(join(dir_path, child_dir_name)) \
            and (not child_dir_name.startswith('.') if skip_hidden else True) \
            and (child_dir_name not in ignore):
            all_files.extend(rec_read_all_files_paths(join(dir_path, child_dir_name), ignore, wanted_exts))
        
        # Add all files
        if \
        isfile(join(dir_path, child_dir_name)) \
        and (not child_dir_name.startswith('.') if skip_hidden else True) \
        and is_accepted_extnsion(wanted_exts, child_dir_name.split('.')[1]) \
        and child_dir_name not in ignore:
            all_files.append(join(dir_path, child_dir_name))
    
    return all_files


def change_text_from_file(file_path: str, pattern: str | Pattern[str], repl: str | Callable[[Match[str]], str]):
    """
    ### _summary_
        Take a file path and replace whatever you want with whatever you want too

        Keep in mind if something faild while reading the file it will raise an error.
    ### Args:
        file_path (str): The path for the file you want
        pattern (str | Pattern[str]): The pattern you want to replace
        repl (str | Callable[[Match[str]], str]): What you want to replace by. If it's a function it will take a Match[str] Object and must return a string

    ### Returns:
        bool: _description_
    """
    content = ""
    with open(file_path, 'r') as file:
        content = sub(pattern, repl, file.read())
    
    with open(file_path, 'w') as file:
        file.write(content)


def change_text_from_files(files_paths: List[str], pattern: str | Pattern[str], repl: str | Callable[[Match[str]], str]):
    """
    ### _summary_
        Take files paths and replace whatever you want with whatever you want too

        Keep in mind if something faild while reading the file it will raise an error.
    ### Args:
        file_path (str): The path for the file you want
        pattern (str | Pattern[str]): The pattern you want to replace
        repl (str | Callable[[Match[str]], str]): What you want to replace by. If it's a function it will take a Match[str] Object and must return a string

    ### Returns:
        bool: _description_
    """
    for file_path in files_paths:
        change_text_from_file(file_path, pattern, repl)


def check_references(files_paths: List[str], look_for: str) -> List[str]:
    """_summary_
        Take files paths and check for reference for class, method or even variable distributed over many files
    Args:
        files_paths (List[str]): The path for the files you want to search for
        look_for (str): Method, variable or class to check for its references

    Returns:
        List[str]: reference with file name and line
    """
    res = []

    for file_path in files_paths:
        with open(file_path, 'r') as file:
            for line_index, line in enumerate(file.readlines()):
                if look_for in line:
                    res.append(look_for + " in file " + file_path + ":" + str(line_index+1) + " in line " + str(line_index+1))
    
    return res


if __name__ == "__main__":
    # Take simple input from terminal But calling the methods as you want and pass replace function is much better and helpful
    # exts = []
    # exts_count = int(input("Enter how many extensions you want to include: "))
    
    # for _ in range(exts_count):
    #     exts.append(input("Enter the extension you want: "))
    
    # ignore = []
    # ignore_count = int(input("Enter how many file/folder you want to ignore: "))
    
    # for _ in range(ignore_count):
    #     ignore.append(input("Enter the file/folder name you want to ignore: "))
    
    # skip_hidden = False
    # while not skip_hidden:
    #     ans = input("Do you want to skip hidden folders/files (y/n): ")
    #     if ans.lower() == 'n':
    #         skip_hidden = False
    #         break
    #     elif ans.lower() == 'y':
    #         skip_hidden = True
    
    # pattern = input("Enter the pattern you want to match (Regex accpeted): ")
    
    # replac_with = input("Enter the value you want to replace with: ")
    
    # entry_point = input("Enter your entry point directory: ")
    
    # paths = rec_read_all_files_paths(entry_point, ignore, exts)
    # change_text_from_files(paths, pattern, replac_with)
    
    # print("Check now.")

    # files = rec_read_all_files_paths(ignore=['node_modules'], wanted_exts='js')

    # res = check_references(files, "authRouter")

    # for r in res:
    #     print(r)
    
    pass
