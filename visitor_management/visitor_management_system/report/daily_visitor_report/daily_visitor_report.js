frappe.query_reports["Daily Visitor Report"] = {
    "filters": [
        {
            "fieldname": "report_date",
            "label": __("Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "reqd": 1
        }
    ]
};