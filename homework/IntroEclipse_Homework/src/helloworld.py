#!/usr/local/bin/python3
#
import unittest

print("Hello World.")


def title(s):
    "How close is this function to str.title()?"
    small_words = ()   # Behave just like s.title() native method
    """ Uncomment the next line to return correct title format
        but different than s.title() native method."""
    #small_words = ('into', 'the', 'a', 'of', 'at', 'in', 'for', 'on') 
    new_title=""
    for i,word in enumerate(s.lower().split()):
        if (word not in small_words) or (i == 0):
            new_title += " " + word.capitalize()
        else:
            new_title += " " + word
    return new_title.lstrip()


class runTest(unittest.TestCase):
    
    def test_title_1_all_numeric(self):
        vtitle = "1984"
        self.assertEqual(title(vtitle), vtitle.title(), "Title should be '1984'")
        
    def test_title_2_all_lower_starts_with_small_word(self):
        vtitle = "the lord of the rings"
        self.assertEqual(title(vtitle), vtitle.title(), "Title should be 'The Lord of the Rings'")
        
    def test_title_3_all_lower_start_with_no_small_word(self):
        vtitle = "lord of the flies"
        self.assertEqual(title(vtitle), vtitle.title(), "Title should be 'Lord of the Flies'")
        
    def test_title_4_tile_all_caps_no_small_words(self):
        vtitle = "ANOTHER ROADSIDE ATTRACTION"
        self.assertEqual(title(vtitle), vtitle.title(), "Title should be 'Another Roadside Attraction'")
        
    def test_title_5_proper_title_format_for_input(self):
        vtitle = "Even Cowgirls Get the Blues"
        self.assertEqual(title(vtitle), vtitle.title(), "Title should be 'Even Cowgirls Get the Blues'")
        
    def test_title_6_bad_input_float(self):
        vtitle = 97.6
        self.assertRaises(TypeError, title(vtitle))

print(title("lord of the flies"))
        
if __name__ == "__main__":
    unittest.main()
    
#