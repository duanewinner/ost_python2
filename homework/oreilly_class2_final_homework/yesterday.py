        """
        Create a temporary settings.py file based on yesterday's date.
        By always using yesterday as the starting date, and dynamically generating settings.py,
        we should guarantee that these tests will always work, and consistently,
        regardless of when they are run.
        WARNING: This will overwrite any existing settings.py file.
        """
        os.chdir(self.workingdir)
        recipients = [("John Doe", "jdoe@abc.abc"),("Alice Smith", "asmith@abc.abc"),("Charlie Brown", "cbrown@abc.abc")]
        daycount = 500
        ydate = (datetime.date.today()-datetime.timedelta(days=1))
        starttime = ("\"" + str('%04d' % ydate.year) + "-" + str('%02d' % ydate.month) + "-" + str('%02d' % ydate.day) + "\"")
        f = open("settings.py", 'w')
        f.write("RECIPIENTS = " + str(recipients) + \
                "\nSTARTTIME = " + starttime + \
                "\nDAYCOUNT = " + str(daycount) + "\n")
        f.close()
