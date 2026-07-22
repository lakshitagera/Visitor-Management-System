import frappe

def execute(filters=None):
    if not filters:
        filters = {}
    
    # If no date is selected yet, use today's date
    report_date = filters.get("report_date") or frappe.utils.today()
    
    columns = get_columns()
    data = get_data(report_date)
    
    return columns, data

def get_columns():
    return [
        { "label": frappe._("Visitor ID"), "fieldname": "name", "fieldtype": "Link", "options": "Visitor", "width": 120 },
        { "label": frappe._("Full Name"), "fieldname": "full_name", "fieldtype": "Data", "width": 150 },
        { "label": frappe._("Host"), "fieldname": "host_employee", "fieldtype": "Link", "options": "Employee", "width": 150 },
        { "label": frappe._("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100 },
        { "label": frappe._("Purpose"), "fieldname": "purpose", "fieldtype": "Small Text", "width": 180 }
    ]

def get_data(report_date):
    # Fetching all records created on the specific selected day
    return frappe.db.get_all("Visitor", 
        filters={
            "creation": ["between", [f"{report_date} 00:00:00", f"{report_date} 23:59:59"]]
        },
        fields=["name", "full_name", "host_employee", "status", "purpose"]
    )

def get_data(report_date):
    conditions = {
        "creation": ["between", [f"{report_date} 00:00:00", f"{report_date} 23:59:59"]]
    }

    # Security check: If not a Manager, restrict to their own visits
    if "System Manager" not in frappe.get_roles():
        user_employee = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name")
        if user_employee:
            conditions["host_employee"] = user_employee

    return frappe.db.get_all("Visitor", 
        filters=conditions,
        fields=["name", "full_name", "host_employee", "status", "purpose"]
    )