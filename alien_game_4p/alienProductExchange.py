import collections
import csv
import pandas as pd
import random


class AlienProductExchange:
    magic_number = 1
    lookups = {}
    modules = 0
    num_participants = 0
    images = 0
    rounds = 0
    round = 0
    alien_symbols = [u'\u2756', u'\u2318', u'\u2327', u'\u25CE',
                     u'\u2739', u'\u2316', u'\u0950', u'\u2B9B', u'\u27E1', u'\u1F65', u'\u2312', u'\u232C']
    lookupTablePath = "f'_static/input_files/"
    lookupTableFilename = "LookupTableModules.xlsx"

    def __init__(self, modules, num_participants, images, rounds, round):
        self.images = images
        self.modules = modules
        self.num_participants = num_participants
        self.rounds = rounds
        self.round = round

        if self.num_participants == 1:
            self.num_participants = 2

        self.read_new_lookup_table()

    def read_new_lookup_table(self):
        self.lookups = {
            'Fitness': []
        }

        for i in range(self.modules):
            self.lookups[f'M{i+1}'] = []

        print(self.lookups)

        dataframe = pd.read_excel(f'_static/input_files/LookupTableModules.xlsx')

        for i, row in dataframe.iterrows():
            fitness = 0.0
            for j in range(1, self.modules+1):
                m_fitness = float("{:.2f}".format(self.calculate_lookup(j, row)))
                m_lookup = float("{:.2f}".format(m_fitness * self.magic_number))
                self.lookups[f'M{j}'].append(m_lookup)
                fitness += m_fitness

            lookup = float("{:.2f}".format(fitness) * self.magic_number)
            self.lookups['Fitness'].append(lookup)

    def read_lookup_table(self, round_number):
        self.lookups = []
        with open(f'_static/input_files/lookupTable{round_number}.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                lookup = float("{:.2f}".format(float(row["fitness_norm"]) * self.magic_number))
                self.lookups.append(lookup)

    def list_duplicates(self, seq):
        tally = collections.defaultdict(list)
        for i, item in enumerate(seq):
            tally[item].append(i)
        return ((key, locs) for key, locs in tally.items()
                if len(locs) > 1)

    def get_new_lookup_values(self, bitstring):
        if not self.lookups:
            self.read_new_lookup_table()

        did = int(bitstring, 2)

        values = {
            'bitstring': bitstring,
            'index': did,
            'fitness': self.lookups['Fitness'][did],
        }

        for i in range(1, self.modules + 1):
            values[f'M{i}'] = self.lookups[f'M{i}'][did]

        return values

    def get_lookup_value(self, bit_string, round_number):
        if not self.lookups:
            self.read_lookup_table(round_number)
        did = int(bit_string, 2)
        print(did)
        return self.lookups[did]

    def get_smallest_performance(self, round_number):
        if not self.lookups:
            self.read_lookup_table(round_number)
        i = self.lookups.index(min(self.lookups))
        print(i)
        return format(i, f'0{self.images}b'), self.lookups[i]

    def get_new_smallest_performance(self):
        if not self.lookups:
            self.read_new_lookup_table()

        i = self.lookups['Fitness'].index(min(self.lookups['Fitness']))

        values = {
            'bitstring': format(i, f'0{self.images}b'),
            'index': i,
            'fitness': self.lookups['Fitness'][i],
        }

        for j in range(1, self.modules + 1):
            values[f'M{j}'] = self.lookups[f'M{j}'][i]

        print(values)
        return values

    def calculate_lookup(self, module, row):
        chars_in_module = int(self.images / self.num_participants)
        m_index_start = (module - 1) * chars_in_module + 1
        sum = 0

        for i in range(chars_in_module):
            sum += row[f'C{m_index_start + i}']

        return sum / chars_in_module

