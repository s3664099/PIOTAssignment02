"""
.. module:: run_tests

"""
import Tests.test_sqlite as test_sqlite

lite = test_sqlite.test_sqlite_utils()
lite.run()