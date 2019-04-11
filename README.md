# pynchronized
A `@synchronized` decorator for synchronising classes or methods, similar to Java's synchronized keyword

## Synchronizing classes
A synchronized class is a class in which methods can only be executed sequentially.

For example, because only one method of `SyncSleeper` can run at a time, the following script will take 3s to run - instead of 2s in the unsynchronized case:

```python
import time
from multiprocessing import Process
from pynchronized import synchronized

@synchronized
class SyncSleeper:
    def sleep_1s(self):
        time.sleep(1)
    def sleep_2s(self):
        time.sleep(2)

sleeper = SyncSleeper()
processes = [
    Process(target=sleeper.sleep_1s, deamon=True),
    Process(target=sleeper.sleep_2s, deamon=True),
]
for p in processes: p.start()
for p in processes: p.join()
```

## Synchronizing methods
Similarly, a there can be only one instance of a synchronized method executing at any time. The following script will take 4s to run instead of 5s if it were a synchronized class instead or 2s in an unsynchronized case:

```python
import time
from multiprocessing import Process
from pynchronized import synchronized

class SyncSleeper:
    def sleep_1s(self):
        time.sleep(1)
    @synchronized
    def sleep_2s(self):
        time.sleep(2)

sleeper = SyncSleeper()
processes = [
    Process(target=sleeper.sleep_1s, daemon=True),
    Process(target=sleeper.sleep_2s, daemon=True),
    Process(target=sleeper.sleep_2s, daemon=True),
]
for p in processes: p.start()
for p in processes: p.join()
```
