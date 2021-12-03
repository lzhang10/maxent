# try to use C++ version of maxent module if possible
# XXX: I do not know how to set/get variable "verbose" in the natural way
# so use two functions here.
try:
    from . import cmaxent
    MaxentModel = cmaxent.MaxentModel
    def verbose():
        return cmaxent.cvar.verbose
    def set_verbose(x):
        cmaxent.cvar.verbose = x
except ImportError:
    import sys
    from . import pymaxent
    print('cmaxent module not found, fall back to python implementation.', file=sys.stderr)
    MaxentModel = pymaxent.MaxentModel
    def verbose():
        return pymaxent.verbose
    def set_verbose(x):
        pymaxent.verbose = x

__all__ = ['MaxentModel', 'set_verbose', 'verbose']
