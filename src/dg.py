import nest

import models.gc
import models.bc
import models.mc
import models.hipp

gcs = nest.Create("gc", 2000)
mcs = nest.Create("bc", 100)
mcs = nest.Create("mc", 80)
mcs = nest.Create("hipp", 40)