from django.test import TestCase
from .random_numbers import random_from_list


class RandomFromList(TestCase):
    mockListOne = [
        (1, "A"),
        (2, "B"),
        (3, "C"),
        (4, "D")
    ]

    def test_get_random_number_in_the_list_range(self):
        # I'm testing this 10 times duo to short list items given
        for i in range(10):
            self.assertTrue(1 <= random_from_list(self.mockListOne) <= 3)

    def test_get_random_number_in_the_list_range_with_index_start(self):
        # I'm testing this 10 times duo to short list items given
        self.assertEqual(3, random_from_list(self.mockListOne, 3))
        self.assertTrue(2 <= random_from_list(self.mockListOne, 2) <= 3)
