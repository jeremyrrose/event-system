from random import random
import pandas as pd
from events.event import Event

class Paladin:
    def __init__(self, name, damage, magic_power, attack_speed, spell_speed):
        self.name = name
        self.events = []

        # These variables might be set by other methods that would determine, like armaments and strength and what-not.
        self.damage = damage
        self.attack_speed = attack_speed
        self.spell_speed = spell_speed
        self.magic_power = magic_power

        # I don't remember the name of this attribute, but it's the thing that happens for a while when you get a crit
        self.vengeance = None

        self.last_attack = 0
        self.last_spell = 0
        self.last_heal = 0

    def set_vengeance(self, event):
        if event.crit:
            self.vengeance = event.time
        elif self.vengeance and event.time - self.vengeance > 20 and not event.crit:
            self.vengeance = None

    def set_last_attack(self, event):
        self.last_attack = event.time

    def set_last_spell(self, event):
        self.last_spell = event.time

    # if spell_speed is a variable factor, it would also make sense to have a spell_ready method
    def attack_ready(self, time):
        return (time - self.last_attack) > self.attack_speed

    def spell_ready(self, time):
        return (time - self.last_spell) > self.spell_speed

    # not sure how decision-making works -- you might have a more complex decision tree
    # this assumes that if a character can attack, they'll attack
    def decision(self, time):
        """
        Determines a character's event decision based on time.

        Args:
            time (int): Sequential time value based on do_events function below.

        Returns:
            Event: An Event of the most prefered type available at the given time.
        """

        # if vengeance is set, check if vengeance has expired
        # if self.vengeance and (time - self.vengeance) > 80:
        #     self.vengeance = None

        if self.attack_ready(time):
            damage = self.damage

            # increase damage if vengeance is active
            if self.vengeance and time - self.vengeance < 200:
                damage = damage * 1.25

            return Attack(self, time, actor_events=True, damage=damage, callbacks=[self.set_last_attack, self.set_vengeance])

        if self.spell_ready(time):
            return Spell(self, time, actor_events=True, magic_power=self.magic_power, callbacks=[self.set_last_spell])

    def __repr__(self):
        return f"{self.name} the {self.__class__.__name__}"


class Attack(Event):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.crit = random() > 0.90
        self.damage = kwargs.get('damage')
        super().callbacks()

    def damage_estimate(self):
        return self.damage
    
    def __repr__(self):
        base = super().__repr__()
        if self.crit:
            base = base + " (!!!CRITICAL!!!)"
        return f"{base}: damage {self.damage}"


class Spell(Event):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.magic_power = kwargs.get('magic_power')
        super().callbacks()

    def damage_estimate(self):
        return self.magic_power
    
    def __repr__(self):
        base = super().__repr__()
        return f"{base}: magic power {self.magic_power}"



def do_events(time_limit, *args):
    """
    Performs events for a specified list of characters for a specified time.

    Args:
        time_limit (int): Number of loop iterations to perform
        args ([Paladin]): Paladin or Paladins to include in events loop
    """

    # reset character attributes in case of multiple do_events calls
    for character in args:
        character.last_attack = 0
        character.last_spell = 0
        character.last_heal = 0

    i = 0
    while i < time_limit:

        for character in args:
            character.decision(i)

        i += 1

def convert_to_dataframe(event_list):
    
    parsed_event_list = []

    for event in event_list:
        damage, magic_power, critical = None, None, None
        if isinstance(event, Attack):
            damage = event.damage
            critical = event.crit
        if isinstance(event, Spell):
            magic_power = event.magic_power
        # row = pd.Series([event.time, event.actor.name, event.__class__.__name__, damage, magic_power, critical ], index=df.columns)
        # print(row)
        parsed_event_list.append([event.time, event.actor.name, event.__class__.__name__, damage, magic_power, critical ])

    df = pd.DataFrame(parsed_event_list, columns=["Time","Actor","Type","Damage","Magic Power", "Critical"])
    return df


def main():

    # args order: name, damage, magic_power, attack_speed, spell_speed
    jeremy = Paladin('Jeremy', 35, 70, 7, 21)
    hristina = Paladin('Hristina', 70, 60, 13, 13)
    ted = Paladin("Ted", 55, 55, 11, 19)

    do_events(200, jeremy, hristina, ted)

    # for event in hristina.events:
    #     print(event)

    results = convert_to_dataframe(Event.events)
    # all results in dataframe
    print(results)

    #only critical
    print(results[results["Critical"] == True])

    print("\n\ntotal magic power of spells: ", sum(results[results["Type"] == "Spell"]["Magic Power"]))

    # all events ever performed by any character
    # print(f"\n\n{len(Event.events)} events: ", Event.events)

    print("jeremy's total damage: ", sum(event.damage_estimate() for event in jeremy.events))
    print("hristina's total damage: ", sum(event.damage_estimate() for event in hristina.events))
    print("ted's total damage: ", sum(event.damage_estimate() for event in ted.events))

    derf = Event('hi there', 340, actor_events=True)
    print(derf)

if __name__ == '__main__':
    main()
