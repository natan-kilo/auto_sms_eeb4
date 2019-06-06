import makefiles

def addToCalendars(config, assignments):
    oldAssignments = makefiles.readData()
    if config["GOOGLE"]["usr"] != "-":
        import calender_google
        cal_google = calender_google.calendar(config["GOOGLE"])
        for assignment in assignments:
            if assignment not in oldAssignments:
                cal_google.makeEvent(assignment)
    if config["APPLE"]["usr"] != "-":
        import calender_icloud
        cal_apple = calender_icloud.calendar(config["APPLE"])
        for assignment in assignments:
            if assignment not in oldAssignments:
                cal_apple.makeEvent(assignment)
