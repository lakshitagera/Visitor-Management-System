frappe.pages["vms-dashboard"].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: __("Visitor Dashboard"),
        single_column: true
    });

    const all_statuses = [
        "Pre-Registered", "Pending Approval", "Approved",
        "Checked-In", "Checked-Out", "Rejected",
        "Expired", "Overstay"
    ];

    const status_config = {
        "Pre-Registered":   { color: "#534AB7", bg: "#F0EFFB", icon: "✦", label: "Pre-Registered" },
        "Pending Approval": { color: "#BA7517", bg: "#FEF6E9", icon: "◎", label: "Pending Approval" },
        "Approved":         { color: "#185FA5", bg: "#EBF3FB", icon: "◉", label: "Approved" },
        "Checked-In":       { color: "#1D9E75", bg: "#E8F8F3", icon: "▲", label: "Checked-In" },
        "Checked-Out":      { color: "#5F5E5A", bg: "#F4F4F3", icon: "▼", label: "Checked-Out" },
        "Rejected":         { color: "#A32D2D", bg: "#FBECec", icon: "✕", label: "Rejected" },
        "Expired":          { color: "#888888", bg: "#F5F5F5", icon: "◌", label: "Expired" },
        "Overstay":         { color: "#C0392B", bg: "#FDF0EF", icon: "⚠", label: "Overstay" }
    };

    if (!document.getElementById("vms-dashboard-styles")) {
        const style = document.createElement("style");
        style.id = "vms-dashboard-styles";
        style.textContent = `
            @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,300&family=DM+Mono:wght@400;500&display=swap');

            .vms-dashboard-wrap {
                padding: 28px 24px 40px;
                font-family: 'DM Sans', sans-serif;
            }

            .vms-dashboard-header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 20px;
                padding-bottom: 20px;
                border-bottom: 1px solid #EBEBEB;
            }

            .vms-header-left h2 {
                font-family: 'DM Sans', sans-serif;
                font-size: 22px;
                font-weight: 700;
                color: #1A1A2E;
                margin: 0 0 4px 0;
                letter-spacing: -0.4px;
            }

            .vms-header-left p {
                font-size: 13px;
                color: #9A9A9A;
                margin: 0;
                font-weight: 400;
            }

            .vms-header-right {
                display: flex;
                align-items: center;
                gap: 10px;
            }

            .vms-live-badge {
                display: flex;
                align-items: center;
                gap: 7px;
                background: #F0FBF5;
                border: 1px solid #C3EDD9;
                border-radius: 20px;
                padding: 5px 13px 5px 9px;
                font-size: 12px;
                font-weight: 600;
                color: #1D9E75;
                letter-spacing: 0.3px;
                text-transform: uppercase;
            }

            .vms-live-dot {
                width: 7px;
                height: 7px;
                border-radius: 50%;
                background: #1D9E75;
                animation: vms-pulse 2s infinite;
            }

            /* Overstay alert badge in header — hidden by default */
            .vms-overstay-alert {
                display: none;
                align-items: center;
                gap: 7px;
                background: #FEF0EF;
                border: 1.5px solid #F5C6C3;
                border-radius: 20px;
                padding: 5px 14px 5px 9px;
                font-size: 12px;
                font-weight: 700;
                color: #C0392B;
                letter-spacing: 0.3px;
                text-transform: uppercase;
                animation: vms-alert-appear 0.4s cubic-bezier(0.34,1.56,0.64,1);
            }

            .vms-overstay-alert.visible {
                display: flex;
            }

            .vms-overstay-alert-dot {
                width: 7px;
                height: 7px;
                border-radius: 50%;
                background: #C0392B;
                animation: vms-pulse-red 1.2s infinite;
                flex-shrink: 0;
            }

            @keyframes vms-pulse-red {
                0%, 100% { opacity: 1; transform: scale(1); box-shadow: 0 0 0 0 rgba(192,57,43,0.4); }
                50% { opacity: 0.7; transform: scale(0.85); box-shadow: 0 0 0 4px rgba(192,57,43,0); }
            }

            @keyframes vms-alert-appear {
                0% { transform: scale(0.8); opacity: 0; }
                100% { transform: scale(1); opacity: 1; }
            }

            @keyframes vms-pulse {
                0%, 100% { opacity: 1; transform: scale(1); }
                50% { opacity: 0.4; transform: scale(0.85); }
            }

            .vms-grid {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 14px;
            }

            .vms-grid.vms-grid-single {
                grid-template-columns: minmax(0, 320px);
                justify-content: center;
            }

            .vms-grid.vms-grid-single .vms-stat-card {
                padding: 36px 40px;
            }

            .vms-grid.vms-grid-single .vms-card-count {
                font-size: 64px;
            }

            .vms-grid.vms-grid-single .vms-card-label {
                font-size: 13px;
                letter-spacing: 1px;
            }

            .vms-grid.vms-grid-single .vms-card-bg-icon {
                font-size: 80px;
            }

            @media (max-width: 900px) {
                .vms-grid { grid-template-columns: repeat(2, 1fr); }
            }

            @media (max-width: 500px) {
                .vms-grid { grid-template-columns: 1fr; }
            }

            .vms-stat-card {
                background: #fff;
                border-radius: 14px;
                padding: 22px 22px 20px;
                position: relative;
                overflow: hidden;
                box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 4px 16px rgba(0,0,0,0.04);
                transition: transform 0.18s ease, box-shadow 0.18s ease, opacity 0.2s ease;
                cursor: pointer;
                border: 1px solid rgba(0,0,0,0.05);
            }

            .vms-stat-card:hover {
                transform: translateY(-3px);
                box-shadow: 0 4px 12px rgba(0,0,0,0.08), 0 12px 32px rgba(0,0,0,0.07);
            }

            /* Overstay card — pulsing red border when count > 0 */
            .vms-stat-card.overstay-active {
                border: 1.5px solid #F5C6C3;
                box-shadow: 0 0 0 0 rgba(192,57,43,0.15),
                            0 4px 16px rgba(192,57,43,0.1);
                animation: vms-overstay-glow 2.5s ease-in-out infinite,
                           vms-count-pop 0.4s cubic-bezier(0.34,1.56,0.64,1);
            }

            @keyframes vms-overstay-glow {
                0%, 100% { box-shadow: 0 0 0 0 rgba(192,57,43,0.15), 0 4px 16px rgba(192,57,43,0.08); }
                50%       { box-shadow: 0 0 0 5px rgba(192,57,43,0.08), 0 4px 20px rgba(192,57,43,0.14); }
            }

            .vms-overstay-badge {
                position: absolute;
                top: 13px;
                right: 13px;
                background: #C0392B;
                color: #fff;
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 0.5px;
                text-transform: uppercase;
                border-radius: 20px;
                padding: 3px 8px;
                line-height: 1.4;
                animation: vms-badge-pop 0.4s 0.2s both cubic-bezier(0.34,1.56,0.64,1);
            }

            @keyframes vms-badge-pop {
                0% { transform: scale(0); opacity: 0; }
                100% { transform: scale(1); opacity: 1; }
            }

            .vms-card-accent {
                position: absolute;
                top: 0; left: 0; right: 0;
                height: 3px;
                border-radius: 14px 14px 0 0;
            }

            .vms-card-bg-icon {
                position: absolute;
                bottom: -8px;
                right: 12px;
                font-size: 52px;
                opacity: 0.07;
                line-height: 1;
                pointer-events: none;
            }

            .vms-card-icon {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                width: 32px;
                height: 32px;
                border-radius: 8px;
                font-size: 14px;
                margin-bottom: 14px;
            }

            .vms-card-count {
                font-family: 'DM Mono', monospace;
                font-size: 38px;
                font-weight: 500;
                line-height: 1;
                margin-bottom: 8px;
                letter-spacing: -1px;
                transition: color 0.2s;
            }

            .vms-card-label {
                font-size: 11px;
                font-weight: 600;
                letter-spacing: 0.8px;
                text-transform: uppercase;
            }

            .vms-last-updated {
                margin-top: 20px;
                text-align: right;
                font-size: 11.5px;
                color: #BBBBBB;
                font-family: 'DM Mono', monospace;
                letter-spacing: 0.2px;
            }

            @keyframes vms-count-pop {
                0% { transform: scale(0.85); opacity: 0.4; }
                100% { transform: scale(1); opacity: 1; }
            }
        `;
        document.head.appendChild(style);
    }

    page.add_field({
        label: __("Status"),
        fieldname: "status_filter",
        fieldtype: "Select",
        options: [""].concat(all_statuses),
        change() { refresh(); }
    });

    page.add_field({
        label: __("Host"),
        fieldname: "host_filter",
        fieldtype: "Link",
        options: "Employee",
        change() { refresh(); }
    });

    page.add_field({
        label: __("Date"),
        fieldname: "date_filter",
        fieldtype: "Date",
        default: frappe.datetime.get_today(),
        change() { refresh(); }
    });

    function get_status_filter() {
        const fd = page.fields_dict.status_filter;
        if (!fd) return "";
        const $sel = fd.$wrapper && fd.$wrapper.find("select");
        if ($sel && $sel.length) return ($sel.val() || "").trim();
        return (fd.get_value() || "").trim();
    }

    const $main = $(wrapper).find(".layout-main-section");

    const $wrap = $(`
        <div class="vms-dashboard-wrap">
            <div class="vms-dashboard-header">
                <div class="vms-header-left">
                    <h2>Visitor Dashboard</h2>
                    <p>Real-time visitor status overview</p>
                </div>
                <div class="vms-header-right">
                    <div class="vms-overstay-alert" id="vms-overstay-alert">
                        <span class="vms-overstay-alert-dot"></span>
                        <span class="vms-overstay-alert-text">0 Overstay</span>
                    </div>
                    <div class="vms-live-badge">
                        <span class="vms-live-dot"></span>
                        Live
                    </div>
                </div>
            </div>
            <div class="vms-grid"></div>
            <div class="vms-last-updated"></div>
        </div>
    `).appendTo($main);

    const $grid = $wrap.find(".vms-grid");
    const $updated = $wrap.find(".vms-last-updated");
    const $overstayAlert = $wrap.find("#vms-overstay-alert");

    function renderCards(counts_map, status_filter) {

        $grid.html("");

        const statuses_to_show = status_filter ? [status_filter] : all_statuses;
        $grid.toggleClass("vms-grid-single", statuses_to_show.length === 1);

        // Update header overstay alert badge
        const overstay_count = counts_map["Overstay"] || 0;
        if (overstay_count > 0) {
            $overstayAlert.find(".vms-overstay-alert-text").text(`${overstay_count} Overstay`);
            $overstayAlert.addClass("visible");
        } else {
            $overstayAlert.removeClass("visible");
        }

        statuses_to_show.forEach((status, i) => {
            const cfg = status_config[status];
            if (!cfg) return;

            const count = counts_map[status] !== undefined ? counts_map[status] : 0;
            const isNonzero = count > 0;
            const isOverstay = status === "Overstay";
            const isOverstayActive = isOverstay && isNonzero;

            const countColor = isNonzero ? cfg.color : cfg.color + "55";
            const cardOpacity = isNonzero ? "1" : "0.55";

            // Overstay badge pill shown inside card when count > 0
            const overstayBadgeHtml = isOverstayActive
                ? `<div class="vms-overstay-badge">⚠ Alert</div>`
                : "";

            const $card = $(`
                <div class="vms-stat-card${isNonzero ? " nonzero" : ""}${isOverstayActive ? " overstay-active" : ""}"
                     style="opacity:${cardOpacity}; ${!isOverstayActive ? `animation: vms-count-pop 0.4s ${i * 60}ms both cubic-bezier(0.34,1.56,0.64,1);` : ''}">
                    <div class="vms-card-accent" style="background:${cfg.color};"></div>
                    ${overstayBadgeHtml}
                    <div class="vms-card-icon" style="background:${cfg.bg}; color:${cfg.color};">${cfg.icon}</div>
                    <div class="vms-card-count" style="color:${countColor};">${count}</div>
                    <div class="vms-card-label" style="color:${cfg.color}; opacity:${isNonzero ? '0.75' : '0.6'};">${cfg.label}</div>
                    <div class="vms-card-bg-icon" style="color:${cfg.color};">${cfg.icon}</div>
                </div>
            `);

            // Click → open Visitor list filtered by this status
            $card.css("cursor", "pointer").on("click", function() { 
                frappe.set_route("List", "Visitor", { status: status });
            });


            $card.css("cursor", "pointer").on("click", function() {
            // Get the date from your dashboard filter or default to today
            let selected_date = page.fields_dict.date_filter.get_value() || frappe.datetime.now_date();

                frappe.set_route("List", "Visitor", { 
                status: status,
                expected_arrival: ["between", [selected_date + " 00:00:00", selected_date + " 23:59:59"]]
                });
            });

            $grid.append($card);
        });

        const now = new Date();
        const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
        $updated.text(`Last updated: ${timeStr}`);
    }

    renderCards({}, "");

    function refresh() {
        const status_filter = get_status_filter();

        const filters = {
            status: status_filter,
            host: page.fields_dict.host_filter.get_value() || "",
            date: page.fields_dict.date_filter.get_value() || ""
        };

        frappe.call({
            method: "visitor_management.visitor_management_system.api.get_dashboard_data",
            args: { filters: filters },
            callback(r) {
                if (!r.message || !r.message.counts) return;

                const counts_map = {};
                r.message.counts.forEach(item => {
                    counts_map[item.status] = item.count;
                });

                renderCards(counts_map, status_filter);
            }
        });
    }

    refresh();
    setInterval(refresh, 5000);
    frappe.realtime.on("vms_dashboard_refresh", () => refresh());
};