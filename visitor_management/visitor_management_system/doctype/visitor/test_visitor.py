# Copyright (c) 2026, CitiXsys and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import now_datetime

class TestVisitor(FrappeTestCase):
    def test_approval_workflow_transition(self):
        # 1. Create a dummy visitor
        visitor = frappe.get_doc({
            "doctype": "Visitor",
            "full_name": "Test Guest",
            "email": "test@example.com",
            "id_type": "Aadhaar",
            "id_number": "123456789012",
            "expected_arrival": now_datetime(),
            "host_employee": "EMP/001" # Make sure this employee exists in your test DB
        }).insert()

        # Initial state check
        self.assertEqual(visitor.workflow_state, "Pre-Registered")

        # 2. Simulate Receptionist sending for approval
        frappe.workflow.apply_workflow(visitor, "Send for Approval")
        self.assertEqual(visitor.workflow_state, "Pending Approval")

        # 3. Simulate Host Approving
        frappe.workflow.apply_workflow(visitor, "Approve")
        
        # 4. Final Assertions
        self.assertEqual(visitor.workflow_state, "Approved")
        self.assertIsNotNone(visitor.checkin_time) # Check if Python logic worked
        
    def test_aadhaar_validation(self):
        # Test if incorrect Aadhaar throws an error
        visitor = frappe.get_doc({
            "doctype": "Visitor",
            "full_name": "Invalid Aadhaar Guest",
            "id_type": "Aadhaar",
            "id_number": "123" # Too short
        })
        self.assertRaises(frappe.ValidationError, visitor.insert)