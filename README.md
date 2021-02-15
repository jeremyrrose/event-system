# OOP Event Tracking System

An `Event` class whose instances can each alter the status of their own `actor` via callbacks.

```python
    """
    Arguments:
        actor (any object): The object performing the event.
        time (int): Sequential time value.

    Keyword Arguments:
        actor_events (boolean): Toggles appending event to actor.events (if actor has events attribute).
        callbacks (list): Functions to be invoked (with current event instance as argument) at conclusion of __init__.
    """
```

### Demonstration File

`events.py` in the root directory describes a simulation of a generic fantasy game. Both the `Attack` and `Spell` classes extend `Event`.
