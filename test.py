import re

string = '(6:9; 1:7)'

string = string.replace(':', ' ')
string = string.replace(';', ' ')
string = string.replace('(', ' ')
string = string.replace(')', ' ')

print(string.split())