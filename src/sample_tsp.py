#!/usr/bin/env python
# encoding: utf-8

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# author: Paco Nathan
# https://github.com/ceteri/exelixi


from random import randint, sample
from uow import UnitOfWorkFactory
import logging
import sys


######################################################################
## class definitions

class TSPFactory (UnitOfWorkFactory):
    """UnitOfWork definition for Traveling Salesperson Problem"""

    def __init__ (self):
        #super(UnitOfWorkFactory, self).__init__()
        self.n_pop = 10
        self.n_gen = 23
        self.max_indiv = 2000
        self.selection_rate = 0.2
        self.mutation_rate = 0.02
        self.term_limit = 5.0e-03
        self.hist_granularity = 3

        # cost matrix for an example TSP: optimize the bicycling route
        # for weekend chores in Mountain View for a young Steve Jobs
        # tuple definition: (name, addr, duration)

        self.route_meta = ( ( "Home", "secret", 0 ),
                            ( "Piazzas Fine Foods", "3922 Middlefield Rd, Palo Alto, CA 94303", 45 ),
                            ( "Mountain View Public Library", "585 Franklin St, Mountain View, CA 94041", 30 ),
                            ( "Seascapes Fish & Pets Inc", "298 Castro St, Mountain View, CA 94041", 10 ),
                            ( "Dana Street Roasting Company", "744 W Dana St, Mountain View, CA 94041", 20 ),
                            ( "Supercuts", "2420 Charleston Rd, Mountain View, CA 94043", 60 ),
                            )

        self.route_cost = ( ( 0, 7, 11, 12, 14, 8 ),
                            ( 7, 0, 18, 18, 19, 5 ),
                            ( 14, 19, 0, 2, 3, 19 ),
                            ( 12, 20, 3, 0, 1, 19 ),
                            ( 12, 18, 3, 1, 0, 18 ),
                            ( 8, 5, 18, 18, 19, 0 ),
                            )

        # sampling parameters
        self.length = len(self.route_cost) - 1
        self.min = 1
        self.max = self.length


    def generate_features (self):
        """generate a new feature set for young Steve pedaling"""
        features = []
        expected = list(xrange(self.min, self.max + 1))

        # sample row indices in the cost matrix, without replacement
        for _ in xrange(self.length):
            x = sample(expected, 1)[0]
            features.append(x)
            expected.remove(x)

        return features


    def mutate_features (self, feature_set):
        """mutate a copy of the given feature set"""
        pos_to_mutate = randint(0, len(feature_set) - 1)
        mutated_feature_set = list(feature_set)
        mutated_feature_set[pos_to_mutate] = randint(self.min, self.max)
        return mutated_feature_set


    def breed_features (self, f_feature_set, m_feature_set):
        """breed two feature sets to produce a child"""
        half = len(f_feature_set) / 2
        return f_feature_set[half:] + m_feature_set[:half]


    def get_fitness (self, feature_set):
        """determine the fitness ranging [0.0, 1.0]; higher is better"""
        #print feature_set

        # 1st estimator: all points were visited?
        expected = set(xrange(self.min, self.max + 1))
        observed = set(feature_set)
        cost1 = len(expected - observed) / float(len(expected))
        #print expected, observed, cost1

        # 2nd estimator: travel time was minimized?
        total_cost = 0
        worst_case = float(sum(self.route_cost[0])) * 2.0
        x0 = 0

        for x1 in feature_set:
            total_cost += self.route_cost[x0][x1]
            x0 = x1

        total_cost += self.route_cost[x0][0]
        cost2 = min(1.0, total_cost / worst_case)
        #print total_cost, worst_case, cost2

        # combine the two estimators into a fitness score
        fitness = 1.0 - (cost1 + cost2) / 2.0

        if cost1 > 0.0:
            fitness /= 2.0

        #print cost1, cost2, fitness, feature_set
        return fitness


if __name__=='__main__':
    uow = TSPFactory()

    print uow.route_meta
    print uow.route_cost
