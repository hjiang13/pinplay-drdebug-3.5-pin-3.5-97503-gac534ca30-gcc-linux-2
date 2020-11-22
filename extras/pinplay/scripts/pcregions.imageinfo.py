#!/usr/bin/env python
# BEGIN_LEGAL
# BSD License
#
# Copyright (c)2018 Intel Corporation. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.  Redistributions
# in binary form must reproduce the above copyright notice, this list of
# conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution.  Neither the name of
# the Intel Corporation nor the names of its contributors may be used to
# endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE INTEL OR
# ITS CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# END_LEGAL
#
#
# @ORIGINAL_AUTHORS: T. Mack Stallcup, Cristiano Pereira, Harish Patil,
#  Chuck Yount
#

#
# Read in a file of frequency vectors (BBV or LDV) and execute one of several
# actions on it.  Default is to generate a regions CSV file from a BBV file.
# Other actions include:
#   normalizing and projecting FV file to a lower dimension
#
# November 2016: Modified by Harish Patil to create LLVMPoints
# Requires Python scripts from SDE (PinPlay) kit (sde-pinplay-*-lin)
# Used by  the script 'runllvmsimpoint.sh'


import datetime
import glob
import math
import optparse
import os
import random
import re
import sys
import argparse


def PrintAndExit(msg):
    """
    Prints an error message exit.

    """
    sys.stderr.write(msg)
    sys.stderr.write("\n")
    sys.exit(-1)

def PrintMsg(msg):
    """
    Prints an message 
    """
    sys.stdout.write(msg)
    sys.stdout.write("\n")
    sys.stdout.flush()

def PrintMsgNoCR(msg):
    """
    Prints an message 
    """
    sys.stdout.write(msg)
    sys.stdout.flush()

def OpenFile(fl, type_str):
    """
    Check to make sure a file exists and open it.

    @return file pointer
    """

    # import pdb;  pdb.set_trace()
    if not os.path.isfile(fl):
        PrintAndExit('File does not exist: %s' % fl)
    try:
        fp = open(fl, 'rb')
    except IOError:
        PrintAndExit('Could not open file: %s' % fl)

    return fp

def IsInt(s):
    """
    Is a string an integer number?

    @return boolean
    """
    try:
        int(s)
        return True
    except ValueError:
        return False

def IsFloat(s):
    """
    Is a string an floating point number?

    @return boolean
    """
    try:
        float(s)
        return True
    except ValueError:
        return False



def OpenFVFile(fv_file, type_str):
    """
    Open a frequency vector file and check to make sure it's valid.  A valid
    FV file must contain at least one line which starts with the string 'T:'.

    @return file pointer
    """

    # import pdb;  pdb.set_trace()
    fp = OpenFile(fv_file, type_str)
    line = fp.readline()
    while not line.startswith('T:') and line:
        line = fp.readline()
    if not line.startswith('T:'):
        PrintAndExit("Invalid " + type_str + fv_file)
    fp.seek(0, 0)

    return fp


def OpenSimpointFile(sp_file, type_str):
    """
    Open a simpoint file and check to make sure it's valid.  A valid
    simpoint file must start with an integer.

    @return file pointer
    """

    fp = OpenFile(sp_file, type_str)
    line = fp.readline()
    field = line.split()
    if not IsInt(field[0]):
        PrintAndExit("Invalid " + type_str + sp_file)
    fp.seek(0, 0)

    return fp



def OpenLabelFile(lbl_file, type_str):
    """
    Open a labels file and check to make sure it's valid.  A valid
    labels file must start with an integer.

    @return file pointer
    """

    fp = OpenFile(lbl_file, type_str)
    line = fp.readline()
    field = line.split()
    if not IsInt(field[0]):
        PrintAndExit("Invalid " + type_str + lbl_file)
    fp.seek(0, 0)

    return fp

def OpenWeightsFile(wt_file, type_str):
    """
    Open a weight file and check to make sure it's valid.  A valid
    wieght file must start with an floating point number.

    @return file pointer
    """

    fp = OpenFile(wt_file, type_str)
    line = fp.readline()
    field = line.split()
    if not IsFloat(field[0]):
        PrintAndExit("Invalid " + weight_str + wt_file)
    fp.seek(0, 0)

    return fp


def GetSlice(fp):
    """
    Get the frequency vector for one slice (i.e. line in the FV file).

    All the frequency vector data for a slice is contained in one line.  It
    starts with the char 'T'.  After the 'T', there should be a sequence
    containing one, or more, of the following sets of tokens:
       ':'  integer  ':' integer
    where the first integer is the dimension index and the second integer is
    the count for that dimension. Ignore any whitespace.

    @return list of the frequency vectors for the slice; element = (dimension, count)
    """

    fv = []
    line = fp.readline()
    while not line.startswith('T') and line:
        # print 'Skipping line: ' + line

        # Don't want to skip the part of BBV files at the end which give
        # information on the basic blocks in the file.  If 'Block id:' is
        # found, then back up the file pointer to before this string.
        #
        if line.startswith('Block id:'):
            fp.seek(0 - len(line), os.SEEK_CUR)
            return []
        line = fp.readline()
    if line == '': return []

    # If vector only contains the char 'T', then assume it's a slice which
    # contains no data.
    #
    if line == 'T\n':
        fv.append((0, 0))
    else:
        blocks = re.findall(':\s*(\d+)\s*:\s*(\d+)\s*', line)
        # print 'Slice:'
        for block in blocks:
            # print block
            bb = int(block[0])
            count = int(block[1])
            fv.append((bb, count))

    # import pdb;  pdb.set_trace()
    return fv


def GetMarker(fp):
    """
    Get the marker ("S:") or ("M:") for one slice 

    Marker data format:
        "S:" marker count 
        "M:" marker count 
     e.g.
        "S: 0x415af8 80"
        "M: 0x7efdef57a301 1"

    @return (marker, count)
    """

    mr = []
    line = fp.readline()
    while not ( line.startswith('S:') or line.startswith('M:')) and line:
        # print 'Skipping line: ' + line

        # Don't want to skip the part of BBV files at the end which give
        # information on the basic blocks in the file.  If 'Block id:' is
        # found, then back up the file pointer to before this string.
        #
        if line.startswith('Block id:'):
            fp.seek(0 - len(line), os.SEEK_CUR)
            return []
        line = fp.readline()
    if line == '': return {'pc':0,'count':0}

    # If vector only contains the char 'S', then assume it's a slice which
    # contains no data.
    #
    if line == 'S\n': return {'pc':0,'count':0}
    if line == 'M\n': return {'pc':0,'count':0}
    mr = line.split()
    #import pdb;  pdb.set_trace()
    return {'pc':mr[1],'count':mr[2]}

def GetFirstPcinfo(fp):
    """
    Get information about the first block executed

    @return {'pc':firstpc,'count':1}
    """

    marker = {'pc':0,'count':0}
    line = fp.readline()
    while not ( line.startswith('S:') or line.startswith('M:')) and line:
        line = fp.readline()
    if line:
        if line.startswith('S:'):
            firstpc = line.split('S:')[1].split()[0]
            marker = {'pc':firstpc,'count':1}
        else:
            firstpc = line.split('M:')[1].split()[0]
            marker = {'pc':firstpc,'count':1}

    # import pdb;  pdb.set_trace()
    return marker

def OutputImageInfo(fp):
    """
    Output records starting with "G:"
    """
    line = fp.readline()
    while line:
        if line and line.startswith('G:'):
            print "#",line
        line = fp.readline()
    # import pdb;  pdb.set_trace()
    return 


def ProcessBlockIdSummary(fp):
    """
    Process records starting with 'Block id:'
     e.g. 'Block id: 2348 0x2aaac42a4306:0x2aaac42a430d'
     e.g. 'Block id: <bbid> <firstPC>:<lastPC>'
        The same 'firstPC' may start multiple 'bbid's.
    @return a dictinary mapping 'firstPC' to a 'list of (bbid, sticount) pairs'
       it starts
    """

    pcbbid_dict = {}
    line = fp.readline()
    while not line.startswith('Block id:') and line:
        line = fp.readline()

    while line.startswith('Block id:') and line:
        tokens = line.split(" ")
        bbid = int(tokens[2])
        pcrange = tokens[3]
        sticount = int(tokens[6])
        pc = pcrange.split(":")[0]
        if pc in pcbbid_dict.keys():
            pcbbid_dict[pc].append((bbid,sticount))
        else:
            pcbbid_dict[pc] = []
            pcbbid_dict[pc].append((bbid,sticount))
        line = fp.readline()

    # import pdb;  pdb.set_trace()
    return pcbbid_dict




def ProcessLabelFile(fp_lbl):
    """
    Process records in a t.labels file
    cluster distance_from_centroid
    slice number is implicit here : sliceNumber = (lineNumber-1)
    @return an array mapping 'sliceN' to the cluster it belongs to
    """

    sliceCluster = [] 
    sliceNum=0
    line = fp_lbl.readline()
    while line:
        tokens = line.split(" ")
        clusterid = int(tokens[0])
        sliceCluster.append(clusterid)
        line = fp_lbl.readline()
        sliceNum = sliceNum + 1

    # import pdb;  pdb.set_trace()
    return sliceCluster

############################################################################
#
#  Functions for generating regions CSV files
#
############################################################################


def GetWeights(fp):
    """
    Get the regions and weights from a weights file.

    @return lists of regions and weights
    """

    # This defines the pattern used to parse one line of the weights file.
    # There are three components to each line:
    #
    #   1) a floating point number  (group number 1 in the match object)
    #   2) white space
    #   3) a decimal number         (group number 2 in the match object)
    #
    # 1) This matches floating point numbers in either fixed point or scientific notation:
    #   -?        optionally matches a negative sign (zero or one negative signs)
    #   \ *       matches any number of spaces (to allow for formatting variations like - 2.3 or -2.3)
    #   [0-9]+    matches one or more digits
    #   \.?       optionally matches a period (zero or one periods)
    #   [0-9]*    matches any number of digits, including zero
    #   (?: ... ) groups an expression, but without forming a "capturing group" (look it up)
    #   [Ee]      matches either "e" or "E"
    #   \ *       matches any number of spaces (to allow for formats like 2.3E5 or 2.3E 5)
    #   -?        optionally matches a negative sign
    #   \ *       matches any number of spaces
    #   [0-9]+    matches one or more digits
    #   ?         makes the entire non-capturing group optional (to allow for
    #             the presence or absence of the exponent - 3000 or 3E3
    #
    # 2) This matches white space:
    #   \s
    #
    # 3) This matches a decimal number with one, or more digits:
    #   \d+
    #
    pattern = '(-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?)\s(\d+)'

    weight_dict = {}
    for line in fp.readlines():
        field = re.match(pattern, line)

        # Look for the special case where the first field is a single digit
        # without the decimal char '.'.  This should be the weight of '1'.
        #
        if not field:
            field = re.match('(\d)\s(\d)', line)
        if field:
            weight = float(field.group(1))
            region = int(field.group(2))
            weight_dict[region] = weight

    return weight_dict


def GetSimpoints(fp):
    """
    Get the regions and slices from the Simpoint file.

    @return list of regions and slices from a Simpoint file
    """

    RegionToSlice = {}
    max_region_number = 0
    for line in fp.readlines():
        field = re.match('(\d+)\s(\d+)', line)
        if field:
            slice_num = int(field.group(1))
            region = int(field.group(2))
            if region > max_region_number:
                max_region_number = region
            RegionToSlice[region] = slice_num

    return RegionToSlice, max_region_number

def GetWarmuppoints(fp, wfactor):
    """
    Get the regions and slices from the Simpoint file.

    @return list of regions and slices from a Simpoint file
    """

    WarmupRegionToSlice = {}
    for line in fp.readlines():
        field = re.match('(\d+)\s(\d+)', line)
        if field:
            slice_num = int(field.group(1))
            region = int(field.group(2))
            WarmupRegionToSlice[region] = slice_num - int(wfactor)

    return WarmupRegionToSlice

def GetRegionBBV(fp, RegionToSlice, max_region_number, pcbblist_dict, sliceCluster):
    """
    Read all the frequency vector slices and the basic block id info from a
    basic block vector file.  Put the data into a set of lists which are used
    in generating CSV regions.

    @return cumulative_icount, region_bbv, region_start_markers, region_end_markers, region_end_marker_relativecount, first_bb_marker
    
    """
    slice_set = set(RegionToSlice.values())

    num_regions = max_region_number + 1
    # region number and cluster id are the same
    # cluster id start at 0 and need not be contiguous.
    # so we need to size our arrays to max_cluster_id + 1

    #import pdb;  pdb.set_trace()

    # List of lists of basic block vectors, each inner list contains the blocks for one of the
    # representative regions. 
    #
    region_bbv = []

    # A tuple {'bbid':x, 'bbcount':y, 'bbinfo':"<fnname:bbname>"}
    current_marker = GetFirstPcinfo(fp)
    first_bb_marker = current_marker
    previous_marker = {}

    # List of start markers for representative regions. 
    region_start_markers = [None] * num_regions

    # List of start markers for representative regions. 
    region_end_markers = [None] * num_regions

    region_end_marker_relativecount = [None] * num_regions

    region_multiplier = [0.0] * num_regions

    # List of per cluster icount
    cluster_icount = [0] * num_regions

    # List of per cluster slicecount
    cluster_slicecount = [0] * num_regions

    # List of the cumulative sum of instructions in the slices.  There is one
    # entry for each slice in the BBV file which contains the total icount up
    # to the end of the slice.
    #
    cumulative_icount = []

    # Cumulative sum of instructions so far
    #
    run_sum = 0

    # Get each slice & generate some data on it.
    #
    slice_num = 0
    #import pdb;  pdb.set_trace()
    while True:
        fv = GetSlice(fp)
        if fv == []:
            break
        previous_marker = current_marker
        current_marker = GetMarker(fp)

        # Get total icount for the basic blocks in this slice
        #
        sum = 0
        for bb in fv:
            count = bb[1]
            sum += count

        # Record the cumulative icount for this slice.
        #
        if sum != 0:
            run_sum += sum
            cumulative_icount += [run_sum]
            clusterid = sliceCluster[slice_num]
            cluster_icount[clusterid] += sum
            cluster_slicecount[clusterid] += 1

        # If slice is a representative region, record the basic blocks of the slice.
        #
        if slice_num in slice_set:
            #import pdb;  pdb.set_trace()
            clusterid = sliceCluster[slice_num]
            region_start_markers[clusterid] = previous_marker 
            region_end_markers[clusterid] = current_marker 
            startPC = previous_marker['pc']
            endPC = current_marker['pc']
            relendPCcount = 1 
            # endPC is going to be executed in the next slice 
            endPCbbidlist = pcbblist_dict[endPC]
            #  now, add executions of endPC in the current slice
            #FIXME : do we need special action if startPC==endPC?
            # relative count is used for region pinball replay
            # and we currently have imprecise logging hence the initial
            # occurrence of endPC (as statPC) is not going to be captured
            # in the pinball. So, till precise logging becomes the default
            # we will continue to decrease relendPCcount by 1
            if startPC == endPC:
                relendPCcount = 0 
            for bbidpair in endPCbbidlist:
                thisitem = [item for item in fv if item[0] == bbidpair[0] ]
                if not thisitem:
                    break
                thispair = thisitem[0] 
                thiscount = thispair[1] 
                bbidsticount = bbidpair[1] 
                thisPCcount = thiscount/bbidsticount
                relendPCcount += thisPCcount
            region_end_marker_relativecount[clusterid] = relendPCcount 
        slice_num += 1

    #import pdb;  pdb.set_trace()
    total_num_slices = len(cumulative_icount)
    for region in sorted(RegionToSlice.keys()): 
        multiplier = float(cluster_icount[region])/float(run_sum)*total_num_slices
        region_multiplier[region] = multiplier
    return cumulative_icount, cluster_icount, cluster_slicecount, region_bbv, region_multiplier, region_start_markers, region_end_markers, region_end_marker_relativecount, first_bb_marker

def GetWarmupRegionBBV(fp, WarmupRegionToSlice, max_region_number, wfactor, pcbblist_dict):
    """
    Read all the frequency vector slices and the basic block id info from a
    basic block vector file.  Put the data into a set of lists which are used
    in generating CSV regions.

    @return warmup_region_start_markers, warmup_region_end_markers, warmup_region_end_marker_relativecount  
    """
    slice_set = set(WarmupRegionToSlice.values())

    num_regions = max_region_number+1;

    # A tuple {'pc':x, 'count':y}
    current_marker = GetFirstPcinfo(fp)
    previous_marker = {}

    # List of start markers for representative regions. 
    region_start_markers = [None] * num_regions

    # List of start markers for representative regions. 
    region_end_markers = [None] * num_regions

    regionslice = [None] * int(wfactor)

    region_end_marker_relativecount = [None] * num_regions

    # List of the cumulative sum of instructions in the slices.  There is one
    # entry for each slice in the BBV file which contains the total icount up
    # to the end of the slice.
    #
    cumulative_icount = []

    # Cumulative sum of instructions so far
    #
    run_sum = 0

    # Get each slice & generate some data on it.
    #
    slice_num = 0
    while True:
        fv = GetSlice(fp)
        if fv == []:
            break
        # print fv
        previous_marker = current_marker
        current_marker = GetMarker(fp)

        # Get total icount for the basic blocks in this slice
        #
        sum = 0
        for bb in fv:
            count = bb[1]
            sum += count

        # Record the cumulative icount for this slice.
        #
        if sum != 0:
            run_sum += sum
            cumulative_icount += [run_sum]

        # If slice is a representative region, record the basic blocks of the slice.
        #
        if slice_num in slice_set:
            if slice_num > int(wfactor): 
                count = 1 # we already read 1 marker
                regionslice[0] = fv
                while (count < int(wfactor)):
                    fv = GetSlice(fp)

                    # Get total icount for the basic blocks in this slice
                    #
                    sum = 0
                    for bb in fv:
                        bbcount = bb[1]
                        sum += bbcount

                    # Record the cumulative icount for this slice.
                    #
                    if sum != 0:
                        run_sum += sum
                        cumulative_icount += [run_sum]

                    regionslice[count] = fv
                    current_marker = GetMarker(fp)
                    count = count + 1
                marker_index = WarmupRegionToSlice.keys()[WarmupRegionToSlice.values().index(slice_num)]
                # WarmupRegionToSlice maps region/cluster_id to slices
                # marker_index is the cluster_id corresponding to slice_num
                region_start_markers[marker_index] = previous_marker 
                region_end_markers[marker_index] = current_marker 
                count = 0
                startPC = previous_marker['pc']
                endPC = current_marker['pc']
                endPCcount = 0 
                #FIXME : do we need special action if startPC==endPC?
                endPCbbidlist = pcbblist_dict[endPC]
                while (count < int(wfactor)):
                    thisbbv = regionslice[count]
                    for bbidpair in endPCbbidlist:
                        thisitem = [item for item in thisbbv if item[0] == bbidpair[0] ]
                        if not thisitem:
                            break
                        thispair = thisitem[0] 
                        thiscount = thispair[1] 
                        bbidsticount = bbidpair[1] 
                        thisPCcount = thiscount/bbidsticount
                        endPCcount += thisPCcount
                    count = count + 1
                slice_num += int(wfactor)
                region_end_marker_relativecount[marker_index] = endPCcount 
            else:
                slice_num += 1
        else:
            slice_num += 1

    # import pdb;  pdb.set_trace()
    return cumulative_icount, region_start_markers, region_end_markers, region_end_marker_relativecount 

def CheckRegions(RegionToSlice, weight_dict):
    """
    Check to make sure the simpoint and weight files contain the same regions.

    @return no return value
    """

    if len(RegionToSlice) != len(weight_dict) or \
       RegionToSlice.keys() != weight_dict.keys():
        PrintMsg('ERROR: Regions in these two files are not identical')
        PrintMsg('   Simpoint regions: ' + str(RegionToSlice.keys()))
        PrintMsg('   Weight regions:   ' + str(weight_dict.keys()))
        cleanup()
        sys.exit(-1)


def GenRegionCSV(fp_bbv, fp_simp, fp_weight, warmup_factor, pcbblist_dict, sliceCluster, argtid):
    """
    Read in three files (BBV, weights, simpoints) and print to stdout
    a regions CSV file which defines the representative regions.

    @return no return value
    """

    # Read data from weights, simpoints and BBV files.
    # Error check the regions.
    #
    tid = 0
    if argtid is not None: 
        tid = int(argtid)
    weight_dict = GetWeights(fp_weight)
    RegionToSlice, max_region_number = GetSimpoints(fp_simp)
    cumulative_icount, cluster_icount, cluster_slicecount, region_bbv, region_multiplier, region_start_markers, region_end_markers, region_end_markers_relativecount, first_bb_marker = GetRegionBBV(fp_bbv, RegionToSlice, max_region_number, pcbblist_dict, sliceCluster)
    CheckRegions(RegionToSlice, weight_dict)

    total_num_slices = len(cumulative_icount)

    # Print header information
    #
    PrintMsgNoCR('# Regions based on: ')
    for string in sys.argv:
        PrintMsgNoCR(string + ' '),
    PrintMsg('')
    PrintMsg('')
    PrintMsg(
        '# comment,thread-id,region-id,start-pc,start-pc-count,end-pc,end-pc-count,end-pc-relative-count, region-length, region-weight, region-multiplier, region-type')
    PrintMsg('')

    total_icount = 0
    for region in sorted(RegionToSlice.keys()): 
        # Calculate the info for the regions and print it.
        #
        slice_num = RegionToSlice[region]
        weight = weight_dict[region]
        multiplier = 0
        start_marker = region_start_markers[region]
        end_marker = region_end_markers[region]
        end_relativecount = region_end_markers_relativecount[region]
        #import pdb;  pdb.set_trace()
        if slice_num > 0:
            start_icount = cumulative_icount[slice_num - 1] + 1
        else:
            # If this is the first slice, set the initial icount to 0
            #
            start_icount = 0
        end_icount = cumulative_icount[slice_num]
        length = end_icount - start_icount + 1
        total_icount += length
        PrintMsg('# RegionId = %d Slice = %d Icount = %d Length = %d Weight = %.5f Multiplier = %.3f ClusterSlicecount = %d ClusterIcount = %d' % \
            (region + 1, slice_num, start_icount, length, weight, region_multiplier[region], cluster_slicecount[region], cluster_icount[region]))
        PrintMsg('#Start: pc : %s absolute_count: %s ' % (start_marker['pc'], start_marker['count'])); 
        PrintMsg('#End: pc : %s absolute_count: %s  relative_count: %s' % (end_marker['pc'], end_marker['count'],end_relativecount)); 
        PrintMsg('cluster %d from slice %d,%d,%d,%s,%s,%s,%s,%d,%d,%.5f,%.3f,%s\n' % \
            (region, slice_num, tid, region + 1, start_marker['pc'], start_marker['count'], end_marker['pc'], end_marker['count'], end_relativecount, length, weight, region_multiplier[region], "simulation"))


    total_simulationregion_icount =  total_icount
    # Re-open the bbv and simpoint files
    fp_bbv.close()
    fp_bbv = OpenFVFile(args.bbv_file, 'Basic Block Vector (bbv) file: ')
    fp_simp.close()
    fp_simp = OpenSimpointFile(args.region_file, 'simpoints file: ')
    total_icount = 0
    NumSimRegions = max_region_number + 1; #== max cluster id+1, 0-based with gaps
    if warmup_factor is not None: 
        if int(warmup_factor) > 0:
            WarmupRegionToSlice = GetWarmuppoints(fp_simp, warmup_factor)
            cumulative_icount, warmup_region_start_markers, warmup_region_end_markers, warup_region_end_markers_relativecount = GetWarmupRegionBBV(fp_bbv, WarmupRegionToSlice, max_region_number, warmup_factor, pcbblist_dict)

            for wregion in sorted(WarmupRegionToSlice.keys()):
                # Calculate the info for the regions and print it.
                #
                wslice_num = WarmupRegionToSlice[wregion]
                wstart_marker = warmup_region_start_markers[wregion]
                wend_marker = warmup_region_end_markers[wregion]
                wend_relativecount = warup_region_end_markers_relativecount[wregion]
                if wslice_num > 0:
                    start_icount = cumulative_icount[wslice_num - 1] + 1
                else:
                    # If this is the first slice, set the initial icount to 0
                    #
                    start_icount = 0
                if wstart_marker is not None: 
                    end_icount = cumulative_icount[wslice_num]
                    length = end_icount - start_icount + 1
                    total_icount += length
                    PrintMsg('# RegionId = %d Slice = %d Icount = %d Length = %d WarmupFactor = %d ' % \
                    (wregion + NumSimRegions + 1, wslice_num, start_icount, length, int(warmup_factor)))
                    PrintMsg('#Start: pc : %s absolute_count: %s ' % (wstart_marker['pc'], wstart_marker['count'])); 
                    PrintMsg('#End: pc : %s absolute_count: %s  relative_count: %s' % (wend_marker['pc'], wend_marker['count'], wend_relativecount)); 
                    PrintMsg('Warmup for regionid %d,%d,%d,%s,%s,%s,%s,%d,%d,%.5f,%.3f,%s:%d\n' % \
                    (wregion+1, tid, wregion + NumSimRegions + 1, wstart_marker['pc'], wstart_marker['count'], wend_marker['pc'], wend_marker['count'], wend_relativecount, length, 0.0, 0.0, "warmup",wregion+1))
                else:
                    PrintMsg('# No warmup possible for regionid %d with WarmupFactor %d\n' % (wregion+1, int(warmup_factor))); 
        # Print summary statistics
        #
        # import pdb;  pdb.set_trace()
    PrintMsg('# First PC, %s' %
                 (first_bb_marker['pc']))
    PrintMsg('# Total instructions in %d regions = %d' %
                 (len(RegionToSlice), total_simulationregion_icount ))
    PrintMsg('# Total instructions in workload = %d' %
                 cumulative_icount[total_num_slices - 1])
    PrintMsg('# Total slices in workload = %d' % total_num_slices)

############################################################################
#
#  Functions for normalization and projection
#
############################################################################


def cleanup():
    """
    Close all open files and any other cleanup required.

    @return no return value
    """

    if fp_bbv:
        fp_bbv.close()
    if fp_lbl:
        fp_lbl.close()
    if fp_simp:
        fp_simp.close()
    if fp_weight:
        fp_weight.close()

############################################################################

# pcregions.py --bbv_file t.bb --region_file t.simpoints --weight_file t.weights --tid tid > $prefix.llvmpoints.csv
parser = argparse.ArgumentParser()
parser.add_argument("--bbv_file", help="basic block vector file", required=True)
parser.add_argument("--region_file", help="files showing simpoint regions", required=True)
parser.add_argument("--weight_file", help="files showing simpoint weights", required=True)
parser.add_argument("--label_file", help="files showing per slice clusters", required=True)
parser.add_argument("--warmup_factor", help="number of slices in warmup region")
parser.add_argument("--tid", help="triggering thread id")
args = parser.parse_args()
fp_lbl = OpenLabelFile(args.label_file, 'Slice label file: ')
fp_bbv = OpenFVFile(args.bbv_file, 'Basic Block Vector (bbv) file: ')
OutputImageInfo(fp_bbv)
fp_bbv.close()
fp_bbv = OpenFVFile(args.bbv_file, 'Basic Block Vector (bbv) file: ')
sliceCluster = ProcessLabelFile(fp_lbl)
pcbblist_dict = ProcessBlockIdSummary(fp_bbv)
fp_simp = OpenSimpointFile(args.region_file, 'simpoints file: ')
fp_weight = OpenWeightsFile(args.weight_file, 'weights file: ')

#import pdb;  pdb.set_trace()

# re-open the bbv file and summarize "Block id:" records
fp_bbv.close()
fp_bbv = OpenFVFile(args.bbv_file, 'Basic Block Vector (bbv) file: ')

GenRegionCSV(fp_bbv, fp_simp, fp_weight, args.warmup_factor, pcbblist_dict, sliceCluster, args.tid)

cleanup()
sys.exit(0)