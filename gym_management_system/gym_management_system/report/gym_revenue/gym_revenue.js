// Copyright (c) 2023, Elius Mgani and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Gym Revenue"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"reqd": 1,
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd": 1,
		},
		{
			"fieldname": "gym_trainer",
			"label": __("Gym Trainer"),
			"fieldtype": "Link",
			"options": "Gym Trainer",
		},

	]
};
