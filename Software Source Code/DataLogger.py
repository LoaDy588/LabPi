class DataLogger:

    # global debug
    _debug = False

    # init function
    def __init__(self, debug=False):

        # global data
        self.data = []

        # configuring global debug
        self._debug = debug

        # debug print
        if self._debug:
            print "DataLogger initiated"

    # write info function, requires info dictionary
    def writeInfo(self, info={'date': 'dd-mm-yyyy', 'time': 'hh:mm',
                              'freq': 'f'}):

        # debug print
        if self._debug:
            print "creating data list"

        # write info to the end of list
        self.data.append(info)


        # debug print
        if self._debug:
            print "data list created: ", info

    # erase current data function
    def eraseData(self):

        # delete everything from list
        del self.data[:]

        # debug print
        if self._debug:
            print "data list erased"

    # write data to list end of list
    # requires  data to write
    def writeData(self, data=0):

        if self._debug:
            print "writing new data: " + data

        self.data.append(data)

    # read single data point from list, requires position, returns data
    # on overflow of index returns "empty"
    def readSingleData(self, position=0):

        # debug print
        if self._debug:
            print "reading at: ", position

        # check overflow
        if ((((position + 1) < len(self.data)) == True) ==
                (((-position) < len(self.data)) == True)):
            # shifting because of info on [0]
            if position >= 0:
                return self.data[(position + 1)]
            else:
                return self.data[(position)]
        else:
            return "empty"

    # returns data without first index(without info)
    def readData(self):

        # debug print
        if self._debug:
            print "reading data list"

        # return list without first index
        return self.data[1:]

    # returns info dictionary
    def readInfo(self):

        # debug print
        if self._debug:
            print "reading info from data list"

        # return first index of data list
        return self.data[0]

    # saves data to a file     REWRITE REWRITE REWRITE REWRITE
    # requires file name, file location
    def saveData(self, name="name", location="location"):

        # debug print
        if self._debug:
            print "saving file at: ", (location + name + ".txt")

        # open file(create if not existing, overwrite if exists)
        # write every item from list to new line
        file = open((location + name + ".txt"), "w")
        for temp in self.data:
            file.write(str(temp) + "\n")
        file.close()

        # debug print
        if self._debug:
            print "file saved at: ", (location + name + ".txt")
