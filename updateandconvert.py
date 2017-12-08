# -*- coding: utf-8 -*-
import csv, os, json, codecs, cStringIO, re, unidecode, unicodedata,  sys, getopt, Tkinter, tkFileDialog, string


def main(argv):
    input_file = ''
    output_file = ''
    format = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:f:",["ifile=","ofile=","format="])
    except getopt.GetoptError:
        print 'csv_json.py -i <path to inputfile> -o <path to outputfile> -f <dump/pretty>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'csv_json.py -i <path to inputfile> -o <path to outputfile> -f <dump/pretty>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg
        elif opt in ("-f", "--format"):
            format = arg
    read_csv(input_file, output_file, format)

#Read CSV File
def read_csv(file, json_file, format):
    csv_rows = []
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        title = reader.fieldnames
        for row in reader:
            csv_rows.extend([{title[i]:row[title[i]] for i in range(len(title))}])
        write_json(csv_rows, json_file, format)

#Convert csv data into json and write it
def write_json(data, json_file, format):
    with open(json_file, "w") as f:
        if format == "pretty":
            f.write(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': '),encoding="utf-8",ensure_ascii=False))
        else:
            f.write(json.dumps(data))

#if __name__ == "__main__":
#   main(sys.argv[1:])

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")



root = Tkinter.Tk()
root.withdraw()

inputFileName = tkFileDialog.askopenfilename()
print inputFileName

# inputFileName = r"C:\Users\Porter\Downloads\jopelist.csv"
outputFileName = os.path.splitext(inputFileName)[0] + "_modified.csv"
jsonFileName = "jopebot.json"

with open(inputFileName, 'rb') as inFile, open(outputFileName, 'wb') as outfile:
    #print inFile.readline()
    r = UTF8Recoder(inFile,"utf-16")
    w = csv.writer(outfile, delimiter=',')
    w.writerow(['Enabled', 'artistName', 'songName', 'albumName', 'year', 'songLength', 'charterName', 'genreName'])
    for row in r:
        # print row
        if "Enabled;Artist;Song" in "".join(row) or "sep=;" in "".join(row):
            pass
        else:
            formatted = "".join(codecs.decode(row,"utf-8"))
            try:
                noSpecialCharacters = unicodedata.normalize('NFKD', formatted).encode('ascii', 'ignore')
                # noSpecialCharacters = unidecode.unidecode(formatted).encode("ascii")
                print noSpecialCharacters
            except Exception, e:
                # This is just a failsafe
                print "FAIL"
                noSpecialCharacters = re.sub('[^a-zA-Z0-9; \n\.]', '', formatted)
                print noSpecialCharacters
            
            final = noSpecialCharacters.replace("\\"," - ").split(";")
            final[5] = float(final[5])*1000
            final[7] = ""
            w.writerow(final)

read_csv(outputFileName, jsonFileName, "pretty")

os.remove(outputFileName)

raw_input("JSON SAVED IN OUTPUT FOLDER - PRESS ENTER")

