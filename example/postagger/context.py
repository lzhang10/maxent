#! /usr/bin/env python
# vi:ts=4:tw=78:shiftwidth=4:expandtab
# vim600:fdm=marker
#
# context.py  -  description
# usage:
#
# Copyright (C) 2003 by Zhang Le <ejoy@users.sourceforge.net>
# Begin       : 16-Jun-2003
# Last Change : 16-Jun-2003.
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

def get_prefix_suffix2(w, length):
    l = min(len(w), length*2) # for Chinese
    p = []
    s = []
    for i in range(2, l + 2, 2): # for Chinese
        p.append(w[:i])
        s.append(w[-i:])
    return p, s

def get_context1(words, pos, i, rare_word):
    'get tag context for words[i]'
    context = []
    w = words[i]
    n = len(words)
    if rare_word:
        pass
    else:
        context.append('curword=' + w)

    return context

def get_context2(words, pos, i, rare_word):
    'get tag context for words[i]'
    context = []
    w = words[i]
    n = len(words)
    if rare_word:
        pass
    else:
        context.append('curword=' + w)

    if i > 0:
        context.append('word-1=' + words[i - 1])
    else:
        context.append('word-1=BOUNDARY')

    return context

def get_context3(words, pos, i, rare_word):
    'get tag context for words[i]'
    context = []
    w = words[i]
    n = len(words)
    if rare_word:
        pass
    else:
        context.append('curword=' + w)

    if i > 0:
        context.append('word-1=' + words[i - 1])
        if i > 1:
            context.append('word-2=' + words[i - 2])
        else:
            context.append('word-2=BOUNDARY')
    else:
        context.append('word-1=BOUNDARY')
        context.append('word-2=BOUNDARY')
    return context

def get_context4(words, pos, i, rare_word):
    'get tag context for words[i]'
    context = []
    w = words[i]
    n = len(words)
    if rare_word:
        pass
    else:
        context.append('curword=' + w)


    if i + 1 < n:
        context.append('word+1=' + words[i + 1])
    else:
        context.append('word+1=BOUNDARY')

    return context

def get_context5(words, pos, i, rare_word):
    'get tag context for words[i]'
    context = []
    w = words[i]
    n = len(words)
    if rare_word:
        pass
    else:
        context.append('curword=' + w)

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

def get_context6(words, pos, i, rare_word):
    'get tag context for words[i]'
    context = []
    w = words[i]
    n = len(words)
    if rare_word:
        pass
    else:
        context.append('curword=' + w)

    if i > 0:
        context.append('word-1=' + words[i - 1])
    else:
        context.append('word-1=BOUNDARY')

    if i + 1 < n:
        context.append('word+1=' + words[i + 1])
    else:
        context.append('word+1=BOUNDARY')

    return context

def get_context7(words, pos, i, rare_word):
    'get tag context for words[i]'
    context = []
    w = words[i]
    n = len(words)
    if rare_word:
        pass
    else:
        context.append('curword=' + w)

    if i > 0:
        context.append('word-1=' + words[i - 1])
        if i > 1:
            context.append('word-2=' + words[i - 2])
        else:
            context.append('word-2=BOUNDARY')
    else:
        context.append('word-1=BOUNDARY')
        context.append('word-2=BOUNDARY')


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

def get_context8(words, pos, i, rare_word):
    'get tag context for words[i]'
    context = []
    w = words[i]
    n = len(words)
    if rare_word:
        prefix, suffix = get_prefix_suffix2(w, 1)
        for p in prefix:
            context.append('prefix=' + p)
        for s in suffix:
            context.append('suffix=' + s)
    else:
        context.append('curword=' + w)

    return context

def get_context9(words, pos, i, rare_word):
    'get tag context for words[i]'
    context = []
    w = words[i]
    n = len(words)
    if rare_word:
        prefix, suffix = get_prefix_suffix2(w, 1)
        for p in prefix:
            context.append('prefix=' + p)
        for s in suffix:
            context.append('suffix=' + s)
    else:
        context.append('curword=' + w)

    if i > 0:
        context.append('word-1=' + words[i - 1])
    else:
        context.append('word-1=BOUNDARY')

    if i + 1 < n:
        context.append('word+1=' + words[i + 1])
    else:
        context.append('word+1=BOUNDARY')

    return context

def get_context10(words, pos, i, rare_word):
    'get tag context for words[i]'
    context = []
    w = words[i]
    n = len(words)
    if rare_word:
        prefix, suffix = get_prefix_suffix2(w, 1)
        for p in prefix:
            context.append('prefix=' + p)
        for s in suffix:
            context.append('suffix=' + s)
    else:
        context.append('curword=' + w)

    if i > 0:
        context.append('word-1=' + words[i - 1])
        if i > 1:
            context.append('word-2=' + words[i - 2])
        else:
            context.append('word-2=BOUNDARY')
    else:
        context.append('word-1=BOUNDARY')
        context.append('word-2=BOUNDARY')


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

def get_context11(words, pos, i, rare_word):
    'get tag context for words[i]'
    context = []
    w = words[i]
    n = len(words)
    if rare_word:
        prefix, suffix = get_prefix_suffix2(w, 2)
        for p in prefix:
            context.append('prefix=' + p)
        for s in suffix:
            context.append('suffix=' + s)
    else:
        context.append('curword=' + w)

    return context

def get_context12(words, pos, i, rare_word):
    'get tag context for words[i]'
    context = []
    w = words[i]
    n = len(words)
    if rare_word:
        prefix, suffix = get_prefix_suffix2(w, 2)
        for p in prefix:
            context.append('prefix=' + p)
        for s in suffix:
            context.append('suffix=' + s)
    else:
        context.append('curword=' + w)

    if i > 0:
        context.append('word-1=' + words[i - 1])
    else:
        context.append('word-1=BOUNDARY')

    if i + 1 < n:
        context.append('word+1=' + words[i + 1])
    else:
        context.append('word+1=BOUNDARY')

    return context

def get_context13(words, pos, i, rare_word):
    'get tag context for words[i]'
    context = []
    w = words[i]
    n = len(words)
    if rare_word:
        prefix, suffix = get_prefix_suffix2(w, 2)
        for p in prefix:
            context.append('prefix=' + p)
        for s in suffix:
            context.append('suffix=' + s)
    else:
        context.append('curword=' + w)

    if i > 0:
        context.append('word-1=' + words[i - 1])
        if i > 1:
            context.append('word-2=' + words[i - 2])
        else:
            context.append('word-2=BOUNDARY')
    else:
        context.append('word-1=BOUNDARY')
        context.append('word-2=BOUNDARY')


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

def get_context14(words, pos, i, rare_word):
    'get tag context for words[i]'
    context = []
    w = words[i]
    n = len(words)
    if rare_word:
        pass
    else:
        context.append('curword=' + w)

    if i > 0:
        context.append('tag-1=' + pos[i - 1])
    else:
        context.append('tag-1=BOUNDARY')

    return context

def get_context15(words, pos, i, rare_word):
    'get tag context for words[i]'
    context = []
    w = words[i]
    n = len(words)
    if rare_word:
        pass
    else:
        context.append('curword=' + w)

    if i > 0:
        context.append('tag-1=' + pos[i - 1])
        if i > 1:
            context.append('tag-2=' + pos[i - 2])
        else:
            context.append('tag-2=BOUNDARY')
    else:
        context.append('tag-1=BOUNDARY')
        context.append('tag-2=BOUNDARY')

    return context

def get_context16(words, pos, i, rare_word):
    'get tag context for words[i]'
    context = []
    w = words[i]
    n = len(words)
    if rare_word:
        pass
    else:
        context.append('curword=' + w)

    if i > 0:
        context.append('tag-1=' + pos[i - 1])
        if i > 1:
            context.append('tag-1,2=' + pos[i - 2] + ',' + pos[i - 1])
        else:
            context.append('tag-1,2=BOUNDARY,' + pos[0])
    else:
        context.append('tag-1=BOUNDARY')
        context.append('tag-1,2=BOUNDARY,BOUNDARY')

    return context

def get_context17(words, pos, i, rare_word):
    'get tag context for words[i]'
    context = []
    w = words[i]
    n = len(words)
    if rare_word:
        pass
    else:
        context.append('curword=' + w)

    if i > 0:
        context.append('tag-1=' + pos[i - 1])
        if i > 1:
            context.append('tag-2=' + pos[i - 2])
            context.append('tag-1,2=' + pos[i - 2] + ',' + pos[i - 1])
        else:
            context.append('tag-2=BOUNDARY')
            context.append('tag-1,2=BOUNDARY,' + pos[0])
    else:
        context.append('tag-1=BOUNDARY')
        context.append('tag-1,2=BOUNDARY,BOUNDARY')

    return context

def get_context18(words, pos, i, rare_word):
    'get tag context for words[i]'
    context = []
    w = words[i]
    n = len(words)
    if rare_word:
        pass
    else:
        context.append('curword=' + w)

    if i > 0:
        context.append('word-1=' + words[i - 1])
        context.append('tag-1=' + pos[i - 1])
    else:
        context.append('word-1=BOUNDARY')
        context.append('tag-1=BOUNDARY')

    if i + 1 < n:
        context.append('word+1=' + words[i + 1])
    else:
        context.append('word+1=BOUNDARY')

    return context

def get_context19(words, pos, i, rare_word):
    'get tag context for words[i]'
    context = []
    w = words[i]
    n = len(words)
    if rare_word:
        pass
    else:
        context.append('curword=' + w)

    if i > 0:
        context.append('word-1=' + words[i - 1])
        context.append('tag-1=' + pos[i - 1])
        if i > 1:
            context.append('tag-2=' + pos[i - 2])
        else:
            context.append('tag-2=BOUNDARY')
    else:
        context.append('word-1=BOUNDARY')
        context.append('tag-1=BOUNDARY')

    if i + 1 < n:
        context.append('word+1=' + words[i + 1])
    else:
        context.append('word+1=BOUNDARY')

    return context

def get_context20(words, pos, i, rare_word):
    'get tag context for words[i]'
    context = []
    w = words[i]
    n = len(words)
    if rare_word:
        pass
    else:
        context.append('curword=' + w)

    if i > 0:
        context.append('word-1=' + words[i - 1])
        context.append('tag-1=' + pos[i - 1])
        if i > 1:
            context.append('tag-2=' + pos[i - 2])
            context.append('tag-1,2=' + pos[i - 2] + ',' + pos[i - 1])
        else:
            context.append('tag-2=BOUNDARY')
            context.append('tag-1,2=BOUNDARY,' + pos[0])
    else:
        context.append('word-1=BOUNDARY')
        context.append('tag-1=BOUNDARY')
        context.append('tag-1,2=BOUNDARY,BOUNDARY')

    if i + 1 < n:
        context.append('word+1=' + words[i + 1])
    else:
        context.append('word+1=BOUNDARY')

    return context

def get_context21(words, pos, i, rare_word):
    'get tag context for words[i]'
    context = []
    w = words[i]
    n = len(words)
    if rare_word:
        prefix, suffix = get_prefix_suffix2(w, 1)
        for p in prefix:
            context.append('prefix=' + p)
        for s in suffix:
            context.append('suffix=' + s)
    else:
        context.append('curword=' + w)

    if i > 0:
        context.append('word-1=' + words[i - 1])
        context.append('tag-1=' + pos[i - 1])
    else:
        context.append('word-1=BOUNDARY')
        context.append('tag-1=BOUNDARY')

    if i + 1 < n:
        context.append('word+1=' + words[i + 1])
    else:
        context.append('word+1=BOUNDARY')

    return context

def get_context22(words, pos, i, rare_word):
    'get tag context for words[i]'
    context = []
    w = words[i]
    n = len(words)
    if rare_word:
        prefix, suffix = get_prefix_suffix2(w, 1)
        for p in prefix:
            context.append('prefix=' + p)
        for s in suffix:
            context.append('suffix=' + s)
        context.append('wordlen=' + str(len(w)))
    else:
        context.append('curword=' + w)

    if i > 0:
        context.append('word-1=' + words[i - 1])
        context.append('tag-1=' + pos[i - 1])
    else:
        context.append('word-1=BOUNDARY')
        context.append('tag-1=BOUNDARY')

    if i + 1 < n:
        context.append('word+1=' + words[i + 1])
    else:
        context.append('word+1=BOUNDARY')

    return context

def get_context23(words, pos, i, rare_word):
    'get tag context for words[i]'
    context = []
    w = words[i]
    n = len(words)
    if rare_word:
        prefix, suffix = get_prefix_suffix2(w, 1)
        for p in prefix:
            context.append('prefix=' + p)
        for s in suffix:
            context.append('suffix=' + s)
    else:
        context.append('curword=' + w)

    context.append('wordlen=' + str(len(w)))

    if i > 0:
        context.append('word-1=' + words[i - 1])
        context.append('tag-1=' + pos[i - 1])
    else:
        context.append('word-1=BOUNDARY')
        context.append('tag-1=BOUNDARY')

    if i + 1 < n:
        context.append('word+1=' + words[i + 1])
    else:
        context.append('word+1=BOUNDARY')

    return context

def get_context24(words, pos, i, rare_word):
    'get tag context for words[i]'
    context = []
    w = words[i]
    n = len(words)
    if rare_word:
        prefix, suffix = get_prefix_suffix2(w, 3)
        for p in prefix:
            context.append('prefix=' + p)
        for s in suffix:
            context.append('suffix=' + s)
    else:
        context.append('curword=' + w)

    if i > 0:
        context.append('word-1=' + words[i - 1])
        context.append('tag-1=' + pos[i - 1])
    else:
        context.append('word-1=BOUNDARY')
        context.append('tag-1=BOUNDARY')

    if i + 1 < n:
        context.append('word+1=' + words[i + 1])
    else:
        context.append('word+1=BOUNDARY')

    return context

def get_context25(words, pos, i, rare_word):
    'get tag context for words[i]'
    context = []
    w = words[i]
    n = len(words)
    if rare_word:
        prefix, suffix = get_prefix_suffix2(w, 4)
        for p in prefix:
            context.append('prefix=' + p)
        for s in suffix:
            context.append('suffix=' + s)
    else:
        context.append('curword=' + w)

    if i > 0:
        context.append('word-1=' + words[i - 1])
        context.append('tag-1=' + pos[i - 1])
    else:
        context.append('word-1=BOUNDARY')
        context.append('tag-1=BOUNDARY')

    if i + 1 < n:
        context.append('word+1=' + words[i + 1])
    else:
        context.append('word+1=BOUNDARY')

    return context

def get_context26(words, pos, i, rare_word):
    'get tag context for words[i]'
    context = []
    w = words[i]
    n = len(words)
    if rare_word:
        prefix, suffix = get_prefix_suffix2(w, 1)
        for p in prefix:
            context.append('prefix=' + p)
        for s in suffix:
            context.append('suffix=' + s)
        if i > 1:
            context.append('tag-2=' + pos[i - 2])
            #context.append('tag-1,2=' + pos[i - 2] + ',' + pos[i - 1])
        else:
            context.append('tag-2=BOUNDARY')
            #context.append('tag-1,2=BOUNDARY,' + pos[0])
    else:
        context.append('curword=' + w)

    if i > 0:
        context.append('word-1=' + words[i - 1])
        context.append('tag-1=' + pos[i - 1])
    else:
        context.append('word-1=BOUNDARY')
        context.append('tag-1=BOUNDARY')

    if i + 1 < n:
        context.append('word+1=' + words[i + 1])
    else:
        context.append('word+1=BOUNDARY')

    return context

def get_context27(words, pos, i, rare_word):
    'get tag context for words[i]'
    context = []
    w = words[i]
    n = len(words)
    if rare_word:
        prefix, suffix = get_prefix_suffix2(w, 1)
        for p in prefix:
            context.append('prefix=' + p)
        for s in suffix:
            context.append('suffix=' + s)
    else:
        context.append('curword=' + w)

    context.append('wordlen=' + str(len(w)))

    if i > 0:
        context.append('word-1=' + words[i - 1])
        context.append('tag-1=' + pos[i - 1])
        if i > 1:
            context.append('word-1,2=' + words[i - 2] + ',' + words[i-1])
        else:
            context.append('word-1,2=BOUNDARY,' + words[i-1])
    else:
        context.append('word-1=BOUNDARY')
        context.append('word-1,2=BOUNDARY,BOUNDARY')
        context.append('tag-1=BOUNDARY')

    if i + 1 < n:
        context.append('word+1=' + words[i + 1])
    else:
        context.append('word+1=BOUNDARY')

    return context

def get_context28(words, pos, i, rare_word):
    'get tag context for words[i]'
    context = []
    w = words[i]
    n = len(words)
    if rare_word:
        prefix, suffix = get_prefix_suffix2(w, 1)
        for p in prefix:
            context.append('prefix=' + p)
        for s in suffix:
            context.append('suffix=' + s)
    else:
        context.append('curword=' + w)

    context.append('wordlen=' + str(len(w)))

    if i > 0:
        context.append('word-1=' + words[i - 1])
        context.append('tag-1=' + pos[i - 1])
    else:
        context.append('word-1=BOUNDARY')
        context.append('tag-1=BOUNDARY')

    if i + 1 < n:
        context.append('word+1=' + words[i + 1])
        if i + 2 < n:
            context.append('word+1,2=' + words[i + 1] + ',' + words[i+2])
        else:
            context.append('word+1,2=' + words[i + 1] + ',BOUNDARY')
    else:
        context.append('word+1=BOUNDARY')
        context.append('word+1,2=BOUNDARY,BOUNDARY')

    return context

def get_context29(words, pos, i, rare_word):
    'get tag context for words[i]'
    context = []
    w = words[i]
    n = len(words)
    if rare_word:
        prefix, suffix = get_prefix_suffix2(w, 1)
        for p in prefix:
            context.append('prefix=' + p)
        for s in suffix:
            context.append('suffix=' + s)
    else:
        context.append('curword=' + w)

    context.append('wordlen=' + str(len(w)))

    if i > 0:
        context.append('word-1=' + words[i - 1])
        context.append('word-1,0=' + words[i - 1] + ',' + w)
        context.append('tag-1=' + pos[i - 1])
    else:
        context.append('word-1=BOUNDARY')
        context.append('word-1,0=BOUNDARY,' + w)
        context.append('tag-1=BOUNDARY')

    if i + 1 < n:
        context.append('word+1=' + words[i + 1])
    else:
        context.append('word+1=BOUNDARY')

    return context

def get_context30(words, pos, i, rare_word):
    'get tag context for words[i]'
    context = []
    w = words[i]
    n = len(words)
    if rare_word:
        prefix, suffix = get_prefix_suffix2(w, 1)
        for p in prefix:
            context.append('prefix=' + p)
        for s in suffix:
            context.append('suffix=' + s)
    else:
        context.append('curword=' + w)

    context.append('wordlen=' + str(len(w)))

    if i > 0:
        context.append('word-1=' + words[i - 1])
        context.append('tag-1=' + pos[i - 1])
    else:
        context.append('word-1=BOUNDARY')
        context.append('tag-1=BOUNDARY')

    if i + 1 < n:
        context.append('word+1=' + words[i + 1])
        context.append('word0,+1=' + w + ',' + words[i + 1])
    else:
        context.append('word+1=BOUNDARY')
        context.append('word0,+1=' + w + ',BOUNDARY')

    return context

def get_context31(words, pos, i, rare_word):
    'get tag context for words[i]'
    context = []
    w = words[i]
    n = len(words)
    if rare_word:
        prefix, suffix = get_prefix_suffix2(w, 1)
        for p in prefix:
            context.append('prefix=' + p)
        for s in suffix:
            context.append('suffix=' + s)
    else:
        context.append('curword=' + w)

    context.append('wordlen=' + str(len(w)))

    if i > 0:
        context.append('word-1=' + words[i - 1])
        context.append('tag-1=' + pos[i - 1])
    else:
        context.append('word-1=BOUNDARY')
        context.append('tag-1=BOUNDARY')

    if i + 1 < n:
        context.append('word+1=' + words[i + 1])
        if i > 0:
            context.append('tag-1,word+1=' + pos[i-1] + ',' + words[i + 1])
        else:
            context.append('tag-1,word+1=BOUNDARY,' + words[i + 1])
    else:
        context.append('word+1=BOUNDARY')
        context.append('tag-1,word+1=BOUNDARY,BOUNDARY')

    return context

def get_context32(words, pos, i, rare_word):
    'get tag context for words[i]'
    context = []
    w = words[i]
    n = len(words)
    if rare_word:
        prefix, suffix = get_prefix_suffix2(w, 1)
        for p in prefix:
            context.append('prefix=' + p)
        for s in suffix:
            context.append('suffix=' + s)
    else:
        context.append('curword=' + w)

    context.append('wordlen=' + str(len(w)))

    if i > 0:
        context.append('word-1=' + words[i - 1])
        context.append('tag-1=' + pos[i - 1])
        if i > 1:
            context.append('word-1,2=' + words[i - 2] + ',' + words[i-1])
        else:
            context.append('word-1,2=BOUNDARY,' + words[i-1])
    else:
        context.append('word-1=BOUNDARY')
        context.append('word-1,2=BOUNDARY,BOUNDARY')
        context.append('tag-1=BOUNDARY')

    if i + 1 < n:
        context.append('word+1=' + words[i + 1])
        if i + 2 < n:
            context.append('word+1,2=' + words[i + 1] + ',' + words[i+2])
        else:
            context.append('word+1,2=' + words[i + 1] + ',BOUNDARY')
    else:
        context.append('word+1=BOUNDARY')
        context.append('word+1,2=BOUNDARY,BOUNDARY')

    return context

