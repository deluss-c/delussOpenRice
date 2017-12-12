import unittest
from delussOpenRice.scraper import models


class TestScraper(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_restaurant_urls(self):
        expected = ['https://www.openrice.com/en/hongkong/r-sen-ryo-causeway-bay-japanese-sushi-sashimi-r109052',
                    'https://www.openrice.com/en/hongkong/r-sen-ryo-causeway-bay-japanese-sushi-sashimi-r25834',
                    'https://www.openrice.com/en/hongkong/r-sen-ryo-causeway-bay-japanese-sushi-sashimi-r453124']
        ors = models.openRiceScraper()
        r = ors.fetch("https://www.openrice.com/en/hongkong/restaurants?where=causeway+bay&what=sen-ryo")
        urls = ors.get_restaurant_urls(r)
        self.assertEqual(urls, expected)

    def test_get_restaurant_data(self):
        expected = {
            'chinese_address': u'\u9285\u947c\u7063\u8ed2\u5c3c\u8a69\u9053500\u865f\u5e0c\u614e\u5ee3\u583413\u6a131304-05\u865f\u8216',
            'english_name': u'sen-ryo',
            'tags': u'Japanese,Sushi/Sashimi,Sushi Bar',
            'photo_number': u'693',
            'chinese_name': u'\u5343\u4e21',
            'english_address': u'Shop 1304-05, 13/F, Hysan Place, 500 Hennessy Road, Causeway Bay'}
        ors = models.openRiceScraper()
        r = ors.fetch("https://www.openrice.com/en/hongkong/r-sen-ryo-causeway-bay-japanese-sushi-sashimi-r109052")
        urls = ors.get_restaurant_data(r)
        self.assertEqual(urls, expected)


if __name__ == '__main__':
    unittest.main()
