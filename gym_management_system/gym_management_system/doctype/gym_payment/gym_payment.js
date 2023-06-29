// Copyright (c) 2023, Elius Mgani and contributors
// For license information, please see license.txt

frappe.ui.form.on('Gym Payment', {
	// refresh: function(frm) {

	// }
	actual_price: (frm) => {
		if (frm.doc.actual_price) {
			let paid_amount = frm.doc.actual_price - frm.doc.discount_amount;
			frm.set_value("paid_amount", paid_amount)
		}
	},
	discount_amount: (frm) => {
		if (frm.doc.discount_amount) {
			let paid_amount = frm.doc.actual_price - frm.doc.discount_amount;
			frm.set_value("paid_amount", paid_amount)
		}
	}
});