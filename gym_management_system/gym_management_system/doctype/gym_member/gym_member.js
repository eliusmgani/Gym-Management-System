// Copyright (c) 2023, Elius Mgani and contributors
// For license information, please see license.txt

frappe.ui.form.on('Gym Member', {
	refresh: (frm) => {
		if (!frm.doc.assigned_locker) {
			frm.add_custom_button(__("Request Locker"), () => { 
				frappe.new_doc("Gym Locker Booking", {
					"gym_member": frm.doc.name
				});
			}).removeClass("btn-default").addClass("btn-info font-weight-bold")
		}
	},
	onload: (frm) => {
		if (!frm.is_new()) {
			frm.trigger("get_age");
		}
	 },
	get_age: (frm) => {
		let ageMS = Date.parse(Date()) - Date.parse(frm.doc.dob);
		let age = new Date();
		age.setTime(ageMS);
		let years = age.getFullYear() - 1970;
		let age_str = years + ' Year(s) ' + age.getMonth() + ' Month(s) ' + age.getDate() + ' Day(s)';
		if (frm.doc.age != age_str) {
			frappe.db.set_value(frm.doc.doctype, frm.doc.name, "age", age_str);
			frm.refresh_field("age");
		}
	},
});
