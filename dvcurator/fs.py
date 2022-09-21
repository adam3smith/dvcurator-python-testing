# check whether dropbox folder is set correctly
def check_dropbox(dropbox, project_name=None):
    import os.path
    from glob import glob
    if not os.path.exists(dropbox):
        print("Dropbox folder not found: " + dropbox) 
        return None
    if not project_name:
        # check if there's any existing "QDR Project - " folders
        test_folders = glob(os.path.join(dropbox, "QDR Project - *"))
        if (len(test_folders) < 1):
            print("ALERT: No existing QDR project folders found in: " + dropbox)
            print("Continuing anyway...")
    else:
        folder_name = 'QDR Project - ' + project_name
        path = os.path.normpath(os.path.join(dropbox, folder_name))
        if os.path.exists(path):
            return path
        else:
            print("Project folder does not exist: " + path)
            return None

    # return true as long as the dropbox path exists if we're not checking for the subfolder
    return True

# What is the latest folder under QDR Prepared?
def current_step(folder):
    from glob import glob
    import os.path
    if not os.path.isdir(folder):
        print("Error: not a folder " + folder)
        return None
    candidates = glob(os.path.join(folder, "[0-9]_*"))
    if (len(candidates) < 1):
        print("Error: no folders found under " + folder)
        return None
    current = candidates[len(candidates)-1]
    return current

# Copy QDR prepared latest step to a new step, incrementing step number
def copy_new_step(folder, step):
    #exists = check_dropbox(dropbox, project_name)
    #if not exists:
    #    return None
    import os.path
    if not os.path.exists(folder):
        print("Subfolder not detected: " + folder)
        return None

    import os.path
    from shutil import copytree
    edit_path = os.path.normpath(os.path.join(folder, "QDR Prepared"))
    current = current_step(edit_path)
    if not current:
        return None
    number = int(os.path.split(current)[1].split("_")[0]) + 1
    new_step = str(number) + "_" + step
    copytree(os.path.join(edit_path, current), os.path.join(edit_path, new_step))
    return os.path.join(edit_path, new_step)
