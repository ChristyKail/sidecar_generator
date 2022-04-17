import unittest
import sidecar_generator


class MyTestCase(unittest.TestCase):

    def test_md5_vs_yoyotta(self):
        test_mhl = '/Users/christykail/Desktop/YoYotta_Reports/2022-04-17_1602_Other_CK_SSD_M003R00H.mhl'

        sidecar_generator.SidecarGenerator(test_mhl)

        self.assertEqual(True, True)

        yy_file = '/Users/christykail/Desktop/YoYotta_Reports/2022-04-17_1602_Other_CK_SSD_M003R00H.md5'
        gen_file = '/Users/christykail/Desktop/YoYotta_Reports/CK_SSD.md5'

        with open(yy_file, 'r') as f:
            yy_contents = f.read()

        with open(gen_file, 'r') as f:
            gen_contents = f.read()

        self.assertEqual(gen_contents, yy_contents)


if __name__ == '__main__':
    unittest.main()
