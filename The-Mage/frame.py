#frame

"""
Frame
|_object :class object:
"""

class Frame:

    def __init__(self, _object):
        self.obj = _object
        if hasattr(self.obj, '__dict__'):
            self.dict = {
                i: i.frame
                    if hasattr(i, 'frame')
                    else getattr(self.obj, i)
                    for i in vars(self.obj).keys()
            }
        else:
            self.dict = {
                i: i.frame
                    if hasattr(i, 'frame')
                    else getattr(self.obj, i)
                    for i in self.obj.__slots__
            }

    def __repr__(self):
        return str(self.dict)
