import sys
"""
Write the provided code to a file named "codes.txt".

Args:
    code (str): The code to write to the file.
"""
f = open("codes.txt", "w")
f.write(sys.argv[1])
f.close