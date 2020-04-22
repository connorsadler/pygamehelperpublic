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

    def runTest(self, spriteStartPoint, spriteDestinationPoint, numberOfMoves, intermediateCheck = None):
        print(">>> runTest, " + str(spriteStartPoint) + ", " + str(spriteDestinationPoint) + " for moves: " + str(numberOfMoves))
        
        path = s10.Path()
        path.addWaypoint(spriteDestinationPoint[0],spriteDestinationPoint[1])
        pathFollowSprite = s10.PathFollowSprite(path)
        pathFollowSprite.setLocation((spriteStartPoint[0],spriteStartPoint[1]))
        for i in range(0,numberOfMoves):
            pathFollowSprite.move()
            if intermediateCheck:
                intermediateCheck(i, pathFollowSprite)

        # Check that the sprite moves to the path points
        self.assertEqual(pathFollowSprite.x, spriteDestinationPoint[0], "final x should be correct")
        self.assertEqual(pathFollowSprite.y, spriteDestinationPoint[1], "final y should be correct")

        print("<<< runTest")

    def testPathFollowing_simple(self):
        self.runTest((0,0), (100,100), 100)

    # TODO: A test to check a short path
    def testPathFollowing_shortPath(self):
        # TODO: Not sure how many steps to expect it to take
        self.runTest((0,0), (10,10), 15)

    # TODO: A test to check a long path
    def testPathFollowing_longPath(self):

        def intermediateCheck(i, pathFollowSprite): 
            if i % 100 == 0:
                self.assertNotEqual(pathFollowSprite.x, 500, "We should not have reached the endpoint yet")
                self.assertNotEqual(pathFollowSprite.y, 500, "We should not have reached the endpoint yet")

        # TODO: Not sure how many steps to expect it to take
        self.runTest((0,0), (500,500), 300, intermediateCheck)


if __name__ == '__main__':
    unittest.main()