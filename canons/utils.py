"""
    Authors:
    Ryan Baker
    Matt Beaulieu
    Anthony Romeo
"""
import collections
import json


def empty_file(file_name):
    """Empty the contents of a file."""
    with open(file_name, 'w'):
        pass


class Thesaurus(object):
    """A wrapper for a thesaurus function, with logic to handle learning"""
    def __init__(self, lookup_func, logfile=None):
        self.lookup_func = lookup_func
        self.value = 0
        self.iteration = 0
        self.logfile = logfile
        if logfile is not None:
            self.read_logs(logfile)

    def find_syns(self, word):
        """Find the most relevant words from our thesaurus"""
        return self.lookup_func(word)

    def read_logs(self, logfile):
        """
        Read the logs for this thesaurus and return a
        starting value and iteration for this thesaurus
        """
        with open(logfile, 'r') as file_contents:
            data = json.load(file_contents)
            for log in data:
                self.value += log.get('value', 0)
            self.iteration = len(data)

    def add_score(self, input_word, word, score):
        """Writes to the log with a new score for the thesaurus"""
        data = []
        # read the json data from the file
        with open(self.logfile, 'r') as open_file:
            data = json.load(open_file)
            data.append({
                'input': input_word,
                'word': word,
                'value': score,
                'iteration': self.iteration})
        # empty the file
        empty_file(self.logfile)
        # write the json data to the file
        with open(self.logfile, 'w') as open_file:
            json.dump(data, open_file)
        # update the iteration and the value of the thesaurus
        self.iteration += 1
        self.value += score


class OrderedSet(collections.MutableSet):
    def __init__(self, iterable=None):
        self.end = end = []
        end += [None, end, end]         # sentinel node for doubly linked list
        self.map = {}                   # key --> [key, prev, next]
        if iterable is not None:
            self |= iterable

    def __len__(self):
        return len(self.map)

    def __contains__(self, key):
        return key in self.map

    def add(self, key):
        if key not in self.map:
            end = self.end
            curr = end[1]
            curr[2] = end[1] = self.map[key] = [key, curr, end]

    def discard(self, key):
        if key in self.map:
            key, prev, next = self.map.pop(key)
            prev[2] = next
            next[1] = prev

    def __iter__(self):
        end = self.end
        curr = end[2]
        while curr is not end:
            yield curr[0]
            curr = curr[2]

    def __reversed__(self):
        end = self.end
        curr = end[1]
        while curr is not end:
            yield curr[0]
            curr = curr[1]

    def pop(self, last=True):
        if not self:
            raise KeyError('set is empty')
        key = self.end[1][0] if last else self.end[2][0]
        self.discard(key)
        return key

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and list(self) == list(other)
        return set(self) == set(other)
