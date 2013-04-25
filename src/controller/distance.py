import math


class Distance(object):

    def compute(self, loc1, loc2):
        """Distance

        Computes the distance between two Locations.

        """
        return math.sqrt((loc1[0]-loc2[0])**2+(loc1[1]-loc2[1])**2)