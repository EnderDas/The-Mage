#frame
"""
Frame
|_object :class object:
"""

class Frame:

    def __init__(self, _object):
        self.obj = _object
        self.dict = {}
        var = vars(self.obj)
        for i in var.keys():
            if type(var[i]) == type(list()):
                self.dict[i] = []
                for k in var[i]:
                    if hasattr(k, 'frame'):
                        self.dict[i].append(k.frame)
                    else:
                        self.dict[i].append(k)
            else:
                try:
                    self.dict[i] = var[i].frame
                except:
                    self.dict[i] = var[i]
        """self.dict = {
            i: i.frame
                if hasattr(i, 'frame')
                else getattr(self.obj, i)
                for i in vars(self.obj).keys()
        }"""

    def __repr__(self):
        return str(self.dict)
