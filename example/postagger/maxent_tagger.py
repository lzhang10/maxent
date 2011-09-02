#! /usr/bin/env python
# vi:ts=4:tw=78:shiftwidth=4:expandtab
# vim600:fdm=marker
#
# maxent_tagger.py  -  a simple command line Part-of-Speech tagger
# usage:
#
# Copyright (C) 2003 by Zhang Le <ejoy@users.sourceforge.net>
# Begin       : 03-May-2003
# Last Change : 12-Mar-2004.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with this program.
#/

import sys

import cPickle
from optparse import OptionParser
from postrainer import split_pos
import postagger
try:
    from maxent import MaxentModel
except ImportError:
    from pymaxent import MaxentModel

def tag_file(tagger, filein, fileout, test):
    for sent in filein:
        s = sent.split()
        if len(s) == 0: continue

        if test:
            print >> fileout, sent[:-1]
            words, t = split_pos(sent.split())
        else:
            words = sent.split()

        tag = tagger.tag_sentence(words, 5)
        assert (len(words) == len(tag))
        #for i, w in enumerate(words):
        for i in range(len(words)):
            w = words[i]
            fileout.write('%s/%s ' % (w, tag[i]))
        print >> fileout
        print >> fileout


def main ():
    usage = "usage: %prog [options] -m model file"
    parser = OptionParser(usage)
    parser.add_option("-o", "--output", type="string",
            help="write tagged result to OUTPUT")
    parser.add_option("-m", "--model", type="string", 
            help="load trained model from MODEL")
    parser.add_option("-t", "--test", action="store_true",
            default=0, help="test mode, include original tag in output")
    parser.add_option("-v", "--verbose",
                    action="store_true", dest="verbose", default=1)
    parser.add_option("-q", "--quiet",
                    action="store_false", dest="verbose")
    parser.add_option("-T","--type",  type="int", default=None, 
            help="choose context type")

    (options, args) = parser.parse_args()

    if not options.model:
        print >> sys.stderr, 'Tagger model name not given!'
        parser.print_usage()
        sys.exit(1)

    model = options.model
    tag_dict = cPickle.load(open(model + '.tagdict'))

    me = MaxentModel()
    me.load(model)
    tagger = postagger.PosTagger(me, tag_dict, options.type)

    tag_in_file = sys.stdin
    if len(args) >=1:
        tag_in_file = open(args[0])

    tag_out_file = sys.stdout
    if options.output:
        tag_out_file = open(out, 'w')

    tag_file(tagger, tag_in_file, tag_out_file, options.test)

if __name__ == "__main__":
    main()

