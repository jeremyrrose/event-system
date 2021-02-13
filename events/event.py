class Event:

    """
    Creates an Event.

    Arguments:
        actor (any object): The object performing the event.
        time (int): Sequential time value.

    Keyword Arguments:
        actor_events (boolean): Toggles appending event to actor.events (if actor has events attribute).
        callbacks (list): Functions to be invoked (with current event instance as argument) at conclusion of __init__.
    """

    # class variable containing all events by any actor
    events = []

    def __init__(self, actor, time, **kwargs):
        self.__time = time
        self.__actor = actor
        self.events.append(self)
        if kwargs.get('actor_events') and hasattr(self.__actor, 'events') and isinstance(self.__actor.events, list):
            self.__actor.events.append(self)
        self.__callbacks = kwargs.get('callbacks') or ()

    def callbacks(self):
        """
        Invoke super().callbacks() in child class to run all.
        This will likely be done at the conclusion of the __init__.
        """
        for callback in self.__callbacks:
            try:
                callback(self)
            except:
                print(f"{callback} could not be executed.")

    def __repr__(self):
        return f"{self.__class__.__name__} by {self.actor} at time {self.time}"

    @property
    def time(self):
        return self.__time

    @property
    def actor(self):
        return self.__actor