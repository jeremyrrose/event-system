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
