import frappe

def execute(filters=None):
    if not filters:
        filters = {}

    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        { "label": frappe._("Date"), "fieldname": "creation", "fieldtype": "Datetime", "width": 150 },
        { "label": frappe._("Visitor ID"), "fieldname": "name", "fieldtype": "Link", "options": "Visitor", "width": 120 },
        { "label": frappe._("Full Name"), "fieldname": "full_name", "fieldtype": "Data", "width": 150 },
        { "label": frappe._("Host"), "fieldname": "host_employee", "fieldtype": "Link", "options": "Employee", "width": 150 },
        { "label": frappe._("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100 },
        { "label": frappe._("Purpose"), "fieldname": "purpose", "fieldtype": "Data", "width": 150 }
    ]

def get_data(filters):
    conditions = []
    
    # 1. Date Range (Required)
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    conditions.append(f"creation BETWEEN '{from_date} 00:00:00' AND '{to_date} 23:59:59'")
    
    # 2. Text Search Filters (Optional)
    if filters.get("visitor_name"):
        conditions.append(f"full_name LIKE '%{filters.get('visitor_name')}%'")
    
    if filters.get("purpose"):
        conditions.append(f"purpose LIKE '%{filters.get('purpose')}%'")

    # 3. Exact Match Filters (Optional)
    if filters.get("host"):
        conditions.append(f"host_employee = '{filters.get('host')}'")
    
    if filters.get("status"):
        conditions.append(f"status = '{filters.get('status')}'")

    # 4. Security: Host Privacy Filter
    if "System Manager" not in frappe.get_roles():
        user_employee = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name")
        if user_employee:
            conditions.append(f"host_employee = '{user_employee}'")
        else:
            return [] # No employee link found, show nothing for safety

    where_clause = " WHERE " + " AND ".join(conditions)

    return frappe.db.sql(f"""
        SELECT creation, name, full_name, host_employee, status, purpose
        FROM `tabVisitor`
        {where_clause}
        ORDER BY creation DESC
    """, as_dict=True)