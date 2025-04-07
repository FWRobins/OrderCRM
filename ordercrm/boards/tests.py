from django.contrib.auth.models import User
from django.test import TestCase

from boards.models import Board, Invite, Favorite


class BoardsTestCase(TestCase):
    def setUp(self):
        # Create users
        self.john = User.objects.create_user(
            username="john",
            email="john@example.com",
            password="j0hn"
        )
        self.mindy = User.objects.create_user(
            username="mindy",
            email="mindy@example.com",
            password="m1ndy"
        )
        self.kylie = User.objects.create_user(
            username="kylie",
            email="kylie@example.com",
            password="kyli3"
        )

        self.board1 = Board.objects.create(title="Board 1", owner=self.john)
        self.board2 = Board.objects.create(title="Board 2", owner=self.john)
        self.board3 = Board.objects.create(title="Board 3", owner=self.mindy)

        Invite.objects.create(user=self.john, board=self.board3)
        Invite.objects.create(user=self.mindy, board=self.board1)

        # Invite mindy to her own board
        Invite.objects.create(user=self.mindy, board=self.board3)

        Invite.objects.create(user=self.kylie, board=self.board2)
        Invite.objects.create(user=self.kylie, board=self.board3)

        # john favorited all the boards he has access to
        Favorite.objects.create(user=self.john, board=self.board1)
        Favorite.objects.create(user=self.john, board=self.board2)
        Favorite.objects.create(user=self.john, board=self.board3)

        # mindy favorited none

        # kylie favorited 1 (not available) and 2
        Favorite.objects.create(user=self.kylie, board=self.board1)
        Favorite.objects.create(user=self.kylie, board=self.board2)

    def test_get_available_boards(self):
        # - john -
        available_boards_for_john = Board.get_available(self.john)
        expected_available_boards_for_john = Board.objects.filter(
            pk__in=[self.board1.pk, self.board2.pk, self.board3.pk])

        self.assertQuerysetEqual(
            available_boards_for_john,
            expected_available_boards_for_john,
            ordered=False,
        )

        # - mindy -
        available_boards_for_mindy = Board.get_available(self.mindy)
        expected_available_boards_for_mindy = Board.objects.filter(
            pk__in=[self.board1.pk, self.board3.pk])

        self.assertQuerysetEqual(
            available_boards_for_mindy,
            expected_available_boards_for_mindy,
            ordered=False,
        )

        # - kylie -
        available_boards_for_kylie = Board.get_available(self.kylie)
        expected_available_boards_for_kylie = Board.objects.filter(
            pk__in=[self.board2.pk, self.board3.pk])

        self.assertQuerysetEqual(
            available_boards_for_kylie,
            expected_available_boards_for_kylie,
            ordered=False,
        )

    def test_get_favorite_boards(self):
        # - john -
        favorite_boards_for_john = Board.get_favorites(self.john)
        expected_favorite_boards_for_john = Board.objects.filter(
            pk__in=[self.board1.pk, self.board2.pk, self.board3.pk])

        self.assertQuerysetEqual(
            favorite_boards_for_john,
            expected_favorite_boards_for_john,
            ordered=False,
        )

        # - mindy -
        favorite_boards_for_mindy = Board.get_favorites(self.mindy)
        expected_favorite_boards_for_mindy = Board.objects.none()

        self.assertQuerysetEqual(
            favorite_boards_for_mindy,
            expected_favorite_boards_for_mindy,
            ordered=False,
        )

        # - kylie -
        favorite_boards_for_kylie = Board.get_favorites(self.kylie)
        expected_favorite_boards_for_kylie = Board.objects.filter(
            pk__in=[self.board2.pk])

        self.assertQuerysetEqual(
            favorite_boards_for_kylie,
            expected_favorite_boards_for_kylie,
            ordered=False,
        )