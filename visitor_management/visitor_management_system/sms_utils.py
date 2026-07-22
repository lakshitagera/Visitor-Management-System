import frappe

def send_sms_stub(receiver_number, message):
    # 1. Check if SMS is enabled in our new Settings DocType
    if not frappe.db.get_single_value("VMS Settings", "enable_sms"):
        return # Do nothing if disabled

    # 2. The "Stub" Log
    # In a real app, you'd put your API request to Twilio/MSG91 here.
    # For now, we log it so we can prove it works.
    frappe.log_error(
        title="SMS Stub Sent",
        message=f"To: {receiver_number}\nMessage: {message}"
    )
    
    # Optional: Show a message to the user for testing
    frappe.msgprint(f"SMS Stub: Message would be sent to {receiver_number}")
    