#! /usr/bin/env python
# vi:ts=4:tw=78:shiftwidth=4:expandtab
# vim600:fdm=marker
#
# orngMaxent.py  -  Python interface of the C++ MaxEnt for Orange lib
#
# Copyright (C) 2004 by Zhang Le <ejoy@users.sourceforge.net>
# Begin       : 01-Nov-2004
# Last Change : 11-Jan-2005.
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
#
# Brief usage (see unittests below):
#    // load data
#    data = orange.ExampleTable("voting")
#
#    // build a learner, specify training data and training parameters 
#    classifier = MaxentLearner(data, iters = 10)
#
#    // do prediction on the ith data
#    // way 1: return the most possible class label
#    c = classifier(data[i])
#
#    // way 2: return probability distribution for all class labels
#    // p[0] is the probability of the first class in data.domain.classVar.values
#    // p[1] is the probability of the second class,  and so on
#    p = classifier(data[i], orange.GetProbabilities)
#
#    // way 3: return a tuple of the most possible class label and its probability
#    r = classifier(data[i], orange.GetBoth)
#
#    // Finally, if you want verbose message during training, just call set_verbose:
#    set_verbose(1)


try:
    from maxent import *
except ImportError:
    import sys
    print >> sys.stderr, 'maxent module not found, get it from homepages.inf.ed.ac.uk/s0450736/maxent_toolkit.html'
    sys.exit(-1)

import orange

# extract features from an orange example
# return a list of features
def extract_features(ex):
    f = []
    for i, a in enumerate(ex.domain.attributes):
        f.append('%s=%s' % (a.name, ex[i]))
    return f

def MaxentLearner(examples=None, **kwds):
    learner = apply(MaxentLearnerClass,(), kwds)
    if examples:
        return learner(examples)
    else:
        return learner

class MaxentLearnerClass:
    def __init__(self, name='Maximum Entropy Learner', 
            iters = 15, method = 'lbfgs', gaussian = 0.0):
        self.name = name
        self.iters = iters
        assert method == 'lbfgs' or method == 'gis'
        self.method = method
        self.gaussian = gaussian

    def __call__(self, data, weight=None):

        # we will ignore the weight 
        # build the me model here
        m = MaxentModel()
        m.begin_add_event()
        for ex in data:
            m.add_event(extract_features(ex), ex.getclass().value)
        m.end_add_event()
        m.train(self.iters, self.method, self.gaussian)
        return MaxentClassifier(model = m, domain = data.domain)

class MaxentClassifier:
    def __init__(self, **kwds):
        self.__dict__ = kwds

    def __call__(self, example, result_type = orange.GetValue):
        if result_type == orange.GetValue:
            return orange.Value(self.domain.classVar, self.model.predict(extract_features(example)))
        else:
            # build a label map, which will be used to sort the outputted
            # probabilities
            class_map = {}
            for pos, label in enumerate(self.domain.classVar.values):
                class_map[label] = pos
            result = self.model.eval_all(extract_features(example))
            if len(result) > 0:
                if result_type == orange.GetProbabilities:
                    r = [None]*len(result)
                    for label, prob in result:
                        r[class_map[label]] = prob
                    return r
                elif result_type == orange.GetBoth:
                    return (orange.Value(self.domain.classVar, result[0][0]), result[0][1])
            else:
                return None

if __name__ == '__main__':
    import unittest
    class TestOrngMaxent(unittest.TestCase):
        def setUp(self):
            set_verbose(1)
            self.data = orange.ExampleTable("voting")
            self.classifier = MaxentLearner(self.data, iters = 10)
            #self.classifier = orange.MaxentClassifier(data)

        def test_predict_class(self):
            for i in range(5):
                c = self.classifier(self.data[i])
                print "original",  self.data[i].getclass(),  "classified as",  c 
            self.assertEqual(self.data[i].getclass(), c)

        def test_predict_prob(self):
            print "Possible classes:",  self.data.domain.classVar.values 
            print "Probabilities for democrats:"

            for i in range(5):
                p = self.classifier(self.data[i], orange.GetProbabilities)
                print "%d: %5.3f (originally %s)" % (i+1, p[1],  self.data[i].getclass())
                self.assertAlmostEqual(p[1], self.data[i].getclass() == \
                        'democrat' and 1.0 or 0.0, 2)

        def test_predict_both(self):
            for i in range(5):
                r = self.classifier(self.data[i], orange.GetBoth)
                self.assertEqual(r[0], self.data[i].getclass())
                self.assertAlmostEqual(r[1], 1.0, 2)

    print 'running unittest...'
    unittest.main()
