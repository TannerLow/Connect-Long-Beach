import os
import shutil
import sys

angular_path = os.path.join(os.getcwd(), "angular")
compile_command = "cd \"" + angular_path + "\" && ng build --base-href /"
src_dir = os.path.join("angular", "dist", "angular")
dst_templates = "templates"
dst_static = "static"

# Executes system call to run command in terminal
def runCommand(command, fail_msg):
    if os.system(command):
        print(fail_msg) # System call returned a non-zero result
        sys.exit(0)

# Get file extension of given filename/filepath
def getExtension(filename):
    tokens = filename.split(".")
    return tokens[len(tokens)-1]


runCommand(compile_command, "Failed to build. Copying aborted.")

# Generate list of files in dist directory and copy them over
path = os.path.join(os.getcwd(), src_dir)
files = os.listdir(path)
for file in files:
    if not os.path.isdir(os.path.join(path, file)):
        print("Copying", file, "...")
        # Put html files in templates folder
        if getExtension(file) == "html":
            filepath = os.path.join(src_dir, file)
            destination = os.path.join(dst_templates, file)
            shutil.copy2(filepath, destination)
        # Put everything else in static folder
        else:
            filepath = os.path.join(src_dir, file)
            destination = os.path.join(dst_static, file)
            shutil.copy2(filepath, destination)
    else:
        filepath = os.path.join(src_dir, file)
        destination = os.path.join(dst_static, file)
        shutil.rmtree(os.path.join(dst_static, file))
        shutil.copytree(filepath, destination)


# Delete old files
path = os.path.join(os.getcwd(), dst_static)
destination_files = os.listdir(path)
for file in destination_files:
    if file not in files:
        os.remove(os.path.join(dst_static, file))

# Make index.html file compatible with flask by inserting static where necessary
filepath = "templates/index.html"
file = open(filepath, "r")
contents = file.read()
contents = contents.split('\"')

# insert /static/ before all file names belonging to the /static folder
for i in range(len(contents)):
    token = contents[i]
    if "styles." in token or "runtime." in token or "polyfills." in token or "main." in token:
        contents[i] = "/static/" + token

with_static = '\"'.join(contents)
file.close()

# Update the file with the insertted text
file = open(filepath, "w")
file.write(with_static)
file.close()


print("Files done copying")