# Copyright (c) 2026, CitiXsys and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    if not filters:
        filters = {}

    columns = [
        { "label": frappe._("Visitor Name"), "fieldname": "full_name", "fieldtype": "Data", "width": 200 },
        { "label": frappe._("Mobile"), "fieldname": "phone_number", "fieldtype": "Data", "width": 150 },
        { "label": frappe._("Total Visits"), "fieldname": "visit_count", "fieldtype": "Int", "width": 120 },
        { "label": frappe._("Last Visit Date"), "fieldname": "last_visit", "fieldtype": "Datetime", "width": 180 }
    ]

    # Logic: Group by phone_number and count occurrences
    # Filter by the date range selected by the user
    min_visits = filters.get("min_visits") or 2
    
    data = frappe.db.sql(f"""
        SELECT 
            full_name, 
            phone_number, 
            COUNT(*) as visit_count, 
            MAX(creation) as last_visit
        FROM `tabVisitor`
        WHERE creation BETWEEN '{filters.from_date} 00:00:00' AND '{filters.to_date} 23:59:59'
        GROUP BY phone_number
        HAVING visit_count >= {min_visits}
        ORDER BY visit_count DESC
    """, as_dict=True)

    return columns, data
 