import db
import fancy_printer
import subprocess
import os


def calign(s1, s2):
    cwd = os.getcwd()
    subprocess.call([cwd + "/cal.exe", s1, s2])
    with open("tmp.txt") as tmp:
        s1 = tmp.readline().replace("\n", "")
        s2 = tmp.readline().replace("\n", "")
    os.remove("tmp.txt")
    return s1, s2

def main():
    query1 = input("UNIPROT ID OF SEQ 1: ")
    query2 = input("UNIPROT ID OF SEQ 2: ")
    s1 = db.getseq(query1)
    s2 = db.getseq(query2)
    db.getseq(query1, erase=True)
    db.getseq(query2, erase=True)
    s1, s2 = calign(s1, s2)
    outputfilename = input("output filename: ")
    fancy_printer.print_alignment(s1, s2, filename=outputfilename)
    return 0

def test():
    query1 = "P01130"
    query2 = "Q99087"
    s1 = db.getseq(query1)
    s2 = db.getseq(query2)
    db.getseq(query1, erase=True)
    db.getseq(query2, erase=True)
    s1, s2 = calign(s1, s2)
    outputfilename = input("output filename: ")
    fancy_printer.print_alignment(s1, s2, filename=outputfilename)
    return 0

if __name__ == '__main__':
    import sys
    opts = sys.argv
    
    if "-test" in opts:
        test()
    else:
        main()

# P01130 Human LDL Receptor
# Q99087 Xenopus laevis LDL Receptor 1

