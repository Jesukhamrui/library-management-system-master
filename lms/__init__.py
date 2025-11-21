"""Package init for lms project.

If PyMySQL is installed, register it as MySQLdb for Django so users on
Windows who can't build `mysqlclient` can still use the MySQL backend.
"""
try:
	import pymysql
	pymysql.install_as_MySQLdb()
except Exception:
	# If PyMySQL isn't available, fall back to native mysqlclient (if installed).
	pass

