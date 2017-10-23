#Top Level of LazyDJ
#Created on Oct 22, 2017
#Ike Lee

from analyze import analyze
import sys

def main(folderLocation): 
	analyze(folderLocation)


if __name__== "__main__": 
	main(sys.argv[1])