# Copyright (c) 2026, CitiXsys and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns = [
        { "label": frappe._("Host (Employee)"), "fieldname": "host", "fieldtype": "Link", "options": "Employee", "width": 200 },
        { "label": frappe._("Total Requests"), "fieldname": "total", "fieldtype": "Int", "width": 120 },
        { "label": frappe._("Approved"), "fieldname": "approved", "fieldtype": "Int", "width": 100 },
        { "label": frappe._("Rejected"), "fieldname": "rejected", "fieldtype": "Int", "width": 100 },
        { "label": frappe._("Approval %"), "fieldname": "rate", "fieldtype": "Percent", "width": 120 }
    ]

    # SQL Math: Count specific statuses per Host
    data = frappe.db.sql(f"""
        SELECT 
            host_employee as host,
            COUNT(*) as total,
            SUM(CASE WHEN status = 'Approved' THEN 1 ELSE 0 END) as approved,
            SUM(CASE WHEN status = 'Rejected' THEN 1 ELSE 0 END) as rejected,
            (SUM(CASE WHEN status = 'Approved' THEN 1 ELSE 0 END) / COUNT(*)) * 100 as rate
        FROM `tabVisitor`
        WHERE creation BETWEEN '{filters.from_date} 00:00:00' AND '{filters.to_date} 23:59:59'
        GROUP BY host_employee
        ORDER BY total DESC
    """, as_dict=True)

    return columns, data

