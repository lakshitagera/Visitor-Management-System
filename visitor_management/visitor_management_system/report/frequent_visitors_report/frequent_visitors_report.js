// Copyright (c) 2026, CitiXsys and contributors
// For license information, please see license.txt

frappe.query_reports["Frequent Visitors Report"] = {
    "filters": [
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -3),
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
            "fieldname": "min_visits",
            "label": __("Minimum Visits"),
            "fieldtype": "Int",
            "default": 2
        }
    ]
};