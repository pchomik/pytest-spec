# -*- coding: utf-8 -*-
"""
:author: Pawel Chomicki
:e-mail: pawel.chomicki@gmail.com
"""
import unittest


def describe_first_level():

    def it_passed_on_first_level():
        assert True is True

    @unittest.skip('To implement')
    def it_skipped_on_first_level():
        assert True is True

    @unittest.skip('Remove docorator to see fail result')
    def it_failed_on_first_level():
        assert True is False

    def describe_second_level():

        def it_passed_on_second_level():
            assert True is True

        @unittest.skip('To implement')
        def it_skipped_on_second_level():
            assert True is True

        @unittest.skip('Remove docorator to see fail result')
        def it_failed_on_second_level():
            assert True is False

        def describe_third_level():

            def it_passed_on_third_level():
                assert True is True

            @unittest.skip('To implement')
            def it_skipped_on_third_level():
                assert True is True

            @unittest.skip('Remove docorator to see fail result')
            def it_failed_on_third_level():
                assert True is False

    def describe_second_level_again():

        def it_passed_on_second_level():
            assert True is True

        @unittest.skip('To implement')
        def it_skipped_on_second_level():
            assert True is True

        @unittest.skip('Remove docorator to see fail result')
        def it_failed_on_second_level():
            assert True is False


def describe_first_level_again():

    def it_passed_on_first_level():
        assert True is True

    @unittest.skip('To implement')
    def it_skipped_on_first_level():
        assert True is True

    @unittest.skip('Remove docorator to see fail result')
    def it_failed_on_first_level():
        assert True is False


if __name__ == '__main__':
    unittest.main()
