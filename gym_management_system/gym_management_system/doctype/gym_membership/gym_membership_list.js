frappe.listview_settings["Gym Membership"] = {
    get_indicator: function (doc) {
        add_fields: ["status"];
        hide_name_column: true;
        const status_colors = {
            "Pending": "grey",
            "Active": "green",
            "On Hold": "blue",
            "Expired": "red",
            "Cancelled": "orange", 
        };
        return [__(doc.status), status_colors[doc.status], "status,=," + doc.status];
    },
};