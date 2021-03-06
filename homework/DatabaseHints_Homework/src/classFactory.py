#!/usr/local/bin/python3
"""
classFactory: function to return a tailored class
"""

def build_row(table, cols):
    """Build a class that creates instances of specific rows"""

    class DataRow:
        """Generic data row class, specialized by surrounding function"""

        def __init__(self, data):
            """Uses data and colum names to inject attributes"""
            assert len(data)==len(self.cols)
            for colname, dat in zip(self.cols, data):
                setattr(self, colname, dat)

        def __repr__(self):
            return "{0}_record({1})".format(self.table, ", ".join(["{0!r}".format(getattr(self, c)) for c in self.cols]))

        def retrieve(self, curs, condition=None):
            lquery=("SELECT * FROM %s " % self.table) + str(condition)
            curs.execute(lquery)
            for row in curs.fetchall():
                yield DataRow(row)


    DataRow.table = table
    DataRow.cols = cols.split()
    return DataRow

