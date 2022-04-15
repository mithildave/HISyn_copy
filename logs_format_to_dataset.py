import sys
counter = 0

def main():
    global counter
    counter +=1
    n= len(sys.argv)
    for i in range(1,n):
        file=sys.argv[i]
        # open your csv and read as a text string
        my_csv_path = file
        with open(my_csv_path, 'a') as f:
            f.write("\n\n"+"TestCase1"+"  **+Counter**"+str(counter)+"\n\n")

    cmdline_text = "test"
    cmdline_text = cmdline_text +"#1"
    print(cmdline_text)
#.test%*

if __name__ == '__main__':

    main()