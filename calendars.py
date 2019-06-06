import makefiles

def addToCalendars(config, assignments):
    if config["GOOGLE"]["usr"] != "-":
        pass
    if config["APPLE"]["usr"] != "-":
        import calender_icloud
        cal_apple = calender_icloud.calendar(config["APPLE"])
        oldAssignments = makefiles.readData()
        for assignment in assignments:
            if assignment not in oldAssignments:
                cal_apple.makeEvent(assignment)
