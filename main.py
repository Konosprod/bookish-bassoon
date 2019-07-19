import sys
import os
import argparse

def Extract(infile, outputdir):
    arcContent = open(infile, "rb")
    arcHeader = open(infile.replace("gpk", "gtb"), "rb")

    if not outputdir.endswith("/"):
        outputdir += "/"

    if not os.path.exists(outputdir):
        os.makedirs(outputdir)

    nbFiles = int.from_bytes(arcHeader.read(0x04), "little")
    print(str(nbFiles) + " files")
    print("-------------------------")
    listFileNamesOffset = []
    listFileNames = []
    listFileOffset = []

    for i in range(0, nbFiles):
        endOffset = int.from_bytes(arcHeader.read(0x04), "little")
        listFileNamesOffset.append(endOffset)
        #print("Offset : 0x{:08X}".format(endOffset))
        sys.stdout.flush()


    for i in range(0, nbFiles):
        offset = int.from_bytes(arcHeader.read(0x04), "little")
        listFileOffset.append(offset+0x40)
        #print("Offset : 0x{:08X}".format(offset))
        sys.stdout.flush()


    beginStringTable = arcHeader.tell()
    for i in range (0, nbFiles):
        starting = listFileNamesOffset[i] + beginStringTable
        arcHeader.seek(starting, 0)
        filename = bytearray()
    
        reading = True

        while reading:
            val = arcHeader.read(1)
            if int.from_bytes(val, "little") != 0x00:
                filename += val
            else:
                reading = False
            

        listFileNames.append("".join( chr(x) for x in bytearray(filename)))
    
    arcContent.seek(0, 2)
    endOfFile = arcContent.tell()
    arcContent.seek(0, 0)

    for i in range(0, nbFiles):
        print("Extracting " + listFileNames[i])
        arcContent.seek(listFileOffset[i])
        endOffset = 0

        if i+1 < nbFiles:
            endOffset = listFileOffset[i+1]
        else:
            endOffset = endOfFile

        file_size = endOffset - listFileOffset[i]

        fileout = open(outputdir + listFileNames[i]+".png", "wb")

        while file_size > 0:
            if file_size >= 1024:
                data = arcContent.read(1024)
            else:
                data = arcContent.read(file_size)

            fileout.write(data)
            file_size -= (1024 if (file_size >= 1024) else file_size)

        fileout.close()

        sys.stdout.flush()

    arcContent.close()
    arcHeader.close()



parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-x", "--extract", help="Extract GPK", action="store_true")
parser.add_argument("input", help="Input file")
parser.add_argument("output", help="Output directory")

args = parser.parse_args()

if args.extract:
    Extract(args.input, args.output)