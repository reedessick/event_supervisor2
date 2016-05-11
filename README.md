# event_supervisor2
a holder for event_supervisor development based off the lvalertMP architecture

we divide each basic type of follow-up process into a separate package. Within each of these packages, modules define extensions of the lvalertMPutils.QueueItem class and all the required methods to support them. These are then used within event_supervisor.parseAlert in response to lvalert messages and are managed dynamically through an instance of ligo.lvalert.interactiveQueue.interactiveQueue running via multiprocessing from lvalert_listenMP.

All that being said, event_supervisor.parseAlert should contain the bulk of the logic associated with the project's goals and each package/module should really just provide a fall-back check which we peform by actually querying GraceDB (instead of just listening to lvalerts).

-------------------

eventSupervisor is organized into several different modules, each corresponding to a different type of follow-up activity. Within each module, extension of eventSupervisorUtils.EventSupervisorQueueItem (an extension of lvalertMPutils.QueueItem) and eventSupervisorUtils.EventSupervisorTask (an extension of lvalertMPutils.Task) are defined. These specify exactly what is expected of each follow-up process, how to check for it, and what action should be taken if deemed necessary. For the most part, this involves querying GraceDB for log messages and files. If they are missing or otherwise indicate a problem, an email is sent to the "responsible parties" but no other action is taken.

The QueueItems defines within each module have a standardized __init__() format, which extracts the required information directly from a config object. In this way, we can standardize how Items are created by passing the same arguments and simply iterating over the Item's names as specified in some directed graph. Furthermore, each QueueItem is responsible for defining the Tasks it needs within the Item's __init__() call. All defined items (subclass of eventSupervisorUtils.EventSupervisorQueueItem) are automatically identified from the modules loded in eventSupervisor.py. In this way, if we add a new Item or module, all that has to be updated is the "directed graph" which defines the parent/child relation ships (and possibly parsing to identify when new log messages satisfy checks).

-------------------

need to write a testing suite that makes sure things are built correctly and all the plumbing works! This could be combined with a large-scale functionality test with lvalertMP to observe the whole thing function together.
