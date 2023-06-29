// Copyright (c) 2023, Elius Mgani and contributors
// For license information, please see license.txt

frappe.ui.form.on('Gym Membership', {
	refresh: (frm) => {
		if (frm.doc.paid == 0 && !frm.doc.__islocal) {
			frm.add_custom_button(__("Make Paymnent"), () => {
				frappe.new_doc("Gym Payment", {
					"payment_for": "Membership"
				}, doc => {
					doc.gym_member = frm.doc.gym_member;
					doc.reference_doctype = frm.doc.doctype;
					doc.reference_name = frm.doc.name;
					doc.payment_date = frappe.datetime.now_date();
					doc.payment_time = frappe.datetime.now_time();
					doc.posting_date = frappe.datetime.now_date();
					doc.posting_time = frappe.datetime.now_time();
					doc.actual_price = frm.doc.membership_cost;
					doc.discount_amount = frm.doc.discount_amount;
					doc.paid_amount = frm.doc.membership_cost - frm.doc.discount_amount;
				});
			}).removeClass("btn-default").addClass("btn-warning font-weight-bold")
		}
	}
});
 