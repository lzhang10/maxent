#include "minunit.h"
#include <stdio.h>
#include <display.hpp>

int tests_run = 0;

using namespace std;
using namespace maxent;

char* test_display() {
    displayA("hello from char*(no new line)");
    display("hello from char*(with new line)");
    displayA("%s from format(no new line)", "Hello");
    display("%s from format(with new line)", "Hello");
    return 0;
}

static char * all_tests() {
    mu_run_test(test_display);
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

