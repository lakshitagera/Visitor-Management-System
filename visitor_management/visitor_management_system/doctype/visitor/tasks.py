import frappe
from frappe.utils import now_datetime

def check_overstay():
    now = now_datetime()
    
    # 1. Fetch only visitors who are physically on-site
    # 'Checked-in' spelling matches your DocType 

    checked_in = frappe.get_all("Visitor",
        filters={"status": "Checked-in"}, 
        fields=["name", "full_name", "host_employee", "check_in_time"])

    for v in checked_in:
        if not v.check_in_time:
            continue
        
        # 2. Calculate the difference in hours
        on_site_hours = (now - v.check_in_time).total_seconds() / 3600
        
        # 3. If they have been here longer than 8 hours
        if on_site_hours > 8:
            # Direct DB update is faster and bypasses validation errors
            frappe.db.set_value("Visitor", v.name, "status", "Overstay")
            
            # 4. Use try-except so an email error doesn't break the whole loop
            try:
                send_overstay_alert(v)
                print(f"Status updated and alert sent for {v.name}")
            except Exception as e:
                # Log the error but keep the 'Overstay' status saved
                frappe.log_error(f"Alert failed for {v.name}: {e}")
                print(f"Status updated for {v.name}, but email failed.")

    # Important: Commit changes so they show up in the browser
    
    frappe.db.commit()

def send_overstay_alert(visitor):
    # 1. Fetch settings
    security_email = frappe.db.get_single_value('VMS Settings', 'security_email')
    
    # 2. Get the Host's email (Matches your DocType field: company_email)
    host_email = frappe.db.get_value("Employee", visitor.host_employee, "company_email")

    if not security_email and not host_email:
        return 

    # 3. Create the message content
    subject = f"OVERSTAY ALERT: {visitor.full_name} is still on-site"
    message = f"""
        <h3>Security Alert</h3>
        <p>Visitor <b>{visitor.full_name}</b> checked in at {visitor.check_in_time}.</p>
        <p>They have exceeded the 8-hour limit.</p>
        <p><b>Host:</b> {visitor.host_employee}</p>
    """

    # 4. Send the mail (delayed=True prevents immediate crash if server is slow)
    frappe.sendmail(
        recipients=[security_email, host_email],
        subject=subject,
        content=message,
        reference_doctype="Visitor",
        reference_name=visitor.name,
        delayed=True 
    )
    
    # Timeline comment
    frappe.get_doc("Visitor", visitor.name).add_comment("Info", "Overstay alert emails queued.")
