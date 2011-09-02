#! /usr/bin/env python
# vi:ts=4:tw=78:shiftwidth=4:expandtab
# vim600:fdm=marker
#
# evaltag.py  -  eval tag result
# usage:
#
# Copyright (C) 2003 by Zhang Le <ejoy@users.sourceforge.net>
# Begin       : 22-May-2003
# Last Change : 25-Jul-2003.
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
from optparse import OptionParser
from postrainer import split_pos

class Stat:
    """
    >>> s = Stat()
    >>> s.word('a', 'b', 'c')
    >>> s.word('a', 'b', 'c')
    >>> s.word('a', 'b', 'b)
    >>> s.word_acc()
    0.33333333333333331
    >>> s.stat
    {('a',  'b',  'c'): 2}
    >>>
    """
    def __init__(self):
        self.n_known_word_correct = 0
        self.n_unknown_word_correct = 0
        self.n_known_word_total = 0
        self.n_unknown_word_total = 0
        self.n_sent_correct = 0
        self.n_sent_total = 0
        self.stat = {}

    def word(self, word, correct_tag, proposed_tag):
        known = word in dict
        if known:
            self.n_known_word_total += 1
        else:
            self.n_unknown_word_total += 1

        if correct_tag == proposed_tag:
            if known:
                self.n_known_word_correct += 1
            else:
                self.n_unknown_word_correct += 1
        else:
            st = self.stat
            t = (word, correct_tag, proposed_tag, not known)
            st[t] = st.get(t, 0) + 1

    def sent(self, correct):
        self.n_sent_total += 1
        if correct:
            self.n_sent_correct += 1

    def word_acc(self):
        return float(self.n_known_word_correct + self.n_unknown_word_correct) /\
                (self.n_known_word_total + self.n_unknown_word_total)

    def known_word_acc(self):
        return float(self.n_known_word_correct) / self.n_known_word_total

    def unknown_word_acc(self):
        return float(self.n_unknown_word_correct) / self.n_unknown_word_total

    def sent_acc(self):
        return float(self.n_sent_correct) / self.n_sent_total

    def dump_stat(self, file, cutoff):
        """Dump detail word statistics of tagging result."""
        st = self.stat
        keys = [k for k in st.keys() if st[k] >= cutoff]
        keys.sort(lambda x, y:cmp(st[y], st[x]))
        print >> file, 'freq\t\tcorrect  proposed  unknown word'
        for k in keys:
            word, correct, proposed_tag, unknown = k
            print >> file, '%4d\t%-10s  %2s   %2s     \t %s' % (st[k], word, correct, 
                    proposed_tag, str(unknown))

    def __str__(self):
        return """Statistics of POS result:
Total words: %d\tKnown words: %d\tUnknown words: %d
Total acc: %.2f%%\tKnown acc: %.2f%%\tUnknown acc: %.2f%%
Total sentences: %d\tCorrect sentences: %d\tSent acc:%.2f%%
        """ % (self.n_known_word_total + self.n_unknown_word_total, 
                self.n_known_word_total, self.n_unknown_word_total, 
                self.word_acc()*100, self.known_word_acc()*100, 
                self.unknown_word_acc()*100, 
                self.n_sent_total, self.n_sent_correct, self.sent_acc()*100)
        

stat = Stat()
dict = {}

def eval_sent(s1, s2):
    s1 = split_pos(s1.split())
    s2 = split_pos(s2.split())
    word1, pos1 = s1
    word2, pos2 = s2

    assert len(word1) == len(pos1)
    assert len(word1) == len(word2)
    assert len(pos1) == len(pos2)

    correct = 0
    for i in range(len(word1)):
        w1 = word1[i]
        p1 = pos1[i]
        w2 = word2[i]
        p2 = pos2[i]
        assert w1 == w2

        stat.word(w1, p1, p2)
        if p1 == p2:
            correct += 1
    stat.sent(correct == len(word1))

def main():
    # parsing command line option {{{
    parser = OptionParser()
    parser.add_option("-d", "--dict", type="string",
                    help="use word frequency information from DICT")
    parser.add_option("-s", "--stat", type="int", default=0, 
                    help="dump detail word statistics (only frequency >= STAT) of tagging result")

    (options, args) = parser.parse_args()
    #}}}

    global dict
    if options.dict:
        import cPickle
        dict = cPickle.load(open(options.dict))
    else:
        print >> sys.stderr, 'dict file not given'
        parser.print_help()
        sys.exit(1)


    file_in = sys.stdin
    file_out = sys.stdout

    s = file_in.readline()
    while s:
        s1 = s[:-1]
        s2 = file_in.readline()[:-1]
        s = file_in.readline()[:-1] #skip blank line
        assert s == ''
        eval_sent(s1, s2)
        s = file_in.readline()
    print >> file_out, stat

    if options.stat:
        stat.dump_stat(sys.stdout, options.stat)


if __name__ == '__main__':
    main()

