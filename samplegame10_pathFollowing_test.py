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

    def runTest(self, alternateMode, spriteStartPoint, spriteDestinationPoint, numberOfMoves, intermediateCheck = None, speed = None):
        print(">>> runTest, alternateMode: " + str(alternateMode) + ", start: " + str(spriteStartPoint) + " dest: " + str(spriteDestinationPoint) + " for moves: " + str(numberOfMoves))
        
        path = s10.Path()
        path.addWaypoint(spriteDestinationPoint[0],spriteDestinationPoint[1])
        pathFollowSprite = s10.PathFollowSprite(path)
        pathFollowSprite.setLocation((spriteStartPoint[0],spriteStartPoint[1]))
        pathFollowSprite.setPathFollowModeAlternate(alternateMode)
        if speed:
            pathFollowSprite.getMoveHandler().setSpeed(speed)

        for i in range(0,numberOfMoves):
            print("move: " + str(i+1))
            pathFollowSprite.move()
            if intermediateCheck:
                intermediateCheck(i, pathFollowSprite)

        # Check that the sprite moves to the path points
        self.assertEqual(pathFollowSprite.x, spriteDestinationPoint[0], "final x should be correct")
        self.assertEqual(pathFollowSprite.y, spriteDestinationPoint[1], "final y should be correct")

        print("<<< runTest")

    def testPathFollowing_simple_defaultStrategy(self):
        # default strategy always takes 100 steps
        self.runTest(False, (0,0), (100,100), 100)

    # A test to check a short path
    def testPathFollowing_shortPath_defaultStrategy(self):
        # default strategy always takes 100 steps
        self.runTest(False, (0,0), (10,10), 100)

    # A test to check a long path
    def testPathFollowing_longPath_defaultStrategy(self):

        def intermediateCheck(i, pathFollowSprite): 
            if i % 10 == 0:
                self.assertNotEqual(pathFollowSprite.x, 500, "We should not have reached the endpoint yet")
                self.assertNotEqual(pathFollowSprite.y, 500, "We should not have reached the endpoint yet")

        # default strategy always takes 100 steps
        self.runTest(False, (0,0), (500,500), 100, intermediateCheck)

    def testPathFollowing_simple_altStrategy(self):
        # Calc is:
        # numSteps: 141.4213562373095
        # velocityVector: (0.7071067811865476, 0.7071067811865476)
        # after 141 steps we are at: 
        #   new location: (99.70205614730341, 99.70205614730341)
        #   check: (0.29794385269659074, 0.29794385269659074)
        self.runTest(True, (0,0), (100,100), 142)

    # A test to check a short path
    def testPathFollowing_shortPath_altStrategy(self):
        # Calc is:
        # numSteps: 14.142135623730951
        # velocityVector: (0.7071067811865475, 0.7071067811865475)
        self.runTest(True, (0,0), (10,10), 15)

    # A test to check a long path
    def testPathFollowing_longPath_altStrategy(self):

        def intermediateCheck(i, pathFollowSprite): 
            if i % 100 == 0:
                self.assertNotEqual(pathFollowSprite.x, 500, "We should not have reached the endpoint yet")
                self.assertNotEqual(pathFollowSprite.y, 500, "We should not have reached the endpoint yet")

        # Calc is:
        # numSteps: 707.1067811865476
        # velocityVector: (0.7071067811865475, 0.7071067811865475)
        self.runTest(True, (0,0), (500,500), 708, intermediateCheck)

    def testPathFollowing_simple_altStrategy_speed3(self):
        # Only takes 48 moves now to get there
        self.runTest(True, (0,0), (100,100), 48, None, 3)

    # A test to check a short horizontal path with speed 3
    def testPathFollowing_shortHorizontalPath_altStrategy_speed3(self):
        # Calc is:
        # checking location vs destination
        #   location: (0, 0)
        #   destination: (10, 0)
        # alternate/advanced mode, with speed: 3
        # numSteps: 3.3333333333333335
        # velocityVector: (3.0, 0.0)
        self.runTest(True, (0,0), (10,0), 5, None, 3)

    def testPathFollowing_shortPath_altStrategy_speed3(self):
        # TODO
        self.runTest(True, (0,0), (10,10), 15, None, 3)

    def testPathFollowing_longPath_altStrategy_speed3(self):
        def intermediateCheck(i, pathFollowSprite): 
            if i % 100 == 0:
                self.assertNotEqual(pathFollowSprite.x, 500, "We should not have reached the endpoint yet")
                self.assertNotEqual(pathFollowSprite.y, 500, "We should not have reached the endpoint yet")

        # 708/3 approx = 236
        self.runTest(True, (0,0), (500,500), 236, intermediateCheck, 3)


if __name__ == '__main__':
    unittest.main()