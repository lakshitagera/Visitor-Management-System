import frappe
from frappe.utils import now_datetime, time_diff_in_seconds

def check_visitor_timeouts():
    # Fetch visitors who are still "Pending Approval"
    pending_visitors = frappe.get_all("Visitor", 
        filters={"workflow_state": "Pending Approval", "docstatus": 0},
        fields=["name", "full_name", "creation", "host_employee", "reminder_sent", "escalation_sent"])

    now = now_datetime()

    for v in pending_visitors:
        # Calculate waiting time in minutes
        wait_time = time_diff_in_seconds(now, v.creation) / 60
        
        # --- 30 MINUTE REMINDER ---
        # Logic: If wait time is at least 30 mins AND we haven't sent the reminder yet
        if wait_time >= 30 and not v.reminder_sent:
            doc = frappe.get_doc("Visitor", v.name)
            notification = frappe.get_doc("Notification", "Approval Reminder - Host")
            notification.send(doc)
            
            # Use db_set to update the value immediately without triggering full save logic
            frappe.db.set_value("Visitor", v.name, "reminder_sent", 1)
            frappe.db.commit() # Force save so the next block knows this is done

        # --- 60 MINUTE ESCALATION ---
        # Logic: If wait time is at least 60 mins AND we haven't sent escalation yet 
        if wait_time >= 60 and not v.escalation_sent:
            doc = frappe.get_doc("Visitor", v.name)
            notification = frappe.get_doc("Notification", "Visitor Approval Escalation")
            notification.send(doc)
            
            frappe.db.set_value("Visitor", v.name, "escalation_sent", 1)
            frappe.db.commit()


        # --- 480 MINUTE OVERSTAY LOGIC ---
        # Calculate if they have stayed past their welcome
        # if wait_time >= 480 and v.workflow_state == "Checked-in":
        #     v_doc = frappe.get_doc("Visitor", v.name)
            
        #     # This 'apply_workflow_action' ensures the Heading turns Dark Brown/Red
        #     from frappe.model.workflow import apply_workflow_action
            
        #     # Make sure "Mark Overstay" is the exact Action name in your Workflow Transitions
        #     apply_workflow_action(v_doc, "Mark Overstay")
            
        #     # Sync the status field just to be safe
        #     v_doc.status = "Overstay"
        #     v_doc.save()
            
        #     # Logging for your terminal test
        #     print(f"Visitor {v.name} has been marked as Overstay.")

        # --- FINAL SYNC: FORCE HEADING TO MATCH STATUS ---
    # Fetch all visitors who are marked as Overstay in the status field
    overstay_visitors = frappe.get_all("Visitor", 
        filters={"status": "Overstay", "workflow_state": ["!=", "Overstay"]},
        fields=["name"]
    )

    for ov in overstay_visitors:
        # Force the Workflow Heading to match the Status
        frappe.db.set_value("Visitor", ov.name, "workflow_state", "Overstay")
        print(f"Force synced heading for {ov.name}")

    frappe.db.commit()
    