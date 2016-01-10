import io
import os
import zipfile
import unittest
from boil import *


def del_if_exists(filename):
    if os.path.isfile(filename):
        os.remove(filename)


class BoilTests(unittest.TestCase):

    def tearDown(self):
        del_if_exists('test1.txt')
        del_if_exists('test2.txt')

    def test_repo_exists(self):
        repos = [
            'tj/n',
            'jquery/jquery',
            'facebook/react',
            'octocat/Spoon-Knife',
            'octocat/octocat.github.io',
            'gaearon/react-hot-boilerplate'
        ]
        for repo in repos:
            self.assertTrue(repo_exists(repo))

    def test_repo_doesnt_exist(self):
        repos = [
            'glifchits/therewillbenosuchrepo',
            'octocat/also_never-a_repo'
        ]
        for repo in repos:
            with self.assertRaises(LookupError):
                repo_exists(repo)

    def test_repo_malformed(self):
        repos = [
            'sdfgdsfgsdf',
            '',
            'sdfgsdfg\\repsdf'
            'sdfs-dfsdfh'
            'one/two/three'
            '/user/repo',
            'user/repo/',
            'https://github.com/user/repo'
        ]
        for repo in repos:
            with self.assertRaises(ValueError):
                repo_exists(repo)

    def test_dump_zip_contents(self):
        self.assertFalse(os.path.exists('test1.txt'))
        self.assertFalse(os.path.exists('test2.txt'))
        self.assertFalse(os.path.exists('tmp'))
        with open('testzipfile.zip', 'rb') as zipfilehandler:
            zipball = zipfile.ZipFile(io.BytesIO(zipfilehandler.read()))
        dump_zip_contents_into_cwd(zipball)
        self.assertTrue(os.path.exists('test1.txt'))
        self.assertTrue(os.path.exists('test2.txt'))
        self.assertFalse(os.path.exists('tmp'))


if __name__ == "__main__":
    unittest.main()
