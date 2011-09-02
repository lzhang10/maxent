#! /usr/bin/env python
# vi:ts=4:tw=78:shiftwidth=4:expandtab
# vim600:fdm=marker
#/

import sys
#sys.path.insert(0, '../python/build/lib.linux-i686-2.4/')

import maxent.pymaxent as pymaxent

try:
    import maxent.cmaxent as cmaxent
except ImportError, NameError:
    print 'cmaxent not found, C++ python extension will not be tested!'
    cmaxent = None

import unittest

class TestMaxent(unittest.TestCase):
    def test_cmaxent(self):
        "only cmaxent specific routine is tested here"
        if cmaxent is None:
            return
        print 'testing cmaxent'
        m = cmaxent.MaxentModel()
        m.begin_add_event()
        m.add_event(['in'], 'A')
        m.add_event(['in'], 'B')
        m.add_event(['in'], 'C')
        m.add_event([('in', 1.0)], 'D', 2)
        m.end_add_event()
        m.train(15, 'gis', 0, 1E-05)
        print m

        places = 5

        self.assertAlmostEqual(m.eval(['in'], 'A'), 0.2, places)
        self.assertAlmostEqual(m.eval(['in'], 'D'), 0.4, places)

        result = m.eval_all(['in'])
        for x in result:
            if x[0] in ['A', 'B', 'C']:
                self.assertAlmostEqual(x[1], 0.2, places)
                self.assertAlmostEqual(x[1], 0.2, places)
                self.assertAlmostEqual(x[1], 0.2, places)
            else:
                self.assertAlmostEqual(x[1], 0.4, places)

    def test_pymaxent(self):
        "only pymaxent specific routine is tested here"
        print 'testing pymaxent'
        m = pymaxent.MaxentModel()
        m.load('data/me_model2.txt')
        print m

        places = 5
        result = m.eval(['in'])
        for x in result:
            if x[0] in ['A', 'B', 'C']:
                self.assertAlmostEqual(x[1], 0.2, places)
                self.assertAlmostEqual(x[1], 0.2, places)
                self.assertAlmostEqual(x[1], 0.2, places)
            else:
                self.assertAlmostEqual(x[1], 0.4, places)

if __name__ == '__main__':
    unittest.main()
