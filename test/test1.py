import mixins


class People(object):

    def people_print(self):
        print('People')


class AaaPeople(People):
    def Aaa_print(self):
        print('aaa')

class BbbPeople:
    def Bbb_print(self):
        print('bbb')


def bb_aa_people():
    p = AaaPeople()
    AaaPeople.__bases__ += (BbbPeople,)
    return p

ba = bb_aa_people()
ba.Bbb_print()