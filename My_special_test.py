# Script to validate output for OMS 6250 Project 2  
# Based on Project 2 Autograder by Michael Brown
# Copyright 2017 Kelly Parks 

import os
import getopt
import sys
import decimal
from Switch import *


def main():
    switch =  Switch(1,None,None)
    switch.send_initial_messages()
    print("Hello \n")


if __name__ == "__main__":
   main()
