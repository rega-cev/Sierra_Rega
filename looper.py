import pyfasta
import tempfile
import os, sys, argparse
import multiprocessing as mp
from multiprocessing import Pool, Value, Process
from formatMutations import getMutations
from formatAlgorithm import generateCSVHeader, generateCSVLine

def doStanfordAnalysis(header, sequence, output_file, graphQL_query_file):
    # global counter
    # += operation is not atomic, so we need to get a lock:
    # with counter.get_lock():
        # counter.value += 1
    # print counter.value
    fd, temp_path = tempfile.mkstemp()

    fd2,temp_path2 = tempfile.mkstemp()

    fd3,temp_path3 = tempfile.mkstemp()
    # ... do stuff with dirpath
    target = open(temp_path, 'w')
    target.write(">" + str(header) + "\n")
    target.write(str(sequence))
    target.close()
    #data = client.execute("fasta",temp_path)
    os.system("sierrapy fasta " + temp_path + " -o " + temp_path2)
    os.close(fd)
    os.remove(temp_path)

    #write mutations to temp file
    fd_mut, temp_path_mut = tempfile.mkstemp()
    target_mut = open(temp_path_mut, 'w')
    target_mut.write(getMutations(temp_path2))
    target_mut.close()
    os.system("sierrapy patterns "+ temp_path_mut +" -o "+temp_path3+" -q " + graphQL_query_file)
    os.close(fd_mut)
    os.remove(temp_path_mut)

    #tmp = open(output_file, 'a')
    #tmp.write(generateCSVLine(str(header), "output." + str(i) + ".json") + "\n")
    #tmp.close()
    print "Working on: " + str(header)
    csvLine = generateCSVLine(str(header), temp_path3)
    if csvLine is not None:
        toReturn = str(csvLine + "\n")
    else:
        toReturn = str(header + ',')
    print toReturn
    #os.remove("input." + str(counter.value) + ".json")
    #os.remove("output." + str(counter.value) + ".json")

    os.close(fd2)
    os.close(fd3)
    os.remove(temp_path2)
    os.remove(temp_path3)
    return toReturn

def main(argv):
    parser = argparse.ArgumentParser(description='Interpret FASTA file with Stanford service.')
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('-i', '--input', dest='input_file', help='Input file name', required=True)
    requiredNamed.add_argument('-o', '--output', dest='output_file', help='Output file name', required=True)
    requiredNamed.add_argument('-q', '--query', dest='graphQL_query_file', help='GraphQL query file', required=True)
    #parser.parse_args(['-h'])
    results = parser.parse_args(argv)
    input_file = results.input_file
    output_file = results.output_file
    graphQL_query_file = results.graphQL_query_file

    tmp = open(output_file, 'w')
    tmp.write(generateCSVHeader())
    tmp.close()

    f = pyfasta.Fasta(input_file)

    nrLoops = int(len(f.keys()) / 1000)

    # Per 1000 sequences, do a Stanford analysis
    for i in range(0,nrLoops):
        headers = list( f.keys()[j] for j in range(i*1000,(i*1000) + 1000) )
        pool = mp.Pool(processes=100)
        results = [pool.apply_async(doStanfordAnalysis, args=(header, f[header], output_file, graphQL_query_file,)) for header in headers]
        tmp = open(output_file, 'a')
        for p in results:
            tmp.write(p.get())
        tmp.close()

    #print nrLoops*1000 + ((nrLoops + len(f.keys())) % 1000)
    # Do the Stanford analysis for the last sequences available
    headers = list( f.keys()[j] for j in range(nrLoops*1000,(nrLoops*1000 + (len(f.keys()) % 1000))))
    pool = mp.Pool(processes=100)
    results = [pool.apply_async(doStanfordAnalysis, args=(header, f[header], output_file, graphQL_query_file,)) for header in headers]
    tmp = open(output_file, 'a')
    for p in results:
        tmp.write(p.get())
    tmp.close()

        #print "First " + str(i*1000) + " done."
        #for j in range(i*1000,(i*1000) + 1000):
        #    print " j: " + str(j)

    #print nrLoops

    #pool = mp.Pool(processes=4)
    #results = [pool.apply_async(doStanfordAnalysis, args=(header, f[header], output_file, graphQL_query_file,)) for header in f.keys()]
    # output = [p.get() for p in results]
    # print(output)

    # tmp = open(output_file, 'a')
    # for p in results:
    #     tmp.write(p.get())
    # tmp.close()

    #for i in range(1,counter.value):
    #    os.remove("input." + str(i) + ".json")
    #    os.remove("output." + str(i) + ".json")
    # for header in f.keys():
        # doStanfordAnalysis(header, f[header], i, output_file, graphQL_query_file)
        # i += 1
    # procs = []

    # for header in f.keys():
    #     proc = Process(target=doStanfordAnalysis, args=(header, f[header], output_file, graphQL_query_file,))
    #     procs.append(proc)
    #     proc.start()
    #
    # for proc in procs:
    #     proc.join()
if __name__ == "__main__":
   main(sys.argv[1:])
