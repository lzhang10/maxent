/*
 * vi:ts=4:shiftwidth=4:expandtab
 * vim600:fdm=marker
 *
 * itemmap.hpp  -  generic item <--> id map class
 *
 * Copyright (C) 2002 by Zhang Le <ejoy@users.sourceforge.net>
 * Begin       : 31-Dec-2002
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

#ifndef ITEMMAP_H
#define ITEMMAP_H

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <iostream>
#include <vector>
#include <string>
#include <functional>

#include <tr1/unordered_map>

template <typename T,
         typename _Hash = std::tr1::hash<T>,
         typename _Pred = std::equal_to<T> >
class ItemMap {
    public:
        typedef T      item_type;
        typedef size_t id_type;
        typedef std::tr1::unordered_map <T, id_type, _Hash, _Pred>         hash_map_type;
        static const size_t null_id;
        typedef typename std::vector<T>::iterator       iterator;
        typedef typename std::vector<T>::const_iterator const_iterator;

        ItemMap(){}

        ~ItemMap();

        iterator begin() { return m_index.begin(); }

        iterator end() { return m_index.end(); }

        const_iterator begin() const { return m_index.begin(); }

        const_iterator end() const { return m_index.end(); }

        size_t size() const { return m_index.size(); }

        bool empty() const { return m_index.empty(); }

        void clear();

        /**
         * add a item into dict return new item's id
         * if the item already exists simply return its id
         */
        id_type add(const T& f);

        /**
         * get a item's id (index in dict)
         * if the item does not exist return null_id
         */
        id_type id(const T& f) const {
            typename hash_map_type::const_iterator it = m_hashdict.find(f);
            if (it == m_hashdict.end())
                return null_id;
            return it->second;
            // return has_item(f) ? m_hashdict[f] : null_id;
        }

        bool has_item(const T& f) const {
            return m_hashdict.find(f) != m_hashdict.end();
        }

        const T& operator[](id_type id) const {
            return m_index[id];
        }

    private:
        mutable hash_map_type m_hashdict;
        std::vector<T>        m_index;
};


template <typename T, typename _Hash, typename _Pred>
const size_t ItemMap<T, _Hash, _Pred>::null_id = 
~(typename ItemMap<T, _Hash, _Pred>::id_type)(0); // -1 is null_id
#include "itemmap.tcc"
#endif /* ifndef ITEMMAP_H */
