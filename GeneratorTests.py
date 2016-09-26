import unittest
import Generator
import Topology
import Utilities


class MyTestCase(unittest.TestCase):
    file = "mongo_creds.json"
    profile = "TestFiles/profile.json"
    test_config = "TestFiles/test_config.json"
    leet = "leet_speak.json"
    config = "config.json"

    def _get_topologies(self):
        db = Generator.get_topologies(self.file, 25)
        self.assertNotEqual(db, None)

    def _get_topology(self):
        result = Generator.load_topologies(500, self.config)
        self.assertTrue(result is not None)

    def test_is_eligible(self):
        result = Generator.is_eligible("?l?l?l?l", self.test_config)
        self.assertFalse(result)
        result = Generator.is_eligible("?l?l?l?l?n?l?l?l?l", self.test_config)
        self.assertFalse(result)
        result = Generator.is_eligible("?l?l?l?l?s?u?l?l?l", self.test_config)
        self.assertTrue(result)
        result = Generator.is_eligible("?l?l?l?l?n?l?u?l?l", self.test_config)
        self.assertTrue(result)

    def test_organized_data(self):
        profile = Utilities.get_JSON_Obj(self.profile)
        organized_data = Generator.organize_profile(profile)
        for x in organized_data.keys():
            for y in organized_data[x]:
                self.assertEquals(x, len(y))
        self.assertTrue("John" in organized_data[4])

    def test_determine_segments(self):
        segments = Generator.get_segments_("?l?l?l?l?l?n?n?n?n?s?s?s?u", [], 0, 'l')
        self.assertEquals(len(segments), 4)
        segments = Generator.get_segments_("?l?l?l?l?l?n?n?n?n?s?s?s?u?u?u", [], 0, 'l')
        self.assertEquals(len(segments), 4)
        segments = Generator.get_segments_("?l?n?s?u", [], 0, 'l')
        self.assertEquals(len(segments), 4)
        segments = Generator.get_segments_("?l", [], 0, 'l')
        self.assertEquals(len(segments), 1)
        segments = Generator.get_segments_(None, [], 0, 'l')
        self.assertTrue(segments is None)
        segments = Generator.get_segments("?l?l?l?l?l?n?n?n?n?s?s?s?u")
        self.assertEquals(len(segments), 4)

    def test_flatten(self):
        flattened = Utilities.flatten_('?l?n?u?s')
        self.assertEquals(flattened,'?l?n?l?l')

    def test_make_password_guesses1(self):
        topology_obj = Topology.Topology('?l?l?l?l?l?l?n?n',8)
        organized_profile = Generator.organize_profile(Utilities.get_JSON_Obj(self.profile))
        passwords = Generator.make_password_guesses(topology_obj,organized_profile)
        self.assertTrue(passwords == None)

    def test_make_password_guesses2(self):
        topology_obj = Topology.Topology('?l?l?l?l?n?n', 546)
        organized_profile = Generator.organize_profile(Utilities.get_JSON_Obj(self.profile))
        passwords = Generator.make_password_guesses(topology_obj, organized_profile)
        self.assertTrue('Salt01' in passwords)
        self.assertTrue('Salt02' in passwords)
        self.assertTrue('John01' in passwords)
        self.assertTrue('John02' in passwords)

    def test_gen_passwords(self):
        pass

    def test_only_eligible_chars(self):
        test_str = "#$%^345#f"
        config = Utilities.get_JSON_Obj(self.config)
        self.assertTrue(Generator.only_eligible_char(test_str,config))
        test_str = "(asdfasdf"
        self.assertFalse(Generator.only_eligible_char(test_str,config))
    def test_sub_vowels(self):
        leet = Utilities.get_JSON_Obj(self.leet)
        config = Utilities.get_JSON_Obj(self.test_config)
        combos = Generator.sub_vowels('john',leet,config)
        self.assertTrue('j0hn' in combos)



if __name__ == '__main__':
    unittest.main()
