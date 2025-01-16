#!/usr/bin/python

import srt
import sys

def srt_to_hour(srt_generator, timeframe):
    '''
    :param srt_generator: Subtitles in SRT format parsed as srt generator
    :type srt_generator: srt. or a file-like object
    :type srt_generator: :term:`generator` of :py:class:`srt.Subtitle` objects
    '''
    
    tmp_hour = None
    tmp_subtitle = None
    
    # example: 2021-09-05 00:12
    # len(example) = 16
    if timeframe == 'h':
        # when flattening to hour, compare the first 13 characters
        extract_timeframe = lambda s : s[0:13]
        modify_content = lambda s : s[0:13] + ":00"
    elif timeframe == 'd':
        # when flattening to day, compare the first 10 characters
        extract_timeframe = lambda s : s[0:10]
        modify_content = extract_timeframe
    else:
        raise "timeframe value "+timeframe+" unknown"
        
    
    for subt in srt_generator:
        
        hour = extract_timeframe( subt.content )
        # note end
        if tmp_subtitle is not None:
            tmp_subtitle.end = subt.end
        
        # is this the first frame in that hour?
        if tmp_hour == hour:
            continue
        
        # its a new hour
        if tmp_subtitle is not None:
            # previous subtitle goes until this one
            tmp_subtitle.end = subt.start
            yield tmp_subtitle
        tmp_hour = hour
        # prepare a new subtitle
        tmp_subtitle = srt.Subtitle(
            index = None,
            start=subt.start,
            end=subt.end,
            
            content=modify_content(subt.content)
        )
    if tmp_subtitle is not None:
        yield tmp_subtitle




def srtfile_to_hours(srt_infilename, srt_outfilename, timeframe):
    with open(srt_infilename, "r") as srt_infile:
        print("reading from "+srt_infilename)
        srt_generator = srt.parse(srt_infile)
        srt_to_hour_generator = srt_to_hour(srt_generator, timeframe)
        with open(srt_outfilename, "w") as srt_outfile:
            srt_outfile.write(srt.compose(srt_to_hour_generator))
    print("written to   "+srt_outfilename)


def main():
    try:
        srt_infilename = sys.argv[1]
        srt_outfilename =  sys.argv[2]
        timeframe =  'd' if ((len(sys.argv) == 4) and sys.argv[3] == '--days') else 'h'
    except e:
        print('Reduces Time Stamp SRT entries to full hours')
        print('Usage: python srt-to-hours.py <infile.srt> <outfile.srt> [--days]')        
        print('  --days: set this to flatten to days instead of just hours')
        print('example: ')
        print('python srt-to-hours.py "2021-09-05 to 09-11 timelapse_1080.srt" "2021-09-05 to 09-11 timelapse_1080_hours.srt"')
        sys.exit(2)
    srtfile_to_hours (srt_infilename, srt_outfilename, timeframe)


if __name__ == "__main__":
    main()