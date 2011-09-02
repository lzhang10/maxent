/* file: minunit.h */
/* A minimal unit testing framework for C (improved)
 *
 * by Zhang Le <ejoy@users.sourceforge.net>
 *
 * This file is based on an article titled:
 * << MinUnit -- a minimal unit testing framework for C >>
 * which can be accessed from: http://www.jera.com/techinfo/jtns/jtn002.html
 *
 * The orignal mu_assert can not report failed experssion and filename
 * information. This improved version solves this problem. You can still use
 * the old one by calling mu_assert2
 *
 * Last Change :17-Dec-2004.
 * 
 * Below is the sample usage:

#include "minunit.h"
#include "bpsf.h"
#include <stdio.h>

int tests_run = 0;

char* test_init() {
    bpsf_info* info;
    mu_assert(info = bpsf_create());
    mu_assert(info->m_filename == (const char*)0);
    mu_assert(info->m_bitmap == (void*)0);
    return 0;
}

static char * all_tests() {
     mu_run_test(test_init);
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

 */

#ifndef _MINUNIT_H
#define _MINUNIT_H

#include <string.h> /* for sprintf */

char buf[1000];
/*#define mu_assert(test)  do { if (!(test)) {  return #test "failed at line"  "[__LINE__] of "  __FILE__ ; } } while (0)*/
#define mu_assert(test)  do { if (!(test)) {  sprintf(buf, "%s failed at line [%d] of file %s", #test, __LINE__, __FILE__); return buf ; } } while (0)

#define mu_assert2(message, test) do { if (!(test)) return message; } while (0) 

#define mu_run_test(test) do { char *message = test(); tests_run++; if (message) return message; } while (0)

extern int tests_run;

#endif /* _MINUNIT_H */
