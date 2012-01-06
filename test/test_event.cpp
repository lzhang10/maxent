// test events
#include "minunit.h"
#include <meevent.hpp>
#include <rfevent.hpp>
#include <iostream>

int tests_run = 0;

using namespace std;
using namespace maxent;

namespace test_me {
    using namespace me;
typedef Event::context_type context_type;

char* test_event() {
    Event ev;
    mu_assert(ev.m_context == (context_type*)0);
    mu_assert(ev.context_size() == 0u);
    mu_assert(ev.m_outcome == 0u);
    mu_assert(ev.m_count == 0u);

    mu_assert((ev < ev) == false);
    mu_assert(ev == Event());

    context_type context1;
    context1.first = 3u;
    context1.second = 1.0;
    Event ev2(&context1,1, 2);
    ev2.set_outcome(1);
    mu_assert(ev2.context_size() == 1u);
    mu_assert(ev2.m_context[0].first == 3u);
    mu_assert(ev2.m_context[0].second == 1.0);
    mu_assert(ev2.m_outcome == 1u);
    mu_assert(ev2.m_count == 2u);

    mu_assert(ev < ev2);

    context_type context2;
    context2.first = 3u;
    context2.second = 1.0;
    Event ev3(&context2, 1, 3);
    ev3.set_outcome(1);
    mu_assert(ev2 == ev3);
    mu_assert(ev2.is_same_context(ev3));

    context_type context3;
    context1.first = 3u;
    context1.second = 1.0;
    Event ev4(&context3,1, 3);
    ev3.set_outcome(0);
    mu_assert(ev3 > ev4);
    mu_assert(ev < ev4);

    return 0;
}

char* 
test_event_space() {
    MEEventSpace es;
    assert(es.feat_map());
    assert(es.outcome_map());

    mu_assert(es.newfeat_mode() == true);

    vector<pair<std::string, float> > context;
    context.push_back(make_pair("A", 1.0));
    context.push_back(make_pair("B", 2.0));
    context.push_back(make_pair("C", 3.0));
    es.add_event(context, 1, "O1");
    mu_assert(es.size() == 1u);
    es.add_event(context, 1, "O2");
    mu_assert(es.size() == 2u);
    es.add_event(context, 1, "O1");
    mu_assert(es.size() == 3u);
    es.merge_events(1);
    mu_assert(es.size() == 2u);

    MEEventSpace es2(es.feat_map(), es.outcome_map());
    mu_assert(es2.newfeat_mode() == false);
    mu_assert(es2.feat_map()->size() == 3u);
    mu_assert(es2.outcome_map()->size() == 2u);

    return 0;
}

} // namespace test_me

namespace test_rf {
    using namespace rf;
typedef Event::context_type context_type;

char* test_event() {
    Event ev;
    mu_assert(ev.m_context == (context_type*)0);
    mu_assert(ev.context_size() == 0u);
    mu_assert(ev.m_count == 0u);
    mu_assert(ev.m_prior == 1.0);

    mu_assert((ev < ev) == false);
    mu_assert(ev == Event());

    context_type context1;
    context1.first = 3u;
    context1.second = 1.0;
    Event ev2(&context1,1, 2);
    ev2.set_prior(3.0);
    mu_assert(ev2.context_size() == 1u);
    mu_assert(ev2.m_context[0].first == 3u);
    mu_assert(ev2.m_context[0].second == 1.0);
    mu_assert(ev2.m_count == 2u);
    mu_assert(ev2.m_prior == 3.0);

    mu_assert(ev < ev2);

    context_type context2;
    context2.first = 3u;
    context2.second = 1.0;
    Event ev3(&context2,1, 1);
    ev3.set_prior(3.0);
    mu_assert(ev2 == ev3);
    mu_assert(ev2.is_same_context(ev3));

    return 0;
}

// this one should be the last to call. it may hang
char* test_event_space_destory() {
    {
        RFEventSpace es;
        es.push_back(Event());
        es.push_back(Event());
        es.push_back(Event());

        context_type* context1 = new context_type;
        context1->first = 3u;
        context1->second = 1.0;
        Event ev1(context1,1, 2);
        es.push_back(ev1);
    }
    {
        RFEventSpace es;
        context_type* context1 = new context_type;
        context1->first = 3u;
        context1->second = 1.0;
        Event ev1(context1,1, 2);
        es.push_back(ev1);
        /*
         * this test will cause segfault on some platform, so disabled here.
        es.push_back(ev1);
        es.push_back(ev1);
        cout << "*INFO* Two warnings on free() should be printed here (but not always, it depends on your libc)." << endl;
        cout << "*INFO* Since we are freeing some wrong memory, you may (or may not) hang or abort. " << endl;
        cout << "*INFO* In case you hangs, just press CTRL-C." << endl;
        cout << endl;
        // test_event in free(): warning: chunk is already free
        // test_event in free(): warning: chunk is already free
        */
    }

    return 0;
}

char* test_event_space() {
    RFEventSpace es;
    assert(es.feat_map());
    assert(es.feat_map());

    mu_assert(es.newfeat_mode() == true);

    vector<pair<std::string, float> > context;
    context.push_back(make_pair("A", 1.0));
    context.push_back(make_pair("B", 2.0));
    context.push_back(make_pair("C", 3.0));
    es.add_event(context, 1, 2.0);
    mu_assert(es.size() == 1u);
    es.add_event(context, 1, 2.0);
    mu_assert(es.size() == 2u);
    es.merge_events(1);
    mu_assert(es.size() == 1u);

    RFEventSpace es2(es.feat_map());
    mu_assert(es2.newfeat_mode() == false);

    return 0;
}

} // namespace test_rf

static char * all_tests() {
    mu_run_test(test_me::test_event );
    mu_run_test(test_me::test_event_space);

    mu_run_test(test_rf::test_event );
    mu_run_test(test_rf::test_event_space);
    mu_run_test(test_rf::test_event_space_destory );
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


