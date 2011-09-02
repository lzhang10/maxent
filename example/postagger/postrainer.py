#! /usr/bin/env python
# vi:ts=4:tw=78:shiftwidth=4:expandtab
# vim600:fdm=marker
#
# postrainer.py  -  Train A Maximum Entropy model for Part-of-Speech Tagging
# usage:
#
# Copyright (C) 2003 by Zhang Le <ejoy@users.sourceforge.net>
# Begin       : 01-May-2003
# Last Change : 10-Oct-2005.
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
import re
from optparse import OptionParser
import postagger 
from colorize import *
try:
    from maxent import MaxentModel
except ImportError:
    from pymaxent import MaxentModel

re_number = re.compile('[0-9]')
re_hyphen = re.compile('-')
re_uppercase = re.compile('[A-Z]')

feat_dict = {}
tag_dict = {}
word_freq = {}
me = None
rare_freq = 0 # word with frequence < rare_freq will be recarded as rare word
training_data = None

def split_pos(s):
    """
    split out word and pos in s into two separate lists
    """
    w = []
    pos = []
    #for i, t in enumerate(s):
    for i in range(len(s)):
        t = s[i]
        ind = t.rindex('/')
        w.append(t[:ind])
        pos.append(t[ind + 1:])
    return w,pos

def gather_feature(word, context, pos):
    if not is_rare_word(word): # only collect tag dict for common words
        if word in tag_dict:
            if not pos in tag_dict[word]:
                tag_dict[word][pos] = 1
            else:
                tag_dict[word][pos] += 1
        else:
            tag_dict[word] = {pos:1}

    for pred in context:
        f = pred + '_' + pos
        feat_dict[f] = feat_dict.get(f, 0) + 1
#        if f in feat_dict:
#            feat_dict[f] += 1
#        else:
#            feat_dict[f] = 1

def is_rare_word(w):
    assert word_freq
    if word_freq.get(w, 0) < rare_freq:
        return True
    return False

def add_event(word, context, pos):
    context = [c for c in context if c + '_' + pos in feat_dict]
    if context:
        me.add_event(context,pos)

def save_training_data(word, context, pos):
    context = [c for c in context if c + '_' + pos in feat_dict]
    if context:
        print >> training_data, pos, 
        for c in context:
            print >> training_data, c, 
        print >> training_data

def add_heldout_event(word, context, pos):
    context = [c for c in context if c + '-' + pos in feat_dict]
    if context:
        me.add_heldout_event(context,pos)

def gather_word_freq(file):
    assert len(word_freq) == 0
    lines = 0
    for s in file:
        lines += 1
        if lines % 1000 == 0:
            print '%d lines' % lines
        sent = s.split()
        words, pos = split_pos(sent)
        for w in words:
            word_freq[w] = word_freq.get(w, 0) + 1

def get_chars(w):
    return [w[i:i+2] for i in range(0, len(w), 2)]

def extract_feature(file, func):
    """extract special features for rare word if rare_feat is True"""
    assert word_freq

    lines = 0
    for s in file:
        lines += 1
        if lines % 1000 == 0:
            print '%d lines' % lines
        sent = s.split()
        if len(sent) == 0: continue

        words, pos = split_pos(sent)
        n = len(words)
        for i in range(n):
            context = get_context(words, pos, i, word_freq.get(words[i], 0) < rare_freq)
            func(words[i], context, pos[i])


def save_word_freq(filename):
    f = open(filename, 'w')
    for w in word_freq.keys():
        print >> f, w, word_freq[w]

def save_tag_dict(filename):
    f = open(filename,'w')
    for w in tag_dict:
        print >> f, w,
        for pos in tag_dict[w].keys():
            print >> f,pos,
        print >> f

def save_features(filename):
    f = open(filename,'w')
    for feat in feat_dict.keys():
        print >> f,  feat_dict[feat], feat

def cutoff_feature(cutoff, rare_cutoff):
    global feat_dict
    tmp = {}
    for f in feat_dict:
        if f.find("curword=") != -1:
            if feat_dict[f] >= rare_cutoff:
                tmp[f] = feat_dict[f]
        elif feat_dict[f] >= cutoff:
            tmp[f] = feat_dict[f]
    feat_dict = tmp

def main ():
    global feat_dict,me
    # parsing options{{{
    usage = "usage: %prog [options] model"
    parser = OptionParser(usage)
    parser.add_option("-f", "--file", type="string", dest="filename",
                    metavar="FILE",
                    help="train a ME model with data from FILE")
    parser.add_option("--heldout", type = "string" , metavar="FILE", 
            help="use heldout events from FILE")
    parser.add_option("--extract", type = "string", metavar="FILE", 
            help="extract training data to file")
    parser.add_option("--events_out", type="string",
            help="write training(heldout) events to file")
    parser.add_option("-c", "--cutoff", type="int", default=10,
            help="discard feature with frequency < CUTOFF when training\
            [default=10]")
    parser.add_option("-r", "--rare", type="int", default=5, 
            help="use special feature for rare word with frequency < RARE \
            [default=5]")
    parser.add_option("-g", "--gaussian", type="float", default=0.0, 
            help="apply Gaussian penality when training \
            [default=0.0]")
    parser.add_option("-b", "--binary", action="store_true", default=0, 
            help="save events in binary format for fast loading [default=off]")
    parser.add_option("--ev_cutoff", type="int", default=1,
            help="discard event with frequency < CUTOFF when training \
            [default=1]")
    parser.add_option("--iters", type="int", default=15,
                    help="how many iterations are required for training[default=15]")

    parser.add_option("-T","--type",  type="int", default=None, 
            help="choose context type [default for English]")
    (options, args) = parser.parse_args()
    #}}}

    if options.filename:
        file = open(options.filename)
    else:
        print 'training file not given'
        parser.print_usage()
        sys.exit(1)

    if len(args) !=1:
        print >> sys.stderr, 'model name not given'
        parser.print_usage()
        sys.exit(1)
    model_name = args[0]

    global rare_freq
    rare_freq = options.rare

    global get_context
    
    get_context = postagger.choose_context(options.type)

    # First pass: gather word frequency information {{{
    print 'First pass: gather word frequency information'
    gather_word_freq(file)
    print '%d words found in training data' % len(word_freq)
    word_freq_file = options.filename + '.wordfreq'
    print 'Saving word frequence information to %s' % col(word_freq_file,
    'lgreen')
    save_word_freq(word_freq_file)
    print
    # }}}

    # Second pass: gather features and tag dict {{{
    file.seek(0)
    print 'Second pass: gather features and tag dict to be used in tagger'
    print 'feature cutoff:%d' % options.cutoff
    print 'rare word freq:%d' % options.rare
    extract_feature(file, gather_feature)
    print '%d features found' % len(feat_dict)
    print '%d words found in pos dict' % len(tag_dict)
    print 'Applying cutoff %d to features' % options.cutoff
    cutoff_feature(options.cutoff, options.rare)
    print '%d features remained after cutoff' % len(feat_dict)
    feature_file = model_name + '.features'
    print 'saving features to file %s' % feature_file
    save_features(feature_file)
#    tag_dict_file = options.filename + '.tagdict'
#    print 'Saving tag dict to file %s' % (col(tag_dict_file, 'lgreen'))
#    save_tag_dict(tag_dict_file)
    tagdict_file = model_name + '.tagdict'
    print 'Saving tag dict object to %s' % col(tagdict_file, 'lgreen'), 
    import cPickle
    cPickle.dump(tag_dict, open(tagdict_file,'w'))
    print 'done'
    #}}}

    if options.extract:
        global training_data
        training_data = open(options.extract, 'w')
        print 'Saving training data to %s' % options.extract
        file.seek(0)
        extract_feature(file, save_training_data)
        sys.exit(0)

    # Third pass:training ME model...{{{
    print 'Third pass:training ME model...'
    me = MaxentModel()
    me.begin_add_event()
    file.seek(0)
    extract_feature(file, add_event)
    #import profile
    #profile.run('me.end_training()','proflog')
    if options.heldout:
        raise 'not tested'
        print 'adding heldout events from %s' % col(options.heldout, 'yellow')
        extract_feature(open(options.heldout), add_heldout_event, True)
    me.end_add_event(options.ev_cutoff)
    if options.events_out:
        raise 'not tested'
        print 'dumping training events to', col(options.events_out, 'lgreen')
#        import hotshot,  hotshot.stats
#        prof = hotshot.Profile("dump_events.prof", 1)
#        prof.runcall(me.dump_events, options.events_out)
        me.dump_events(options.events_out, options.binary)
        sys.exit(0)

    me.train(options.iters, 'lbfgs', options.gaussian)
    
    print 'training finished'

    print 'saving tagger model to %s' % model_name,
    me.save(model_name)
    print 'done'
    # }}}

if __name__ == "__main__":
    main()

