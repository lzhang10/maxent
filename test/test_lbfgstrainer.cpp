#include "minunit.h"
#include <lbfgstrainer.hpp>
#include <modelfile.hpp>
#include <algorithm>

int tests_run = 0;

using namespace std;
using namespace maxent;

namespace maxent {
    extern int verbose;
}


char* test_constructor() {

    // creation
    LBFGSTrainer t;
    cerr << "current no way to check throw" << endl;
    /*
    BOOST_CHECK_THROW(t.train(), runtime_error);
    BOOST_CHECK_THROW(t.load_training_data("no events", "no model"),
            runtime_error);
    BOOST_CHECK_THROW(t.load_training_data("data/me_gis_train.ev", "no model"),
            runtime_error);
    BOOST_CHECK_THROW(t.load_training_data("no events", "data/me_model.txt"),
            runtime_error);
            */
//    BOOST_CHECK_THROW(t.save_param("no model", false), runtime_error);
//    BOOST_CHECK_THROW(t.save_param("model_temp", false), runtime_error);
    return 0;
}

char* check_events(const vector<Event>& ev) {
    mu_assert(ev.size() == 4u);
    mu_assert(ev[0].m_count == 1u);
    mu_assert(ev[1].m_outcome == 1u);
    mu_assert(ev[2].context_size() == 1u);
    mu_assert(ev[3].m_context[1].first == 1u);
    mu_assert(ev[3].m_context[1].second == 1.0);
    return 0;
}

char* test_load_events() {
    MEEventSpace es;
    load_events_txt("data/me_gis_train.ev", es);
    return check_events(es);
}

//void test_save_events() {
//    vector<Event> ev;
//    BOOST_CHECK_THROW(save_events_txt("tmp.ev", ev), runtime_error);
//    load_events_txt("gis_training.ev", ev);
//    save_events_txt("tmp.ev", ev);
//    vector<Event> ev2;
//    load_events_txt("tmp.ev", ev2);
//    check_events(ev2);
//}

char* test_training() {
    LBFGSTrainer t;
    shared_ptr<MEEventSpace> es(new MEEventSpace);
    load_events_txt("data/me_gis_train.ev", *es);

    MaxentModelFile m;
    m.load("data/me_model.txt");
    shared_ptr<ParamsType> params;
    size_t n_theta;
    shared_array<double> theta;
    shared_array<double> sigma;
    m.params(params, n_theta, theta);
    t.set_training_data(es, params, n_theta, theta, sigma, 4);

    t.train();

    m.set_params(params, n_theta, theta);
    m.save("data/model_temp", false);

    // test training with Gaussian prior
    sigma.reset(new double[n_theta]);
    fill(sigma.get(), sigma.get() + n_theta, 100.0);
    t.set_training_data(es, params, n_theta, theta, sigma, 4);
    t.train();
    m.set_params(params, n_theta, theta);
    m.save("data/model_temp", false);
    return 0;
}

char* test_training2() {
    LBFGSTrainer t;
    shared_ptr<MEEventSpace> es(new MEEventSpace);
    load_events_txt("data/me_gis_train2.ev", *es);

    MaxentModelFile m;
    m.load("data/me_model2.txt");
    shared_ptr<ParamsType> params;
    size_t n_theta;
    shared_array<double> theta;
    shared_array<double> sigma;
    m.params(params, n_theta, theta);
    t.set_training_data(es, params, n_theta, theta, sigma, 4);

    t.train();

    m.set_params(params, n_theta, theta);
    m.save("data/model_temp", false);

    // test training with Gaussian prior
    sigma.reset(new double[n_theta]);
    fill(sigma.get(), sigma.get() + n_theta, 100.0);
    t.set_training_data(es, params, n_theta, theta, sigma, 4);
    t.train();
    m.set_params(params, n_theta, theta);
    m.save("data/model_temp", false);
    return 0;
}

static char * all_tests() {
    mu_run_test(test_constructor);
    mu_run_test(test_load_events);

    // mu_run_test(test_save_events);
    mu_run_test(test_training);
    mu_run_test(test_training2 );
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
