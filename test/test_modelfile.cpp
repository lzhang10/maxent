// test ModelFile
#include "minunit.h"
#include <modelfile.hpp>

int tests_run = 0;

using namespace std;
using namespace boost;
using namespace maxent;
typedef ItemMap<string> StringItemMap;

namespace test_me {
    using namespace me;
char*
test_constructor() {
    // creation
    MaxentModelFile f;

    cerr << "no checking for throw yet" << endl;
    /*
    BOOST_CHECK_THROW(f.pred_map(), runtime_error);
    BOOST_CHECK_THROW(f.outcome_map(), runtime_error);
    */

    // empty model
    /*
    shared_ptr<ParamsType> params;
    size_t n_theta;
    shared_array<double> theta;
    BOOST_CHECK_THROW(f.params(params, n_theta, theta), runtime_error);
    */

    return 0;
}

MaxentModelFile* 
load_model(const string& file) {
    MaxentModelFile* f = new MaxentModelFile();
    f->load(file);
    return f;
}

char* 
check_model(MaxentModelFile& f) {
    shared_ptr<PredMapType>    pred_map;
    shared_ptr<OutcomeMapType> outcome_map;
    shared_ptr<ParamsType>     params;
    shared_array<double>       theta;
    size_t n_theta;

    pred_map    = f.pred_map();
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
    mu_assert(theta[param[3].second] == 3.3);
    param = (*params)[1];
    mu_assert(param.size() == 1u);
    mu_assert(param[0].first == 3u);
    mu_assert(theta[param[0].second] == 4.4);
    return 0;
}

char* 
test_load() {
    MaxentModelFile t;
    // BOOST_CHECK_THROW(t.load("no this model"), runtime_error);

    MaxentModelFile* f;
    // load a known model
    f = load_model("data/me_model.txt");
    char* r = check_model(*f);
    delete f;
    return r;
}

char* 
test_save() {
    MaxentModelFile t;
    // BOOST_CHECK_THROW(t.save("no this model", false), runtime_error);

    {
        MaxentModelFile f;
        f.load("data/me_model.txt");
        f.save("data/model_temp", false);

        MaxentModelFile f2;
        f2.load("data/model_temp");
        return check_model(f2);
    }
}

char* 
test_bin_model() {
    MaxentModelFile f;
    f.load("data/me_model.txt");
    f.save("data/model_temp", true);

    MaxentModelFile f2;
    f2.load("data/model_temp");
    return check_model(f2);
}

} // namespace test_me

namespace test_rf {
    using namespace me;
char*
test_constructor() {
    // creation
    RandomFieldModelFile f;

    // BOOST_CHECK_THROW(f.feat_map(), runtime_error);

    /*
    double Z;
    size_t n_theta;
    shared_array<double> theta;
    // error on empty model
    // BOOST_CHECK_THROW(f.params(Z, n_theta, theta), runtime_error);
    */
    return 0;
}

RandomFieldModelFile*
load_model(const string& file) {
    RandomFieldModelFile* f = new RandomFieldModelFile();
    f->load(file);
    return f;
}

char*
check_model(RandomFieldModelFile& f) {
    shared_ptr<FeatMapType> feat_map;
    double                  Z;
    size_t                  n_theta;
    shared_array<double>    theta;

    feat_map = f.feat_map();
    f.params(Z, n_theta, theta);
    mu_assert(Z == 1.0);
    mu_assert(n_theta == 5u);
    mu_assert(feat_map->size() == n_theta);
    mu_assert(feat_map->id("A") == 0u);
    mu_assert(feat_map->id("E") == 4u);
    mu_assert(feat_map->id("F") == feat_map->null_id);

    // test some indiviual paramaters
    mu_assert(theta[0] == 0.0);
    mu_assert(theta[3] == 3.3);
    return 0;
}

char* 
test_load() {
    RandomFieldModelFile t;
    /*
    BOOST_CHECK_THROW(t.load("no this model"), runtime_error);
    */

    RandomFieldModelFile* f;
    // load a known model
    f = load_model("data/rf_model.txt");
    char* r = check_model(*f);
    delete f;
    return r;
}

char* 
test_save() {
    RandomFieldModelFile t;
    /*
    BOOST_CHECK_THROW(t.save("no this model", false), runtime_error);
    */

    {
        RandomFieldModelFile f;
        f.load("data/rf_model.txt");
        f.save("data/model_temp", false);

        RandomFieldModelFile f2;
        f2.load("data/model_temp");
        return check_model(f2);
    }
}

char*
test_bin_model() {
    RandomFieldModelFile f;
    f.load("data/rf_model.txt");
    f.save("data/model_temp", true);

    RandomFieldModelFile f2;
    f2.load("data/model_temp");
    return check_model(f2);
}

} // namespace test_rf

static char * all_tests() {
    mu_run_test(test_me::test_constructor);
    mu_run_test(test_me::test_load );
    mu_run_test(test_me::test_save );
    mu_run_test(test_me::test_bin_model );

    mu_run_test(test_rf::test_constructor );
    mu_run_test(test_rf::test_load );
    mu_run_test(test_rf::test_save );
    mu_run_test(test_rf::test_bin_model );
    return 0;
}

int main(int argc, char **argv) {
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


