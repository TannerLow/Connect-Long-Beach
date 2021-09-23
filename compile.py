import os
import shutil
import sys

angular_path = os.path.join(os.getcwd(), "angular")
compile_command = "cd \"" + angular_path + "\" && ng build --base-href /static/"
src_dir = "angular\\dist\\angular"
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
files = os.listdir(os.path.join(os.getcwd(), src_dir))
for file in files:
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

print("Files done copying")