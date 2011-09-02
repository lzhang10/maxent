#! /usr/bin/env python
# vi:ts=4:tw=78:shiftwidth=4:expandtab
# vim600:fdm=marker
#
# maxent.py  -  A (partial implemented) Maximum Entropy Modeling Toolkit
# in Python. This module only supports loading and using a ME model
# (previously trained with C++ version).
# 
# Copyright (C) 2003 by Zhang Le <ejoy@users.sourceforge.net>
# Begin       : 28-Apr-2003
# Last Change : 12-Mar-2004.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

import sys
import math
import types

exp = math.exp

DBM_MAX = 1.0E+304

verbose = 1

class ItemMap: #{{{
    """
    doc test string {{{
    >>> m = ItemMap()
    >>> len(m)
    0
    >>> m.add('a')
    0
    >>> m.add('a')
    0
    >>> m.add('b')
    1
    >>> len(m)
    2
    >>> m[0]
    'a'
    >>> m[1]
    'b'
    >>> m[2]
    >>>
    }}}
    """
    def __init__(self):
        self.index = [] # store item
        self.dict  = {} # map item to index

    def __str__(self):
        # TODO: avoid using += for speed
        s = '[ItemMap]\n'
        for i in xrange(len(self.index)):
            s += '%d: %s\n' % (i,self.index[i])
        return s

    def __len__(self):
        return len(self.index)

    def __getitem__(self, i):
        if i < 0 or i >= len(self.index):
            return None
        else:
            return self.index[i]
    
    def id(self, item):
        try:
            return self.dict[item]
        except KeyError:
            return None

    def add(self, item):
        if self.dict.has_key(item):
            return self.dict[item]
        else:
            i = len(self.index)
            self.dict[item] = i
            self.index.append(item)
            return i
        #}}}

class MaxentModel:
    """This class implements a (read-only) Conditional Maximum Entropy Model.

       For performance reason, training facility is only provided in C++ module.
    """
    def __init__(self):
        # the row format of paramater array:
        # pred_id  (outcome_id1, param1),..., (outcome_idn, paramn)
        # each pred_id may have multiply outcomes and corresponding params
        self.params = None
        self.pred_map = self.outcome_map = None

    def __str__(self):
        if self.params is None:
            return 'Empty Model (Python Version)'

        n = 0
        for i in xrange(len(self.params)):
            n += len(self.params[i])

        return"""Conditional Maximum Entropy Model (Python Version)
        Number of context predicates  : %d
        Number of outcome             : %d
        Number of paramaters(features): %d""" \
        % (len(self.pred_map), len(self.outcome_map),n)

    def check_modeltype(self, model):
        return 0

    def load(self, model, param = ''):
        """Load a ME model from model file previously saved by Maxent Trainer.

           param is optional if the parameter file is not default .param 
        """

        binary = self.check_modeltype(model)
        if binary:
            raise "binary format not supported yet"
            # load_model_bin(model);
        else:
            self.load_model_txt(model)

    def load_model_txt(self, model):
        #print 'loading txt model from %s' % (model)
        self.pred_map = ItemMap()
        self.outcome_map = ItemMap()
        self.params = []

        f = open(model)

        # skip header comments
        line = f.readline()[:-1]
        if 'txt,maxent' not in line:
            raise """This is pure python version of maxent module, only txt maxent model can be accepted"""
        while line == '' or line[0] == '#':
            line = f.readline()[:-1]

        # read context predicates
        count = int(line)
        for i in range(count):
            line = f.readline()[:-1]
            self.pred_map.add(line)

        # read outcomes 
        line = f.readline()[:-1]
        count = int(line)
        for i in range(count):
            line = f.readline()[:-1]
            self.outcome_map.add(line)

        # read paramaters
        count = len(self.pred_map)
        assert count > 0
        fid = 0
        for i in range(count):
            line = f.readline().split()
            params = []
            for i in range(1, len(line)):
                oid = int(line[i])
                params.append((oid, fid))
                fid += 1
            self.params.append(params)

        # load theta
        theta = []
        n_theta = int(f.readline())
        theta = [0] * n_theta
        for i in range(n_theta):
            theta[i] = float(f.readline())

        # put theta into params
        # TODO: possible speed up?
        for param in self.params:
            for i in range(len(param)):
                param[i] = (param[i][0], theta[param[i][1]])

    def eval(self, context):
        """Evaluates given context and return a outcome distribution.

        i.e. Pr(outcome | context)
        context is a list of string names of the contextual predicates
        contextual predicates which are not seen during training are
        simply dropped off.
        eval() return a list of all possible outcomes with their probabilities:
        [(outcome1, prob1), (outcome2, prob2),...] 
        the return list is sorted on their probabilities in descendant order.
        """

        assert type(context) == types.ListType or type(context) == types.TupleType
        n_outcome = len(self.outcome_map)
        probs = [0.0] * n_outcome
        #outcome_sum = zeros(len(self.outcome_map), float)
        for c in context:
            pid = self.pred_map.id(c)
            if pid is not None:
                param = self.params[pid]
                for j in range(len(param)):
                    probs[param[j][0]] += param[j][1]

        sum = 0.0
        for i in range(n_outcome):
            try:
                probs[i] = exp(probs[i])
            except OverflowError:
                probs[i] = DBL_MAX
            sum += probs[i]

        for i in range(n_outcome):
            probs[i] /= sum
        #TODO: optimize here exp(outcome_sum,outcome_sum) does not work
        outcomes = []
        for i in range(n_outcome):
            outcomes.append((self.outcome_map[i], probs[i]))
        outcomes.sort(lambda x,y: -cmp(x[1], y[1]))
        return outcomes

    def predict(self, context):
        """Evaluates given context and return the most possible outcome y

           This function is a thin wrapper for  eval().
        """
        return self.eval(context)[0][0]

def _test():
    import doctest, pymaxent 
    return doctest.testmod(pymaxent)
           
if __name__ == "__main__":
    _test()
