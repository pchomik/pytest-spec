"""
:author: Pawel Chomicki
:e-mail: pawel.chomicki@gmail.com
"""

import unittest


def describe_first_level():
    def it_passed_on_first_level():
        assert True is True

    @unittest.skip("To implement")
    def it_skipped_on_first_level():
        assert True is True

    @unittest.skip("Remove docorator to see fail result")
    def it_failed_on_first_level():
        assert True is False

    def it_passed_with_custom_message_on_first_level():
        """Shows custom message from docstring summary"""
        assert True is True

    def it_passed_with_multiline_docstring_on_first_level():
        """
        Shows custom multiline message from docstring summary

        And doesn't show additional info.
        """
        assert True is True

    def describe_second_level():
        def it_passed_on_second_level():
            assert True is True

        @unittest.skip("To implement")
        def it_skipped_on_second_level():
            assert True is True

        @unittest.skip("Remove docorator to see fail result")
        def it_failed_on_second_level():
            assert True is False

        def it_passed_with_custom_message_on_second_level():
            """Shows custom message from docstring summary"""
            assert True is True

        def it_passed_with_multiline_docstring_on_second_level():
            """
            Shows custom multiline message from docstring summary

            And doesn't show additional info.
            """
            assert True is True

        def describe_third_level():
            def it_passed_on_third_level():
                assert True is True

            @unittest.skip("To implement")
            def it_skipped_on_third_level():
                assert True is True

            @unittest.skip("Remove docorator to see fail result")
            def it_failed_on_third_level():
                assert True is False

            def it_passed_with_custom_message_on_third_level():
                """Shows custom message from docstring summary"""
                assert True is True

            def it_passed_with_multiline_docstring_on_third_level():
                """
                Shows custom multiline message from docstring summary

                And doesn't show additional info.
                """
                assert True is True

    def describe_second_level_again():
        def it_passed_on_second_level():
            assert True is True

        @unittest.skip("To implement")
        def it_skipped_on_second_level():
            assert True is True

        @unittest.skip("Remove docorator to see fail result")
        def it_failed_on_second_level():
            assert True is False


def describe_first_level_again():
    def it_passed_on_first_level():
        assert True is True

    @unittest.skip("To implement")
    def it_skipped_on_first_level():
        assert True is True

    @unittest.skip("Remove docorator to see fail result")
    def it_failed_on_first_level():
        assert True is False


if __name__ == "__main__":
    unittest.main()
