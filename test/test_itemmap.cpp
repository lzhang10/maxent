// test ItemMap
#include "minunit.h"
#include <itemmap.hpp>
#include <string.h>

int tests_run = 0;


using namespace std;
typedef ItemMap<string> StringItemMap;

template <typename T>
char* test_constructor() {

    // creation
    T m;
    mu_assert(m.size() == 0u);
    mu_assert((int)T::null_id == -1);

    // mu_assert_THROW(m[0])
    mu_assert(m.has_item("A") == false);
    mu_assert(m.id("A") == T::null_id);
    mu_assert(m.id("A") == m.null_id);

    // assignment
    T m2 = m;
    mu_assert(m2.size() == 0u);

    T m3;
    m3 = m2;
    mu_assert(m3.size() == 0u);

    return 0;
}

char* test_constructors() {
    char* a = test_constructor<StringItemMap>();
    return a;
}

template <typename T>
char* test_operation() {

    T m;
    mu_assert(m.add("A") == 0u);
    mu_assert(m.size() == 1u);

    m.clear();

    mu_assert(m.size() == 0u);
    mu_assert(m.size() == 0u);
    mu_assert(m.add("A") == 0u);
    mu_assert(m.size() == 1u);
    mu_assert(m.add("B") == 1u);
    mu_assert(m.size() == 2u);
    mu_assert(m.add("C") == 2u);
    mu_assert(m.size() == 3u);
    mu_assert(m.add("C") == 2u);
    mu_assert(m.size() == 3u);

    mu_assert(m[0] == "A");
    mu_assert(m[1] == "B");
    mu_assert(m[2] == "C");

    mu_assert(m.id("A") == 0u);
    mu_assert(m.id("C") == 2u);
    mu_assert(m.id("D") == T::null_id);

    T m2(m);
    mu_assert(m.size() == m2.size());
    mu_assert(m[0] == m2[0]);
    mu_assert(m.id("A") == m2.id("A"));
    mu_assert(m.id("D") == m2.id("D"));


    // excepted errors
//    mu_assert(m.id("A") == 3);
//    mu_assert(m[0], m[1]);

    return 0;
}

char* test_operations() {
    char* a = test_operation<StringItemMap>();
    return a;
}


static char * all_tests() {
    mu_run_test(test_constructors);
    mu_run_test(test_operations);

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

