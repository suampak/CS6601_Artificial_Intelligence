import random
import unittest

from priority_queue import PriorityQueue

class TestPriorityQueue(unittest.TestCase):
    def test_append_and_pop(self):
        """Test the append and pop functions"""
        queue = PriorityQueue()
        temp_list = []

        for _ in xrange(10):
            a = random.randint(0, 10000)
            queue.append((a, 'a'))
            temp_list.append(a)

        temp_list = sorted(temp_list)

        for item in temp_list:
            popped = queue.pop()
            self.assertEqual(item, popped[0])

if __name__ == '__main__':
    unittest.main()
