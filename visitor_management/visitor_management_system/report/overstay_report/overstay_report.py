# Copyright (c) 2026, CitiXsys and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    if not filters:
        filters = {}

    columns = [
        { "label": frappe._("Visitor"), "fieldname": "name", "fieldtype": "Link", "options": "Visitor", "width": 120 },
        { "label": frappe._("Visitor Name"), "fieldname": "full_name", "fieldtype": "Data", "width": 150 },
        { "label": frappe._("Host"), "fieldname": "host_employee", "fieldtype": "Link", "options": "Employee", "width": 150 },
        { "label": frappe._("Check-In Time"), "fieldname": "check_in_time", "fieldtype": "Datetime", "width": 160 },
        { "label": frappe._("Purpose"), "fieldname": "purpose", "fieldtype": "Data", "width": 150 }
    ]

    # Conditions: Only 'Overstay' status within the date range
    conditions = [
        "status = 'Overstay'",
        f"creation BETWEEN '{filters.from_date} 00:00:00' AND '{filters.to_date} 23:59:59'"
    ]

    # Security: Non-managers only see their own visitors' overstays
    if "System Manager" not in frappe.get_roles(frappe.session.user):
        user_employee = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name")
        if user_employee:
            conditions.append(f"host_employee = '{user_employee}'")
        else:
            return [], []

    where_clause = " WHERE " + " AND ".join(conditions)

    data = frappe.db.sql(f"""
        SELECT name, full_name, host_employee, check_in_time, purpose
        FROM `tabVisitor`
        {where_clause}
        ORDER BY check_in_time ASC
    """, as_dict=True)

    return columns, data