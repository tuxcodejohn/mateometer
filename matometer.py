#!/usr/bin/python


#Matometer, the matefill detector baseed on aubiopitch.by Paul Brossier 
#Copyright (C) 2011  _john john_atsign_tuxcode_dotorg

#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#or look here: http://www.gnu.org/licenses/gpl-2.0.txt




import sys
from aubio.task import *
from dataclean import dataclean
from mateformeln import  matefill_by_f_aprox2 


usage = "usage: %s [options]* [-i INFILE.wav] " % sys.argv[0]


def parse_args():
    from optparse import OptionParser
    parser = OptionParser(usage=usage)
    parser.add_option("-i","--input", action="store", dest="filename",                    help="input sound file")
    parser.add_option("-m","--mode", action="store", dest="mode", default='mcomb',        help="pitch detection mode [default=mcomb]\  mcomb|yin|fcomb|schmitt")
    parser.add_option("-B","--bufsize", action="store", dest="bufsize", default=None,     help="buffer size [default=2048]") 
    parser.add_option("-H","--hopsize", action="store", dest="hopsize", default=None,     help="overlap size [default=512]") 
    parser.add_option("-t","--threshold", action="store", dest="threshold", default=0.1,  help="pitch threshold (for yin) [default=0.1]") 
    parser.add_option("-T","--thresdif", action="store", dest="thresdif",default=3,       help="runaway value delta threshold [default=4]")
    parser.add_option("-s","--silence", action="store",dest="silence", default=-58,       help="silence threshold [default=-58]") 
    parser.add_option("-D","--delay", action="store", dest="delay" ,                      help="number of seconds frames to take back [default=0]") 
    parser.add_option("-S","--smoothing", action="store",dest="smoothing", default=False, help="use a median filter of N frames [default=0]") 
    parser.add_option("-M","--maximum", action="store",  dest="pitchmax", default=False,  help="maximum pitch value to look for (Hz) [default=20000]") 
    parser.add_option("-l","--minimum", action="store",  dest="pitchmin", default=120,    help="minimum pitch value to look for (Hz) [default=120]") 
    parser.add_option("-v","--verbose", action="store_true",dest="verbose", default=False, help="make lots of noise") 
    parser.add_option("-q","--quiet", action="store_false",dest="verbose", default=False,  help="be quiet (default)" )
    (options, args) = parser.parse_args()
    if not options.bufsize:
	if options.mode == aubio_pitch_yin:     options.bufsize = 1024
	elif options.mode == aubio_pitch_schmitt: options.bufsize = 2048
	elif options.mode == aubio_pitch_mcomb:   options.bufsize = 4096
	elif options.mode == aubio_pitch_fcomb:   options.bufsize = 4096 
	else: options.bufsize = 2048
    if not options.hopsize:
	options.hopsize = float(options.bufsize) / 2
    if not options.filename:
	print "no file name given\n", usage
	sys.exit(1)
    return options, args


if __name__ == '__main__':
    options, args = parse_args()
    filename   = options.filename
    params = taskparams()
    params.samplerate = float(sndfile(filename).samplerate())
    params.hopsize    = int(options.hopsize)
    params.bufsize    = int(options.bufsize)
    params.step       = params.samplerate/float(params.hopsize)
    params.yinthresh  = float(options.threshold)
    params.silence    = float(options.silence)
    params.verbose    = options.verbose
    params.omode      = aubio_pitchm_freq
    if options.smoothing: params.pitchsmooth = int(options.smoothing)
    if options.pitchmax:  params.pitchmax    = int(options.pitchmax)
    if options.pitchmin:  params.pitchmin    = int(options.pitchmin)
    if options.delay: params.pitchdelay = float(options.delay)
    pitch = []
    params.pitchmode  = options.mode
    try:
	filetask = taskpitch(filename,params=params)
	pitch = filetask.compute_all()
	if options.verbose : print pitch
	b = dataclean(pitch,schwelle2=options.thresdif,killneg=True)
	if options.verbose : print "options: " , options
	if options.verbose : print b
	f=  (float(sum(b))/len(b))
    except:
	sys.exit("didn't work. maybe your audio sux :-)")

    print "--> %f Hz"% f
    print "--> fuellung: %f%%"% (matefill_by_f_aprox2(f)*100)



