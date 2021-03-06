import math
import random

from realm_generator import person
from realm_generator import alignment


class Faction():
    def __init__(self, data, nobility, powerful=False):
        self.region = random.choice(nobility)
        if len(self.region.vassals) > 0:
            self.region = random.choice(self.region.vassals).name

        self.name = self._generate_name(data)
        self.events = []
        self.persons = []
        self.powerful = powerful
        self.reputation = random.choice(data['adjectives'])

        self.alignment, self.alignment_print = alignment.get_alignment(data)

        num_of_mems = 3 + math.floor(random.random() * 7)

        if self.powerful is True:
            self.size = math.floor(
                random.random() * 1000 +
                random.random() * 100 +
                random.random() * 10 +
                num_of_mems
            )
        else:
            self.size = math.floor(
                random.random() * 100 +
                random.random() * 10 +
                num_of_mems
            )

        self.persons.append(person.Person(data, alignment=self.alignment, leader=True))

        for _ in range(num_of_mems - 1):
            mem = person.Person(data, alignment=self.alignment)
            mem.leader_relation = "follower"
            self.persons.append(mem)

        for m in self.persons:
            if m.age < person.ADULT_AGE:
                m.age = person.ADULT_AGE

    def get_leader(self):
        h = [m for m in self.persons if m.head is True]
        if len(h) > 0:
            return h[0]

    def _generate_name(self, data):
        if random.random() > 0.5:
            r = random.random()
            if r > 0.66:
                name = "{} of the {}".format(
                    random.choice(data['faction_prefixes']),
                    random.choice(data['animals'])
                )
            elif r > 0.33:
                name = "{} of Saint {}".format(
                    random.choice(data['faction_prefixes']),
                    random.choice(data['names_male'])
                )
            else:
                name = "{} of {}".format(
                    random.choice(data['faction_prefixes']),
                    self.region
                )
        else:
            if random.random() > 0.5:
                name = "{} {}".format(
                    self.region,
                    random.choice(data['faction_suffixes'])
                )
            else:
                name = "{} {}".format(
                    random.choice(data['adjectives_whimsical']).capitalize(),
                    random.choice(data['faction_suffixes'])
                )

        return name


def create_factions(data, powerful_factions, weak_factions, nobility):
    factions = []

    for _ in range(powerful_factions):
        f = Faction(data, nobility, powerful=True)
        factions.append(f)

    for _ in range(weak_factions):
        f = Faction(data, nobility)
        factions.append(f)

    return factions


def all_agents(factions):
    agents = []
    for f in factions:
        for m in f.members:
            agents.append(m)
    return agents


def random_agent(factions):
    agents = all_agents(factions)
    return random.choice(agents)
