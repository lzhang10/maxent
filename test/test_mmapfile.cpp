// test ItemMap
#include "minunit.h"
#include <mmapfile.hpp>
#include <fstream>
#include <cstdio>
#include <line_mem_iterator.hpp>
#include <token_mem_iterator.hpp>

int tests_run = 0;

using namespace std;

char* test_mmapfile() {
    char* tmpfile = tmpnam(0);
    ofstream of(tmpfile, ios::binary);
    for (size_t i = 0;i < 100; ++i)
        of.write((const char*)&i, sizeof(i));
    of.close();

    MmapFile fm(tmpfile, "r", 0);
    mu_assert(fm.open() == true);
    mu_assert(fm.size() == 100ul*sizeof(size_t));

    size_t* p = (size_t*)fm.addr();
    for (size_t i = 0;i < 100; ++i)
        mu_assert(*p++ == i);
    mu_assert(remove(tmpfile) == 0);
    return 0;
}

char* test_line_mem_iterator() {
    char* tmpfile = tmpnam(0);
    {
        ofstream of(tmpfile);
        of << "first line." << endl;
        of << "second line." << endl;
        of << "" << endl;
        of << "last line!" << endl;
    }
    MmapFile fm(tmpfile, "r", 0);
    mu_assert(fm.open() == true);
    const char* data = (const char*)fm.addr();
    line_mem_iterator<> it(data, data + fm.size());
    line_mem_iterator<> end;
    for (; it != end; ++it) {
        string s(it->first, it->second - it->first);
        cout << s << endl;
    }
    mu_assert(remove(tmpfile) == 0);
    return 0;
}

char* test_token_mem_iterator() {
    char buf[] = " this	is  ÖÐ¹ú 	a \r\r test !  \r\r";
    token_mem_iterator<> it(buf, buf + strlen(buf));
    token_mem_iterator<> end;
    for (; it != end; ++it) {
        string s(it->first, it->second - it->first);
        cout << s << endl;
    }
    return 0;
}

static char * all_tests() {
    mu_run_test(test_mmapfile);
    mu_run_test(test_line_mem_iterator);
    mu_run_test(test_token_mem_iterator);
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

