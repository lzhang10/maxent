#! /usr/bin/env python
# vi:ts=4:tw=78:shiftwidth=4:expandtab
# vim600:fdm=marker
# postagger.py  -  A Simple Maximum Entropy Part-of-Speech Tagger
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

import cPickle
import re
from context import *

re_number = re.compile('[0-9]')
re_hyphen = re.compile('-')
re_uppercase = re.compile('[A-Z]')

def choose_context(type = None):
    """Choose context type, default is for English."""
    if type:
        return eval('get_context' + str(type))
    else:
        return get_context_english

def get_prefix_suffix_english(w, length):
    l = min(len(w), length) + 1
    p = []
    s = []
    for i in range(l):
        p.append(w[:i])
        s.append(w[-i:])
    return p, s

def get_context_english(words, pos, i, rare_word):
    """context type for English."""
    'get tag context for words[i]'
    context = []
    w = words[i]
    n = len(words)
    if rare_word:
        prefix, suffix = get_prefix_suffix_english(w, 4)
        for p in prefix:
            context.append('prefix=' + p)
        for s in suffix:
            context.append('suffix=' + s)
        if re_number.search(w):
            context.append('numeric')
        if re_uppercase.search(w):
            context.append('uppercase')
        if re_hyphen.search(w):
            context.append('hyphen')
    else:
        context.append('curword=' + w)

    if i > 0:
        context.append('word-1=' + words[i - 1])
        context.append('tag-1=' + pos[i - 1])
        if i > 1:
            context.append('word-2=' + words[i - 2])
            context.append('tag-1,2=' + pos[i - 2] + ',' + pos[i - 1])
        else:
            context.append('word-2=BOUNDARY')
            context.append('tag-1,2=BOUNDARY,' + pos[0])
    else:
        context.append('word-1=BOUNDARY')
        context.append('word-2=BOUNDARY')
        context.append('tag-1=BOUNDARY')
        context.append('tag-1,2=BOUNDARY,BOUNDARY')


    if i + 1 < n:
        context.append('word+1=' + words[i + 1])
        if i + 2 < n:
            context.append('word+2=' + words[i + 2])
        else:
            context.append('word+2=BOUNDARY')
    else:
        context.append('word+1=BOUNDARY')
        context.append('word+2=BOUNDARY')

    return context

class PosTagger:
    """a Simple Maximum Entropy Part-of-Speech Tagger
    model is a Maximum Entropy model
    optional param dict is a python dict object which maps
    a word to a list of valid POS:
        dict = {'word':[pos1,pos2,...,posn],...}
    provide a dict can speed up the tagging process
    Example:
    >>> class _TrialModel:
    ...     def eval(self, context):
    ...             return [('pos1', 0.7), ('pos2', 0.3)]
    ...
    >>> m = _TrialModel()
    >>> tagger = PosTagger(m)
    >>> tagger.tag_sentence('w1 w2 w3'.split(), 3)
    [['pos1', 'pos1', 'pos1'], ['pos2', 'pos1', 'pos1'], ['pos1', 'pos2', 'pos1']]
    >>>
    }}}
    """

    def __init__(self, model, dict = None, context = None):
        """Create a tagger instance.

           @param model A MaxentModel model instance
           @param dict  Optional tagger dict
           @param context Context type to use, default to English context
        """
        self.model = model
        self.dict = dict
        self.get_context = choose_context(context)

# {{{
#    def get_context(self, words, pos, i):
#        'get tag context for words[i]'
#        context = []
#        w = words[i]
#        n = len(words)
#        if w not in self.dict:
#            prefix, suffix = get_prefix_suffix(w, 4)
#            for p in prefix:
#                context.append('prefix=' + p)
#            for s in suffix:
#                context.append('suffix=' + s)
#            if re_number.search(w):
#                context.append('numeric')
#            if re_uppercase.search(w):
#                context.append('uppercase')
#            if re_hyphen.search(w):
#                context.append('hyphen')
#        else:
#            context.append('curword=' + w)
#
#        if i > 0:
#            context.append('word-1=' + words[i - 1])
#            context.append('tag-1=' + pos[i - 1])
#            if i > 1:
#                context.append('word-2=' + words[i - 2])
#                context.append('tag-1,2=' + pos[i - 2] + ',' + pos[i - 1])
#            else:
#                context.append('word-2=BOUNDARY')
#                context.append('tag-1,2=' + pos[i - 2] + ',BOUNDARY')
#        else:
#            context.append('word-1=BOUNDARY')
#            context.append('word-2=BOUNDARY')
#            context.append('tag-1=BOUNDARY')
#            context.append('tag-1,2=BOUNDARY,BOUNDARY')
#
#
#        if i + 1 < n:
#            context.append('word+1=' + words[i + 1])
#            if i + 2 < n:
#                context.append('word+2=' + words[i + 2])
#            else:
#                context.append('word+2=BOUNDARY')
#        else:
#            context.append('word+1=BOUNDARY')
#            context.append('word+2=BOUNDARY')
#
#        return context


#    def get_special_feature(self, s, i, pos):
#        """
#        get_special_feature() is called to add language specific
#        features. Reimplement get_special_feature() if you want to 
#        add some language specific features
#        """
#        # TODO: subclass for Chinese
#        re_number = re.compile('[0-9]')
#        re_hyphen = re.compile('-')
#        re_uppercase = re.compile('[A-Z]')
#
#        w = s[i]
#        context = []
#        if w not in self.dict:
#            prefix, suffix = get_prefix_suffix(w, 4)
#            for p in prefix:
#                context.append('p' + p)
#            for s in suffix:
#                context.append('s' + s)
#            if re_number.search(w):
#                context.append('f_number')
#            if re_uppercase.search(w):
#                context.append('f_uppercase')
#            if re_hyphen.search(w):
#                context.append('f_hyphen')
#        return context
#}}}

    def tagword(self, s, i, hist ):
        """
        tag word s[i] under given pos history hist
        return a list of (pos, score) pair sorted 
        on score
        get_special_feature() is called to add language specific
        features. Reimplement get_special_feature() if you want to 
        add some language specific features
        """
        #print 'tagging word:' , s, i ,hist
        assert s
        assert len(hist) == i

        context = self.get_context(s, hist, i, (s[i] not in self.dict))
        result = self.model.eval_all(context)
        #TODO:speed optimize
        if self.dict and s[i] in self.dict:
            w = s[i]
            return [x  for x in result \
                if (w in self.dict and  x[0] in self.dict[w]) ]
        else:
            return result

    def tag_sentence1(self, s, N):
        """
        tagging given sentence s and return N best 
        POS sequences scored on the last word (recursively)
        s is a list of words to tag
        """
        n = len(s)
        assert n
        assert N > 0

        if n == 1:
            pos = self.tagword(s, 0, [])
            #return [[x[0]] for x in pos[:N]] #discard score
            return [[x[0]] for x in pos] #discard score
        else:
            # recursively tagging first n-1 words
            # hist = [[pos11, pos12], [pos21, pos22, ...] ...]
            hist = self.tag_sentence(s[:-1], N)
            assert hist

            result = []
            for i in range(len(hist)):
                for pos, score in self.tagword(s, n-1, hist[i]):
                    result.append((i, pos, score))
            #print 'ranking'
            result.sort(lambda x,y: cmp(y[2], x[2]))
            #pp.pprint(result)
            return [hist[ret[0]] + [ret[1]] for ret in result[:N] ]

    def tag_sentence(self, sent, N):
        """
        tagging given sentence s and return N best 
        POS sequences scored on the last word (recursively)
        s is a list of words to tag
        """
        def insert(h, s):
            h.append(s)

        def extract(h):
            return h.pop()

        def advance(tag, sent, i):
            pos = self.tagword(sent, i, tag[0])
            r = []
            for t, score in pos:
                r.append([tag[0] + [t], score * tag[1]])
            return r

        n = len(sent)
        assert N > 0

        s = [[], 1.0]
        h0 = []
        insert(h0, s)

        for i in range(n):
            sz = min(N, len(h0))
            h1 = []
            for j in range(sz):
                r = advance(extract(h0), sent, i)
                for x in r:
                    insert(h1, x)
            h0 = h1
            h0.sort(lambda x,y: cmp(x[1], y[1]))
        return h0[-1][0]

def _test():
    import doctest, postagger 
    return doctest.testmod(postagger)
           
def test_tagger():
    class _TrialModel:
        def eval(self, context):
                return [('pos1', 0.7), ('pos2', 0.3)]

    m = _TrialModel()
    tagger = PosTagger(m)
    print tagger.tag_sentence('w1 w2 w3'.split(), 3)
    #[['pos1', 'pos1', 'pos1'], ['pos2', 'pos1', 'pos1'], ['pos1', 'pos2', 'pos1']]

if __name__ == "__main__":
    #_test()
    test_tagger()
