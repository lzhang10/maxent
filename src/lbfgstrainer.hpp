/*
 * vi:ts=4:tw=78:shiftwidth=4:expandtab
 * vim600:fdm=marker
 *
 * lbfgstrainer.hpp  -  a conditional ME trainer using Limited Memory BFGS
 * algorithm
 *
 * Copyright (C) 2003 by Zhang Le <ejoy@users.sourceforge.net>
 * Begin       : 01-Jun-2003
 * Last Change : 09-Feb-2012.
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
 */

#ifndef LBFGSTRAINER_H
#define LBFGSTRAINER_H

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "trainer.hpp"

namespace maxent{
class LBFGSTrainer : public Trainer {
    public:
        void train(size_t iter = 100, double eps = 1E-05);
        // void save_param(const string& model, bool binary) const;

    private:
        // void save_param_txt(const string& model) const;
        void init_trainer();
        double heldout_accuracy() const;

        struct featid_hasher {
            size_t operator()(const pair<size_t, size_t>& p) const {
                return p.first + p.second;
            }
        };

        shared_array<double>  m_observed_expects;
};

} // namespace maxent

#endif /* ifndef LBFGSTRAINER_H */

