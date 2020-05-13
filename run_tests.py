import sys
sys.path.append("Tests")

import test_sqlite

lite = test_sqlite.test_sqlite_utils()
lite.run()