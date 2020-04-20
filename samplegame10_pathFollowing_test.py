import unittest

import samplegame10_pathFollowing as s10

#
# VSCode info: https://code.visualstudio.com/docs/python/testing
# 
# TestStringMethods sample tests are taken from: https://docs.python.org/3/library/unittest.html
#

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

class PathFollowSpriteTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.path = s10.Path()
        cls.path.addWaypoint(100,100)
        cls.pathFollowSprite = s10.PathFollowSprite(cls.path)

    def testPathFollowing(self):
        self.pathFollowSprite.setLocation((90,90))
        for i in range(0,300):
            self.pathFollowSprite.move()
            # TODO: We should assert that the sprite moves to the path points

    # TODO: A test to check a short path
    # TODO: A test to check a long path


if __name__ == '__main__':
    unittest.main()