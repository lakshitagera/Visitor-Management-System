# Copyright (c) 2026, CitiXsys and contributors
# For license information, please see license.txt

import frappe
from frappe import _ 
from frappe.model.document import Document
from frappe.utils import nowdate, now_datetime, today, format_time 
from visitor_management.visitor_management_system.sms_utils import send_sms_stub

class Visitor(Document):
    def validate(self):
        # --- 1. SYNC STATUS WITH WORKFLOW ---
        if self.workflow_state:
            self.status = self.workflow_state

        # 1. Phone Number Validation
        if self.phone_number:
            # Remove any spaces or dashes the user might have typed
            clean_phone = str(self.phone_number).replace(" ", "").replace("-", "")
            
            # Logic: If it looks like an Indian number (starts with 6-9 or +91)
            # or if the user didn't specify a country code, we enforce 10 digits.
            if len(clean_phone) < 10:
                frappe.throw(_("Phone number must be at least 10 digits."))
            
            # If it's exactly 10 digits, we assume it's a standard Indian mobile number
            # If it's longer than 10, we treat it as an International number (with country code)
            if len(clean_phone) > 15:
                frappe.throw(_("Phone number cannot exceed 15 digits."))

        # --- 2. ID VALIDATION ---
        if self.id_type == "Aadhaar":
            # Validation logic remains, but actual ID digits are never output by the AI
            if not self.id_number or len(str(self.id_number)) != 12:
                frappe.throw("Aadhaar number must be exactly 12 digits")

        # --- 3. FIELD VALIDATION ---
        if not self.expected_arrival:
            frappe.throw("Please select an Expected Arrival time")

        # --- 4. SECURITY GATE & PHYSICAL CHECK-IN ---
        if self.workflow_state == "Checked-in":
            # Security Check
            current_db_status = frappe.db.get_value("Visitor", self.name, "status")
            if current_db_status in ["Rejected", "Expired"]:
                frappe.throw(f"Access Denied: Cannot check-in a visitor with {current_db_status} status.")
            
            # PHYSICAL TIMESTAMP: Only recorded when they actually check in
            if not self.check_in_time:
                self.check_in_time = now_datetime()
                frappe.msgprint(f"Check-in successful! Timestamp recorded: {format_time(self.check_in_time)}")

        # --- 5. APPROVAL & SMS LOGIC (NO TIMESTAMP HERE) ---
        if self.workflow_state == "Approved":
            # We only send the message, we DON'T record check_in_time yet
            sms_enabled = frappe.db.get_single_value('VMS Settings', 'enable_sms')
            if sms_enabled and self.phone_number:
                send_sms_stub(self.phone_number, f"Hi {self.full_name}, your entry is approved! Please show this at the gate.")

        # --- 6. CHECK-OUT LOGIC ---
        if self.workflow_state == "Checked-out" and not self.check_out_time:
            self.check_out_time = now_datetime()
            
            if self.check_in_time:
                diff_seconds = frappe.utils.time_diff_in_seconds(self.check_out_time, self.check_in_time)
                self.visit_duration = diff_seconds / 60
                
            frappe.msgprint(f"Visitor Checked-out. Duration: {int(self.visit_duration)} minutes.")

        # --- 7. DELEGATION ---
        if self.workflow_state == "Pending Approval":
            self.check_for_delegation()

    def before_save(self):
        # Auto-generate Badge Number
        if not self.badge_number:
            year = nowdate().split('-')[0]
            self.badge_number = frappe.model.naming.make_autoname(f"BADGE-{year}-.####")

        # Fallback to ensure status is updated correctly
        if self.workflow_state == "Checked-in" and not self.check_in_time:
           self.check_in_time = now_datetime()
           self.status = "Checked-in"

    def check_for_delegation(self):
        delegation = frappe.get_value("Host Delegation", 
            {
                "employee": self.host_employee,
                "status": "Active",
                "from_date": ["<=", today()],
                "to_date": [">=", today()]
            }, 
            "delegate_employee"
        )
        
        if delegation:
            frappe.msgprint(f"Note: Approval request sent to {delegation} (Delegate).")
    
    def on_update(self):
       # This triggers the 'vms_dashboard_refresh' event in the browser
       frappe.publish_realtime("vms_dashboard_refresh")
    