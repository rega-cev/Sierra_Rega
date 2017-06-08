import pyfasta
import tempfile
import os, sys, argparse
from formatMutations import getMutations
from formatAlgorithm import generateCSVHeader, generateCSVLine

def main(argv):
    parser = argparse.ArgumentParser(description='Interpret FASTA file with Stanford service.')
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('-i', '--input', dest='input_file', help='Input file name', required=True)
    requiredNamed.add_argument('-o', '--output', dest='output_file', help='Output file name', required=True)
    #parser.parse_args(['-h'])
    results = parser.parse_args(argv)
    input_file = results.input_file
    output_file = results.output_file

    f = pyfasta.Fasta(input_file)
    i = 0
    tmp = open(output_file, 'w')
    tmp.write(generateCSVHeader())
    tmp.close()

    for header in f.keys():
        fd, temp_path = tempfile.mkstemp()
        # ... do stuff with dirpath
        target = open(temp_path, 'w')
        target.write(">" + str(header) + "\n")
        target.write(str(f[header]))
        target.close()
        #data = client.execute("fasta",temp_path)
        os.system("sierrapy fasta " + temp_path + " -o input." + str(i) + ".json")
        os.close(fd)
        os.remove(temp_path)

        #write mutations to temp file
        fd_mut, temp_path_mut = tempfile.mkstemp()
        target_mut = open(temp_path_mut, 'w')
        target_mut.write(getMutations("input." + str(i) + ".json"))
        target_mut.close()
        os.system("sierrapy patterns "+ temp_path_mut +" -o output." + str(i) + ".json -q ~/git/SierraPy_Rega/rega_query_2.gql")
        os.close(fd_mut)
        os.remove(temp_path_mut)

        tmp = open(output_file, 'a')
        tmp.write(generateCSVLine(str(header), "output." + str(i) + ".json") + "\n")
        tmp.close()

        os.remove("input." + str(i) + ".json")
        os.remove("output." + str(i) + ".json")
        #shutil.rmtree(dirpath)
        i += 1

if __name__ == "__main__":
   main(sys.argv[1:])
