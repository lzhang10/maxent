# try to use C++ version of maxent module if possible
# XXX: I do not know how to set/get variable "verbose" in the natural way
# so use two functions here.
try:
    import cmaxent
    MaxentModel = cmaxent.MaxentModel
    def verbose():
        return cmaxent.cvar.verbose
    def set_verbose(x):
        cmaxent.cvar.verbose = x
except ImportError:
    import sys
    import pymaxent
    print >> sys.stderr, 'cmaxent module not found, fall back to python implementation.'
    MaxentModel = pymaxent.MaxentModel
    def verbose():
        return pymaxent.verbose
    def set_verbose(x):
        pymaxent.verbose = x

__all__ = ['MaxentModel', 'set_verbose', 'verbose']
