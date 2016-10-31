# pylint: disable=unused-variable,unused-argument,expression-not-assigned,singleton-comparison

import pytest
from expecter import expect

from kcards.models import Room, Card, Color


def describe_room():

    @pytest.fixture
    def room():
        return Room(code='foobar')

    def describe_init():

        def it_generates_an_id_when_unspecified():
            room1 = Room()
            room2 = Room()

            expect(room1) != room2

    def describe_sort():

        def it_uses_the_id():
            rooms = [Room(code='1'), Room(code='A'), Room(code='a')]

            expect(sorted(rooms)) == rooms

    def describe_code():

        def it_matches_the_id(room):
            expect(room.code) == 'foobar'

    def describe_queue():

        @pytest.fixture
        def filled_room(room):
            room.green = ["Bob", "Joe"]
            room.yellow = ["John", "Fred"]
            return room

        def when_empty(room):
            expect(room.queue) == []

        def when_active(filled_room):
            filled_room.active = True

            expect(filled_room.queue) == [
                Card("John", Color.yellow),
                Card("Fred", Color.yellow),
                Card("Bob", Color.green),
                Card("Joe", Color.green),
            ]

        def when_inactive(filled_room):
            filled_room.active = False

            expect(filled_room.queue) == [
                Card("Bob", Color.green),
                Card("John", Color.yellow),
                Card("Fred", Color.yellow),
                Card("Joe", Color.green),
            ]

    def describe_add_card():

        def with_single_card(room):
            room.add_card("John Doe", Color.green)

            expect(room.queue) == [
                Card("John Doe", Color.green),
            ]

        def with_multiple_cards(room):
            room.add_card("John Doe", Color.yellow)
            room.add_card("Jace Browning", Color.green)
            room.add_card("Dan Lindeman", Color.yellow)

            expect(room.queue) == [
                Card("John Doe", Color.yellow),
                Card("Dan Lindeman", Color.yellow),
                Card("Jace Browning", Color.green),
            ]

        def with_red_card(room):
            room.add_card("John Doe", Color.green)
            room.add_card("Jace Browning", Color.yellow)
            room.add_card("Dan Lindeman", Color.red)

            expect(room.queue) == [
                Card("Dan Lindeman", Color.red),
                Card("John Doe", Color.green),
                Card("Jace Browning", Color.yellow),
            ]

    def describe_next_speaker():

        def it_leaves_empty_rooms_unchanged(room):
            room.next_speaker()

            expect(room.queue) == []

        def it_removes_interrupts_first(room):
            room.add_card("John Doe", Color.green)
            room.add_card("Jace Browning", Color.red)

            room.next_speaker()

            expect(room.queue) == [
                Card("John Doe", Color.green),
            ]

        def it_can_start_a_new_thread(room):
            room.add_card("Jace Browning", Color.green)
            room.add_card("John Doe", Color.yellow)
            room.add_card("Dan Lindeman", Color.green)

            room.next_speaker()

            expect(room.queue) == [
                Card("John Doe", Color.yellow),
                Card("Dan Lindeman", Color.green),
            ]

        def it_removes_the_next_followup(room):
            room.add_card("Jace Browning", Color.yellow)
            room.add_card("Dan Lindeman", Color.yellow)

            room.next_speaker()

            expect(room.queue) == [
                Card("Dan Lindeman", Color.yellow)
            ]

        def it_removes_the_last_followup(room):
            room.add_card("John Doe", Color.yellow)
            room.add_card("Jace Browning", Color.green)

            room.next_speaker()

            expect(room.queue) == [
                Card("Jace Browning", Color.green),
            ]

        def it_can_advance_to_the_next_topic(room):
            room.add_card("John Doe", Color.green)
            room.add_card("Dan Lindeman", Color.green)

            room.next_speaker()

            expect(room.queue) == [
                Card("Dan Lindeman", Color.green),
            ]

        def it_clears_the_queue_without_active_discussion(room):
            room.add_card("John Doe", Color.green)
            room.add_card("Dan Lindeman", Color.green)

            room.next_speaker()
            room.next_speaker()

            expect(room.queue) == []

        def it_clears_the_queue_with_active_discussion(room):
            room.add_card("John Doe", Color.green)
            room.add_card("Jace Browning", Color.yellow)
            room.add_card("Dan Lindeman", Color.green)

            room.next_speaker()
            room.next_speaker()
            room.next_speaker()

            expect(room.queue) == []
