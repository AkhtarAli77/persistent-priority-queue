import os
import tempfile
import unittest

from module import PersistentPriorityQueue


class TestPersistentPriorityQueue(unittest.TestCase):

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        self.queue = PersistentPriorityQueue(self.temp_file.name)

    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)

    def test_insert_and_peek(self):
        self.queue.insert("Task A", 3)
        self.queue.insert("Task B", 1)

        self.assertEqual(self.queue.peek()["item"], "Task B")
        self.assertEqual(self.queue.peek()["priority"], 1)

    def test_extract_min(self):
        self.queue.insert("Task A", 3)
        self.queue.insert("Task B", 1)

        result = self.queue.extract_min()

        self.assertEqual(result["item"], "Task B")
        self.assertEqual(result["priority"], 1)

    def test_extract_max(self):
        self.queue.insert("Task A", 3)
        self.queue.insert("Task B", 1)

        result = self.queue.extract_max()

        self.assertEqual(result["item"], "Task A")
        self.assertEqual(result["priority"], 3)

    def test_update(self):
        self.queue.insert("Task A", 5)

        result = self.queue.update("Task A", 1)

        self.assertTrue(result)
        self.assertEqual(self.queue.peek()["priority"], 1)

    def test_delete(self):
        self.queue.insert("Task A", 1)

        result = self.queue.delete("Task A")

        self.assertTrue(result)
        self.assertTrue(self.queue.is_empty())

    def test_is_empty(self):
        self.assertTrue(self.queue.is_empty())

        self.queue.insert("Task A", 1)

        self.assertFalse(self.queue.is_empty())

    def test_persistence(self):
        self.queue.insert("Task A", 2)

        new_queue = PersistentPriorityQueue(self.temp_file.name)

        self.assertFalse(new_queue.is_empty())
        self.assertEqual(new_queue.peek()["item"], "Task A")
        self.assertEqual(new_queue.peek()["priority"], 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)