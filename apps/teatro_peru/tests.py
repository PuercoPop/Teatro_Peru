# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from .models import Ticket, CastMember


class ValidateCastMember(TestCase):
    def setUp(self):
        self.client = Client()

    def test_incomplete_parameters(self):
        """
        Missing at least one parameter
        """
        response = self.client.post(
            reverse("validate_cast_member"),
            {'name': None,
             'role': None,},
            )
        self.assertEqual(response.status_code, 400)
        response = self.client.post(
            reverse("validate_cast_member"),
            {'name': "Pepe X",
             'role': None,},
            )
        self.assertEqual(response.status_code, 400)
        response = self.client.post(
            reverse("validate_cast_member"),
            {'name': None,
             'role': "Fotografía",},
            )
        self.assertEqual(response.status_code, 400)

    def test_invalid_parameters(self):
        response = self.client.post(
            reverse("validate_cast_member"),
            {'name': 1,
             'role': "Fotografía",},
            )
        self.assertEqual(response.status_code, 400)
    def test_successful_case(self):
        response = self.client.post(
            reverse("validate_cast_member"),
            {'name': "Pepe X",
             'role': "Fotografía",},
            )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context.get('m_elenco'), CastMember)


class ValidateTicket(TestCase):
    def setUp(self):
        self.client = Client()

    def test_incomplete_parameters(self):
        response = self.client.post(
            reverse("validate_ticket"),
            {'name': None,
             'cost': None,},
            )
        self.assertEqual(response.status_code, 400)

    def test_invalid_parameters(self):
        response = self.client.post(
            reverse("validate_ticket"),
            {'name': None,
             'cost': "Garbage",},
            )
        self.assertEqual(response.status_code, 400)

    def test_successful_case(self):
        """
        Verify the 200 status code and the html type
        """
        response = self.client.post(
            reverse("validate_ticket"),
            {'name': "Vip", 'cost': 100,},
            )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context.get('m_entrada'), Ticket)
