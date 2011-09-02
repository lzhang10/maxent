/*
 * vi:ts=4:tw=78:shiftwidth=4:expandtab
 * vim600:fdm=marker
 *
 * sdrive.c  -  simple driver for lbfgs, translated from sdrive.f
 * usage:
 *      1. g77 -c lbfgs.f
 *      2. gcc -o sdrive sdrive.c lbfgs_wrapper.c lbfgs.o -lg2c
 *      3. ./sdriver
 *
 * Copyright (C) 2004 by Zhang Le <ejoy@users.sourceforge.net>
 * Begin       : 17-Nov-2004
 * Last Change : 26-Apr-2005.
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
 * THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
 * DEALINGS IN THE SOFTWARE.
 */

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <assert.h>

#include <stdio.h>
#include "lbfgs.h"

int main(int argc, char **argv)
{
    double f;
    int j;
    int n;
    int icall;
    double t1, t2;
    double x[100];
    double g[100];

    lbfgs_t* opt;

    n = 100;
    opt = lbfgs_create(n, 5, 1.0E-5);
    opt->iprint[0] = 1;
    opt->iprint[1] = 0;
    opt->diagco = 0;

    for (j = 0; j < n; j += 2) {
        x[j] = -1.2;
        x[j+1] = 1;
    }

    icall = 0;
    while (1) {
        f = 0;
        for (j = 0; j < n; j += 2) {
            t1 = 1 - x[j];
            t2 = 10 * (x[j+1] - x[j] * x[j]);
            g[j+1] = 20 * t2;
            g[j] = -2 * (x[j] * g[j+1] + t1);
            f = f + t1 * t1 + t2 * t2;
        }
        if (lbfgs_run(opt, x, &f, g) <= 0)
            break;
        ++icall;
        /* We allow at most 2000 evaluations of F and G */
        if (icall > 2000)
            break;
    }

    lbfgs_destory(opt);

    return 0;
}


