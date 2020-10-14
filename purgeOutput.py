import os
import shutil

[shutil.rmtree(x[0]) for x in os.walk('.') if x[0].startswith(".\dataset_")]
