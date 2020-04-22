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
        pass

    def testPathFollowing_simple(self):
        path = s10.Path()
        path.addWaypoint(100,100)
        pathFollowSprite = s10.PathFollowSprite(path)
        pathFollowSprite.setLocation((0,0))
        for i in range(0,100):
            pathFollowSprite.move()

        # Check that the sprite moves to the path points
        self.assertEqual(pathFollowSprite.x, 100, "final x should be correct")
        self.assertEqual(pathFollowSprite.y, 100, "final y should be correct")

    # TODO: A test to check a short path
    def testPathFollowing_shortPath(self):
        path = s10.Path()
        path.addWaypoint(10,10)
        pathFollowSprite = s10.PathFollowSprite(path)
        pathFollowSprite.setLocation((0,0))
        for i in range(0,100):
            pathFollowSprite.move()
        
        # Check that the sprite moves to the path points
        self.assertEqual(pathFollowSprite.x, 100, "final x should be correct")
        self.assertEqual(pathFollowSprite.y, 100, "final y should be correct")

    # TODO: A test to check a long path
    def testPathFollowing_longPath(self):
        path = s10.Path()
        path.addWaypoint(500,500)
        pathFollowSprite = s10.PathFollowSprite(path)
        pathFollowSprite.setLocation((0,0))
        for i in range(0,100):
            pathFollowSprite.move()
        
        # Check that the sprite moves to the path points
        self.assertEqual(pathFollowSprite.x, 100, "final x should be correct")
        self.assertEqual(pathFollowSprite.y, 100, "final y should be correct")


if __name__ == '__main__':
    unittest.main()