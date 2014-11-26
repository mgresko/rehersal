class BunchDict(dict):

    def __getattr__(self, attr):
        if attr in self.__dict__.keys():
            return self.__dict__[attr]
        else:
            val = self[attr]
            if isinstance(val, dict):
                return BunchDict(val)
            else:
                return val
