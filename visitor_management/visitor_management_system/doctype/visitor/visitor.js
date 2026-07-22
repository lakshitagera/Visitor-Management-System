// Copyright (c) 2026, CitiXsys and contributors
// For license information, please see license.txt

frappe.listview_settings['Visitor'] = {
    get_indicator: function(doc) {
        const status_colors = {
            "Pending Approval": "#BA7517", // Brownish/Orange
            "Approved": "#185FA5",         // Blue
            "Checked-in": "#1D9E75",       // Green
            "Checked-out": "#5F5E5A",      // Grey
            "Rejected": "#A32D2D",         // Red
            "Expired": "#888",             // Greyish
            "Overstay": "#712B13",         // Dark Brown
            "Pre-Registered": "#534AB7"    // Purple
        };

        return [__(doc.status), status_colors[doc.status] || "grey", "status,=," + doc.status];
    }
};

frappe.ui.form.on('Visitor', { 

    phone_number: function(frm) {
        if (frm.doc.phone_number) {
            let phone = frm.doc.phone_number.replace(/\D/g, ''); // removes non-digits
            
            if (phone.length < 10) {
                frappe.msgprint(__('Please enter a valid 10-digit mobile number or a full international number with country code.'));
            }
        }
    },

    full_name: function(frm) {
        if (frm.doc.full_name) {
            let capitalized = frm.doc.full_name.toLowerCase().replace(/\b\w/g, l => l.toUpperCase());
            if (frm.doc.full_name !== capitalized) {
                frm.set_value('full_name', capitalized);
            }
        }
    },

    refresh: function(frm) {
        console.log("Visitor Form Refreshing - Status: ", frm.doc.status); 

        // Add Shortcut to Dashboard
        // This button will now try the route and log it to the console
        frm.add_custom_button(__('Open Dashboard'), function() {
            console.log("Attempting to route to dashboard...");
            frappe.set_route('vms-dashboard'); 
        }, __("Actions"))
        
        handle_rejection_ui(frm);

        if (frm.is_new()) {
            frappe.db.get_single_value('Visitor Settings', 'nda_text')
                .then(nda_text => {
                    if (nda_text) {
                        frm.set_df_property('nda_acknowledged', 'description', 
                            `<b>Terms of Entry:</b><br>${nda_text}`);
                    }
                });
        }
    },

    // 2. STATUS TRIGGER
    status: function(frm) {
        handle_rejection_ui(frm);

        if (frm.doc.status === 'Rejected') {
            frappe.msgprint({
                title: __('Reason Required'),
                message: __('Please explain why this visit was rejected.'),
                indicator: 'orange'
            });
        }
    },

    // 3. NDA TRIGGER
    nda_acknowledged: function(frm) {
        if (frm.doc.nda_acknowledged) {
            frappe.show_alert({
                message: __('NDA Acknowledged successfully'),
                indicator: 'green'
            });
        }
    },

    // 4. HOST EMPLOYEE TRIGGER
    host_employee: function(frm) {
        if (frm.doc.host_employee) {
            frappe.call({
                method: 'frappe.client.get_value',
                args: {
                    doctype: 'Host Delegation',
                    filters: {
                        employee: frm.doc.host_employee,
                        status: 'Active',
                        from_date: ['<=', frappe.datetime.get_today()],
                        to_date: ['>=', frappe.datetime.get_today()]
                    },
                    fieldname: 'delegate_employee'
                },
                callback: function(r) {
                    if (r.message && r.message.delegate_employee) {
                        frappe.msgprint({
                            title: __('Host on Leave'),
                            indicator: 'blue',
                            message: __('<b>{0}</b> is currently away. Please contact the delegate <b>{1}</b> for approval.', 
                                [frm.doc.host_employee, r.message.delegate_employee])
                        });
                    }
                }
            });
        }
    }
});


// --- HELPER FUNCTIONS ---
function handle_rejection_ui(frm) {
    let is_rejected = (frm.doc.status === 'Rejected');

    // Toggle Visibility
    frm.toggle_display('rejection_reason', is_rejected);

    // Set Mandatory only if status is Rejected
    frm.set_df_property('rejection_reason', 'reqd', is_rejected);
}


