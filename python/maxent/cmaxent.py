# This file was created automatically by SWIG.
# Don't modify this file, modify the SWIG interface instead.
# This file is compatible with both classic and new-style classes.

"""
maxent - Python binding for C++ Conditional Maximum Entropy Model.

"""

import _cmaxent

def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "this"):
        if isinstance(value, class_type):
            self.__dict__[name] = value.this
            if hasattr(value,"thisown"): self.__dict__["thisown"] = value.thisown
            del value.thisown
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static) or hasattr(self,name) or (name == "thisown"):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError,name

import types
try:
    _object = types.ObjectType
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0
del types


class MaxentModel(_object):
    """Proxy of C++ MaxentModel class"""
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, MaxentModel, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, MaxentModel, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ maxent::MaxentModel instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def __init__(self, *args):
        """
        __init__(self) -> MaxentModel

        Create an empty MaxentModel instance
        """
        _swig_setattr(self, MaxentModel, 'this', _cmaxent.new_MaxentModel(*args))
        _swig_setattr(self, MaxentModel, 'thisown', 1)
    def __str__(*args): 
        """
        __str__(self) -> char

        Create an empty MaxentModel instance
        """
        return _cmaxent.MaxentModel___str__(*args)

    def load(*args): 
        """
        load(self, model)

        Load a MaxentModel from a file
        """
        return _cmaxent.MaxentModel_load(*args)

    def save(*args): 
        """
        save(self, model, binary=False)
        save(self, model)

        Save current model to a file. 
        Parameters: 
        model   The filename of the model to save.  
        binary  If true, the file is saved in binary format, which is
        usually smaller (if compiled with libz) and much faster to
        load.
        """
        return _cmaxent.MaxentModel_save(*args)

    def eval(*args): 
        """
        eval(self, context, outcome) -> double

        This method calculates the conditional probability p(y|x) for given x
        (context) and y (outcome).

        Parameters: 
        context  A list of pair (string,  float) indicates names of the contextual
        predicates and their values which are to be evaluated together.  
        outcome  The outcome label for which the conditional probability is
        calculated.  

        If only string context is given, their values are assumed to be 1.0

        Returns: 
        The conditional probability of p(outcome|context).
        """
        return _cmaxent.MaxentModel_eval(*args)

    def predict(*args): 
        """
        predict(self, context) -> outcome_type

        Evaluates a context,  return the most possible outcome y for given context x.
        """
        return _cmaxent.MaxentModel_predict(*args)

    def begin_add_event(*args): 
        """
        begin_add_event(self)

        Signal the begining of adding event (the start of training). 

        This method must be called before adding any event to the model. It informs
        the model the beginning of training. 

        After the last event is added end_add_event() must be called to indicate the
        ending of adding events.
        """
        return _cmaxent.MaxentModel_begin_add_event(*args)

    def add_event(*args): 
        """
        add_event(self, context, outcome, count=1)

        Add an event (context, outcome, count) to current model for training later. 

        add_event() should be called after calling begin_add_event(). 

        Parameters: 
        context  A list of pair (string, float) to indicate the context
        predicates and their values (must be >= 0) occured in the event. Feature value
        is assumed to be 1.0 if omitted.
        outcome  A string indicates the outcome label.  
        count  How many times this event occurs in training set. default = 1
        """
        return _cmaxent.MaxentModel_add_event(*args)

    def add_heldout_event(*args): 
        """
        add_heldout_event(self, context, outcome, count=1)
        add_heldout_event(self, context, outcome)

        Add an event (context, outcome, count) to current model for training later. 

        add_event() should be called after calling begin_add_event(). 

        Parameters: 
        context  A list of pair (string, float) to indicate the context
        predicates and their values (must be >= 0) occured in the event. Feature value
        is assumed to be 1.0 if omitted.
        outcome  A string indicates the outcome label.  
        count  How many times this event occurs in training set. default = 1
        """
        return _cmaxent.MaxentModel_add_heldout_event(*args)

    def end_add_event(*args): 
        """
        end_add_event(self, cutoff=1)
        end_add_event(self)

        Signal the ending of adding events. 

        This method must be called after adding of the last event to inform the model
        the ending of the adding events.

        Parameters: 
        cutoff  Event cutoff,  all events that occurs less than cutoff times will be
        discussed. Default = 1 (remain all events). Please note this is different from
        the usual sense of *feature cutoff*.
        """
        return _cmaxent.MaxentModel_end_add_event(*args)

    def train(*args): 
        """
        train(self, iter=15, method="lbfgs", sigma2=0.0, tol=1E-05)
        train(self, iter=15, method="lbfgs", sigma2=0.0)
        train(self, iter=15, method="lbfgs")
        train(self, iter=15)
        train(self)

        Train a ME model using selected training method. 

        Parameters: 
        iter  Specify how many iterations are need for iterative methods. Default
        is 15 iterations. 
        method  The training method to use. Can be 'lbfgs' or 'gis'. L-BFGS is used
        as the default training method. 
        sigma2  Global variance (sigma^2) in Gaussian prior smoothing. Default is 0,  which
        turns off Gaussian smoothing. 
        tol  Tolerance for detecting model convergence. Read manual for details.

        """
        return _cmaxent.MaxentModel_train(*args)

    def eval_all(*args): 
        """
        eval_all(self, context) -> std::vector<(pair<(maxent::MaxentModel::outcome_type,double)>)>

        Evaluates a context, return the conditional distribution of given context
        as a list of (outcome, probability) pairs. 

        This method calculates the conditional probability p(y|x) for each possible
        outcome tag y. 

        Parameters: 
        context  A list of string names of the contextual predicates which are to
        be evaluated together. Feature values are assumed to be 1.0 if omitted.

        """
        return _cmaxent.MaxentModel_eval_all(*args)

    def __del__(self, destroy=_cmaxent.delete_MaxentModel):
        """__del__(self)"""
        try:
            if self.thisown: destroy(self)
        except: pass


class MaxentModelPtr(MaxentModel):
    def __init__(self, this):
        _swig_setattr(self, MaxentModel, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, MaxentModel, 'thisown', 0)
        _swig_setattr(self, MaxentModel,self.__class__,MaxentModel)
_cmaxent.MaxentModel_swigregister(MaxentModelPtr)
cvar = _cmaxent.cvar


