import frappe

@frappe.whitelist()
def get_dashboard_data(filters=None):
    if isinstance(filters, str):
        filters = frappe.parse_json(filters)
    
    conditions = []
    
    # --- SERVER-SIDE SECURITY FILTER ---
    # If the user is a 'Host' (Employee), they should only see their visitors.
    # We check if they are NOT a System Manager.
    
    if "System Manager" not in frappe.get_roles():
        # Find the Employee record linked to the current user's email
        user_employee = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name")
        if user_employee:
            conditions.append(f"host_employee = '{user_employee}'")
        else:
            # If no employee record is found, return empty to prevent data leaks
            return {"counts": []}
    # -----------------------------------

    # Apply UI filters on top of the security filter
    if filters.get("status"):
        conditions.append(f"status = '{filters.get('status')}'")
    if filters.get("host") and "System Manager" in frappe.get_roles():
        # Managers can filter by any host; regular hosts are locked to themselves
        conditions.append(f"host_employee = '{filters.get('host')}'")
    if filters.get("date"):
        conditions.append(f"DATE(creation) = '{filters.get('date')}'")

    where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""

    counts = frappe.db.sql(f"""
        SELECT status, COUNT(*) as count 
        FROM `tabVisitor` 
        {where_clause}
        GROUP BY status
    """, as_dict=True)
    
    return {"counts": counts}