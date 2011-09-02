/*
 * vi:ts=4:shiftwidth=4:expandtab
 * vim600:fdm=marker
 * SWIG binding for python
 * Last Change : 19-Mar-2005.
 */
%define DOCSTRING
"maxent - Python binding for C++ Conditional Maximum Entropy Model.
"
%enddef
%module(docstring=DOCSTRING) cmaxent

%{
#include "maxentmodel.hpp"
%}
%include "std_string.i"

%feature("autodoc",  "0");

namespace maxent {
    using namespace std;

    extern int verbose;  // set this to 0 if you do not want verbose output

    // workaround for new version of SWIG handling of default arguments
    %feature("compactdefaultargs") MaxentModel::add_event;
     
    class MaxentModel {
        public:
            // remove them?
            // typedef me::feature_type feature_type;
            // typedef me::feature_type outcome_type;
            typedef std::string outcome_type;
            typedef std::string feature_type;
            typedef std::vector<pair<feature_type, float> > context_type;

            %typemap (in) context_type& (context_type v) { // {{{
                int len;
                int i;

                if (!PyList_Check($input)) 
                    PyErr_Print();

                len  = PyList_Size($input);
                if (len > 0) {
                    PyObject* x = PyList_GetItem($input, 0);

                    // if this is a tuple of (string, float) {{{
                    if (PyTuple_Check(x) && PyTuple_Size(x) == 2) {
                        PyObject* a;
                        PyObject* b;
                        char* s;
                        double d;
                        for (i = 0; i < len; ++i) {
                            x = PyList_GetItem($input, i);
                            a = PyTuple_GetItem(x, 0);
                            b = PyTuple_GetItem(x, 1); // TODO: use PyTuple_GET_ITEM() for speed
                            assert(a); 
                            assert(b);
                            s = PyString_AsString(a);
                            if (PyErr_Occurred())
                                PyErr_Print();
                            d = PyFloat_AsDouble(b);
                            if (PyErr_Occurred())
                                PyErr_Print();
                            v.push_back(std::make_pair(std::string(s), d));
                        }
                        // }}}

                        // or just a single string, float value is omitted {{{
                } else if (PyString_Check(x)) {
                    char* s;
                    for (i = 0; i < len; ++i) {
                        x = PyList_GetItem($input, i);
                        s = PyString_AsString(x);
                        if (PyErr_Occurred())
                            PyErr_Print();
                        v.push_back(std::make_pair(std::string(s), 1.0));
                    }
                    // }}}

                } else {
                    PyErr_SetString(PyExc_RuntimeError, "invalid context_type argument, should be [(str, float), ...]");
                }
                }

                $1 = &v;
            }// }}}

            %typemap (out) std::vector<pair<outcome_type, double> > { // {{{
                PyObject* tup;
                PyObject* ret = PyList_New($1.size());
                assert(ret);
                for (size_t i = 0; i < $1.size(); ++i) {
                    tup = PyTuple_New(2);
                    assert(tup);
                    if (!tup) {
                        PyErr_SetString(PyExc_RuntimeError, "out of memory in calling PyTuple_New().");
                    }
                    PyTuple_SetItem(tup, 0,
                            PyString_FromString($1[i].first.c_str()));
                    PyTuple_SetItem(tup, 1, PyFloat_FromDouble($1[i].second));
                    PyList_SetItem(ret, i, tup);
                    if (PyErr_Occurred())
                        PyErr_Print();
                }
                $result = ret;
            } // }}}

            %feature("docstring", "Create an empty MaxentModel instance");
            MaxentModel();

            char* __str__() const;

            %feature("docstring", "Load a MaxentModel from a file");
            void load(const string& model);

            %feature("docstring", "
Save current model to a file. 
Parameters: 
model   The filename of the model to save.  
binary  If true, the file is saved in binary format, which is
usually smaller (if compiled with libz) and much faster to
load.");
            void save(const string& model, bool binary = false) const;

            %feature("docstring", "
This method calculates the conditional probability p(y|x) for given x
(context) and y (outcome).

Parameters: 
context  A list of pair (string,  float) indicates names of the contextual
predicates and their values which are to be evaluated together.  
outcome  The outcome label for which the conditional probability is
calculated.  

If only string context is given, their values are assumed to be 1.0

Returns: 
The conditional probability of p(outcome|context).");
            double eval(const context_type& context, const outcome_type& outcome) const;

            %feature("docstring", "
Evaluates a context,  return the most possible outcome y for given context x.");
            outcome_type predict(const context_type& context) const;

            %feature("docstring", "
Signal the begining of adding event (the start of training). 

This method must be called before adding any event to the model. It informs
the model the beginning of training. 

After the last event is added end_add_event() must be called to indicate the
ending of adding events.");
            void begin_add_event();

            %feature("docstring", "
Add an event (context, outcome, count) to current model for training later. 

add_event() should be called after calling begin_add_event(). 

Parameters: 
context  A list of pair (string, float) to indicate the context
predicates and their values (must be >= 0) occured in the event. Feature value
is assumed to be 1.0 if omitted.
outcome  A string indicates the outcome label.  
count  How many times this event occurs in training set. default = 1");
            void add_event(const context_type& context,
                    const outcome_type& outcome,
                    size_t count = 1);

            void add_heldout_event(const context_type& context,
                    const outcome_type& outcome,
                    size_t count = 1);

            %feature("docstring", "
Signal the ending of adding events. 

This method must be called after adding of the last event to inform the model
the ending of the adding events.

Parameters: 
cutoff  Event cutoff,  all events that occurs less than cutoff times will be
discussed. Default = 1 (remain all events). Please note this is different from
the usual sense of *feature cutoff*.");
            void end_add_event(size_t cutoff = 1);

            %feature("docstring", "
Train a ME model using selected training method. 

Parameters: 
iter  Specify how many iterations are need for iterative methods. Default
is 15 iterations. 
method  The training method to use. Can be 'lbfgs' or 'gis'. L-BFGS is used
as the default training method. 
sigma2  Global variance (sigma^2) in Gaussian prior smoothing. Default is 0,  which
turns off Gaussian smoothing. 
tol  Tolerance for detecting model convergence. Read manual for details.
");
            void train(size_t iter = 15, const std::string& method = "lbfgs",
                    double sigma2 = 0.0, // non-zero enables Gaussian prior smoothing
                    double tol = 1E-05);

            %feature("docstring", "
Evaluates a context, return the conditional distribution of given context
as a list of (outcome, probability) pairs. 

This method calculates the conditional probability p(y|x) for each possible
outcome tag y. 

Parameters: 
context  A list of string names of the contextual predicates which are to
be evaluated together. Feature values are assumed to be 1.0 if omitted.
");
            %rename(eval_all) py_eval;
            std::vector<pair<outcome_type, double> > py_eval(const context_type& context) const;
    };


} // namespace maxent

