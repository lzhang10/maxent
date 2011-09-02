// test MaxentModel
// TODO: add test for Gaussian prior
#include "minunit.h"
#include <maxentmodel.hpp>
#include <modelfile.hpp>
#include <trainer.hpp>
#include <math.h>

int tests_run = 0;

using namespace std;
using namespace maxent;
using namespace me;

char* test_constructor() {
    // creation
    MaxentModel m;
    cerr << "testing throw not ready" << endl;
    /* no way to check throw so far
    mu_assert_THROW(m.save("no model"), runtime_error);
    mu_assert_THROW(m.dump_events("no model"), runtime_error);
    mu_assert_THROW(m.train(), runtime_error);
    */
    cout << m.__str__() << endl;
    return 0;
}

char* test_model1(const string& method) {
    MaxentModel m;
    m.begin_add_event();
    vector<string> c;
    c.push_back("in");
    m.add_event(c,"A",1);
    m.add_event(c,"B",1);
    m.add_event(c,"C",1);
    m.add_event(c,"D",2);
    m.add_heldout_event(c,"A",1);
    m.add_heldout_event(c,"B",1);
    m.add_heldout_event(c,"C",1);
    m.add_heldout_event(c,"D",2);
    m.end_add_event();
    cout << m.__str__() << endl;
    m.train(15, method);

    double tol = 1E-03;
    mu_assert(fabs(m.eval(c, "A") - 0.2) < tol);
    mu_assert(fabs(m.eval(c, "C") - 0.2) < tol);
    mu_assert(fabs(m.eval(c, "D") - 0.4) < tol);

    // test save&load
    m.save("data/model_temp");
    MaxentModel m2;
    m2.load("data/model_temp");
    mu_assert(fabs(m2.eval(c, "A") - 0.2) < tol);
    mu_assert(fabs(m2.eval(c, "C") - 0.2) < tol);
    mu_assert(fabs(m2.eval(c, "D") - 0.4) < tol);
    return 0;
}

char* test_model2(const string& method) {
    MaxentModel m;
    m.begin_add_event();
    vector<string> c;
    c.push_back("in");
    m.add_event(c,"A",1);
    m.add_event(c,"B",1);
    m.add_event(c,"C",1);
    m.add_event(c,"D",2);
    c.push_back("out");
    m.add_event(c,"D",2);
    m.end_add_event();
    m.train(300, method);
    m.save("data/model_temp");
    double tol = 1E-02;
    c.pop_back();
    mu_assert(fabs(m.eval(c, "A") - 0.1999)  < tol);
    mu_assert(fabs(m.eval(c, "C") - 0.1999)  < tol);
    mu_assert(fabs(m.eval(c, "D") - 0.4000)  < tol);
    c.push_back("out");
    mu_assert(fabs(m.eval(c, "A") - 0.0)  < tol);
    mu_assert(fabs(m.eval(c, "D") - 0.9999)  < tol);

    // test save&load
    m.save("data/model_temp");
    MaxentModel m2;
    m2.load("data/model_temp");
    c.pop_back();
    mu_assert(fabs(m2.eval(c, "A") - 0.1999)  < tol);
    mu_assert(fabs(m2.eval(c, "C") - 0.1999)  < tol);
    mu_assert(fabs(m2.eval(c, "D") - 0.4000)  < tol);
    c.push_back("out");
    mu_assert(fabs(m2.eval(c, "A") - 1.9e-06)  < tol);
    mu_assert(fabs(m2.eval(c, "D") - 0.9999)  < tol);
    return 0;
}

char* test_model3(const string& method) {
    MaxentModel m;
    m.begin_add_event();
    vector<pair<string, float> > c;
    c.push_back(make_pair("in", 10.0)); // context
    m.add_event(c,"A",1);
    m.add_event(c,"B",1);
    m.add_event(c,"C",1);
    m.add_event(c,"D",2);
    m.end_add_event();
    m.train(50, method);
    double tol = 1E-03;
    mu_assert(fabs(m.eval(c, "A") - 0.2) < tol);
    mu_assert(fabs(m.eval(c, "C") - 0.2) < tol);
    mu_assert(fabs(m.eval(c, "D") - 0.4) < tol);

    // test save&load
    m.save("data/model_temp");
    MaxentModel m2;
    m2.load("data/model_temp");
    mu_assert(fabs(m2.eval(c, "A") - 0.2) < tol);
    mu_assert(fabs(m2.eval(c, "C") - 0.2) < tol);
    mu_assert(fabs(m2.eval(c, "D") - 0.4) < tol);
    return 0;
}

char* test_lbfgs1() { return test_model1("lbfgs"); }
char* test_lbfgs2() { return test_model2("lbfgs"); }
char* test_lbfgs3() { return test_model3("lbfgs"); }

char* test_gis1() { return test_model1("gis"); }
char* test_gis2() { return test_model2("gis"); }
char* test_gis3() { return test_model3("gis"); }
    // test_model3("gis"); // non-binary feature is not ready for gis 

char* check_model(MaxentModelFile& f) {
    shared_ptr<PredMapType>    pred_map;
    shared_ptr<OutcomeMapType> outcome_map;
    shared_ptr<ParamsType> params;
    size_t n_theta;
    shared_array<double> theta;

    pred_map = f.pred_map();
    outcome_map = f.outcome_map();
    f.params(params, n_theta, theta);
    mu_assert(n_theta == 5u);
    mu_assert(pred_map->size() == 2u);
    mu_assert(outcome_map->size() == 4u);
    mu_assert(params->size() == 2u);
    mu_assert(pred_map->id("in") == 0u);
    mu_assert(outcome_map->id("B") == 1u);

    // test some indiviual paramaters
    vector<pair<outcome_id_type,  size_t> > param;
    param = (*params)[0];
    mu_assert(param.size() == 4u);
    mu_assert(param[0].first == 0u);
    mu_assert(theta[param[0].second] == 0.0);
    mu_assert(param[3].first == 3u);
    mu_assert(theta[param[3].second] == 0.0);
    param = (*params)[1];
    mu_assert(param.size() == 1u);
    mu_assert(param[0].first == 3u);
    mu_assert(theta[param[0].second] == 0.0);
    return 0;
}

char* check_events(const MEEventSpace& es) {
    mu_assert(es.size() == 4u);
    mu_assert(es[0].m_count == 1u);
    mu_assert(es[1].m_outcome == 1u);
    mu_assert(es[2].context_size() == 1u);
    mu_assert(es[3].m_context[1].first == 1u);
    mu_assert(es[3].m_context[1].second == 1.0);
    return 0;
}

char* test_dump_events() {
    MaxentModel m;
    m.begin_add_event();
    vector<string> c;
    c.push_back("in");
    m.add_event(c,"A",1);
    m.add_event(c,"B",1);
    m.add_event(c,"C",1);
    c.push_back("out");
    m.add_event(c,"D",2);
    m.end_add_event();
    m.dump_events("data/model_temp");
    MEEventSpace es;
    load_events_txt("data/model_temp.ev", es);
    return check_events(es);
}

static char * all_tests() {
    mu_run_test(test_constructor);
    mu_run_test(test_gis1);
    mu_run_test(test_gis2);
    mu_run_test(test_gis3);
    mu_run_test(test_lbfgs1);
    mu_run_test(test_lbfgs2);
    mu_run_test(test_lbfgs3);
    mu_run_test(test_dump_events);

    return 0;
}

int main(int argc, char **argv) {
    maxent::verbose = 1;
    char *result = all_tests();
    if (result != 0) {
        printf("%s\n", result);
    }
    else {
        printf("ALL TESTS PASSED\n");
    }
    printf("Tests run: %d\n", tests_run);

    return result != 0;
}

