i = 4
d = 4.0
s = 'HackerRank '

import sys

# Declare second integer, double, and String variables.
for en, val in enumerate(sys.stdin):
    if en==0:
        ii=int(val)
    elif en==1:
        dd=float(val)
    elif en==2:
        ss=str(val)

# Read and save an integer, double, and String to your variables.
# Print the sum of both integer variables on a new line.
print(i + ii)

# Print the sum of the double variables on a new line.
print(d + dd)

# Concatenate and print the String variables on a new line
# The 's' variable above should be printed first.
print(s + ss)
