#!/usr/bin/python

import srt
import sys
import datetime

'''
the start time to add
'''
add_time_starttime = datetime.timedelta(0)
'''
the last end yielded by add_time
'''
add_time_lastend = datetime.timedelta(0)

def add_time(srt_generator):
    '''
    add the add_time_starttime to the SRT.
    set add_time_lastend on each yield to know the duration of the current SRT file 
    
    I considered on 2024-10-09 to use an object generator and use member variables, 
    but as this would be a singleton and for each file new, chose the global variables.
    
    :param srt_generator: Subtitles in SRT format parsed as srt generator
    :type srt_generator: :term:`generator` of :py:class:`srt.Subtitle` objects
    returns a generator of :py:class:`srt.Subtitle` objects that add to time
    '''
    global add_time_starttime, add_time_lastend
    for subt in srt_generator:
        # remember original subt.end
        add_time_lastend = subt.end 
        subt.start = add_time_starttime + subt.start
        subt.end = add_time_starttime + subt.end
        yield subt



def concat_srt_files(srt_filenames, srt_outfilename):
    '''
    Concatenate srt_filenames to srt_outfilename
    
    TODO: this only writes the first day
    
    '''
    global add_time_starttime, add_time_lastend
    with open(srt_outfilename, "w") as srt_outfile:
        for srt_infilename in srt_filenames:
            with open(srt_infilename, "r") as srt_infile:
                print("reading from "+srt_infilename)
                srt_generator = srt.parse(srt_infile)
                srt_concat_generator = add_time(srt_generator)
                tmp_s = srt.compose(srt_concat_generator)
                srt_outfile.write(tmp_s)
                print("... "+str(len(tmp_s))+" characters")
            # add the duration of the last file to add_time_starttime
            add_time_starttime = add_time_starttime + add_time_lastend
    print("written to   "+srt_outfilename)

def load_srt_filenames(filename):
    '''
    Load srt filenames from filename. 
    '''
    print("reading '"+filename+"'")
    with open(filename, "r") as f:
        srt_filenames = f.readlines()
        
    # remove the tailing \n using rstrip
    return [d.rstrip('\n') for d in srt_filenames]


def main():
    if 3 != len(sys.argv):
        print('Concatenates SRT files. Input files are read from a text file from inputfilename.')
        print('Usage: python srt-concatenate.py <inputfilename> <outputfilename>')
        print('example: ')
        print('python srt-concatenate.py "days-srt.txt" "result.srt"')
        sys.exit(2)
    filename = sys.argv[1]
    outputfilename = sys.argv[2]
    srt_filenames = load_srt_filenames(filename)
    concat_srt_files (srt_filenames, outputfilename)


if __name__ == "__main__":
    main()