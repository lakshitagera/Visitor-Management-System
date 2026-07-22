// Copyright (c) 2026, CitiXsys and contributors
// For license information, please see license.txt

frappe.query_reports["Visitor History Log"] = {
    "filters": [
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
            "reqd": 1
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "reqd": 1
        },
        {
            "fieldname": "visitor_name",
            "label": __("Visitor Name"),
            "fieldtype": "Data"
        },
        {
            "fieldname": "host",
            "label": __("Host"),
            "fieldtype": "Link",
            "options": "Employee"
        },
        {
            "fieldname": "status",
            "label": __("Status"),
            "fieldtype": "Select",
            "options": ["", "Pre-Registered", "Pending Approval", "Approved", "Checked-In", "Checked-Out", "Rejected", "Expired", "Overstay"]
        },
        {
            "fieldname": "purpose",
            "label": __("Purpose"),
            "fieldtype": "Data"
        }
    ]
};
