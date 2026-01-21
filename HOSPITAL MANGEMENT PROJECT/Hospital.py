"""
Pretty UI wrapper for your Hospital Management System
UI changes only. Logic / DB code preserved.
Requires: customtkinter, mysql-connector-python
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

# ---------------- Appearance ----------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class Hospital:
    def __init__(self, root):
        self.root = root
        self.root.title("HOSPITAL MANAGEMENT SYSTEM")
        self.root.geometry('1540x800+0+0')
        self.root.minsize(1100, 700)

        # Variables (unchanged)
        self.name_of_tablets = tk.StringVar()
        self.name_of_disease = tk.StringVar()
        self.ref = tk.StringVar()
        self.dose = tk.StringVar()
        self.no_of_tablets = tk.StringVar()
        self.lot = tk.StringVar()
        self.issued_date = tk.StringVar()
        self.expiry_date = tk.StringVar()
        self.daily_dose = tk.StringVar()
        self.side_effects = tk.StringVar()
        self.further_info = tk.StringVar()
        self.storage_advice = tk.StringVar()
        self.medication_info = tk.StringVar()
        self.patient_id = tk.StringVar()
        self.patient_name = tk.StringVar()
        self.dob = tk.StringVar()
        self.gender = tk.StringVar()
        self.patient_address = tk.StringVar()

        # Topbar
        topbar = ctk.CTkFrame(self.root, height=90, corner_radius=0)
        topbar.pack(fill="x", side="top")
        title = ctk.CTkLabel(topbar, text="Hospital Management System", font=ctk.CTkFont(size=28, weight="bold"))
        title.place(x=22, y=18)
        subtitle = ctk.CTkLabel(topbar, text="Manage patients & prescriptions — clean UI, same logic",
                                font=ctk.CTkFont(size=12), text_color="#AAB2C1")
        subtitle.place(x=24, y=56)
        self.mode_switch = ctk.CTkSwitch(topbar, text="Light mode", command=self.toggle_appearance)
        self.mode_switch.place(relx=0.86, rely=0.33)

        # Main layout
        main = ctk.CTkFrame(self.root, corner_radius=12)
        main.pack(fill="both", expand=True, padx=16, pady=12)

        top_content = ctk.CTkFrame(main, fg_color="transparent")
        top_content.pack(fill="both", expand=True)
        bottom_actions = ctk.CTkFrame(main, fg_color="transparent")
        bottom_actions.pack(fill="x", pady=(8,0))

        left = ctk.CTkFrame(top_content, width=480, corner_radius=12)
        left.pack(side="left", fill="y", padx=(12,8), pady=12)
        left.pack_propagate(False)

        right = ctk.CTkFrame(top_content, corner_radius=12)
        right.pack(side="right", fill="both", expand=True, padx=(8,12), pady=12)

        # Left form
        ctk.CTkLabel(left, text="Patient Information", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(12,6))
        form_area = ctk.CTkScrollableFrame(left, width=440, height=560, corner_radius=10)
        form_area.pack(padx=12, pady=(6,12), fill="both", expand=True)

        def add_label(entry_frame, text):
            ctk.CTkLabel(entry_frame, text=text, anchor="w", font=ctk.CTkFont(size=11, weight="bold")).pack(fill="x", padx=6, pady=(8,2))

        # --- IMPORTANT CHANGE: keep CTk look but use ttk.Combobox with matching font/height ---
        add_label(form_area, "NAME OF TABLETS")
        tablets = ["Acetaminophen","Azithromycin","Botox","Brilinta","Bunavail","Cymbalta","Doxycycline","Dupixent",
                   "Entresto","Entyvio","Farxiga","Humira","Ibuprofen","Imbruvica","Januvia","Jardiance","Keytruda",
                   "Lexapro","Lisinopril","Lyrica","Melatonin","Meloxicam","Metformin","Mounjaro","Naltrexone",
                   "Naproxen","Narcan","Omeprazole","Opdivo","Ozempic","Pantoprazole","Prednisone","Probuphine",
                   "Qulipta","Quviviq","Rybelsus","Sublocade","Tepezza","Wegovy","Wellbutrin","Xanax","Yervoy","Zubsolv"]

        # Style ttk combobox to visually match CTkEntry font/size
        style = ttk.Style()
        # prefer 'clam' to allow customizations
        try:
            style.theme_use("clam")
        except:
            pass
        # Match the font size/weight so combobox looks similar to surrounding CTk widgets
        combofont = ("Segoe UI", 20)
        style.configure("Custom.TCombobox", font=combofont, fieldbackground="#2b2b2b", background="#2b2b2b", foreground="#E6EEF3")
        style.map("Custom.TCombobox",
                  fieldbackground=[('readonly', '#2b2b2b')],
                  background=[('readonly', '#2b2b2b')])

        # Create ttk Combobox (readonly) and limit dropdown height to 8 items (compact with scrollbar)
        tablet_cb = ttk.Combobox(form_area, textvariable=self.name_of_tablets, values=tablets, state="readonly", style="Custom.TCombobox", width=45)
        try:
            tablet_cb.configure(height=8)   # limit dropdown to 8 visible items (most ttk implementations honor this)
        except Exception:
            pass
        tablet_cb.current(0)
        # pack with fill so width aligns with CTkEntry
        tablet_cb.pack(padx=6, pady=(0,6), anchor="w", fill="x")

        # Disease combobox: same approach
        add_label(form_area, "NAME OF DISEASE")
        diseases = ["Covid-19","Fever","Angina","Atopic eczema","Bowel cancer","Chest/Rib injury","Eye cancer",
                    "Inflammatory bowel disease (IBD)","Liver cancer","Ovarian cancer","PTSD","Stomach cancer","Hepatitis","Flu",
                    "Sexually transmitted infection","Gastroenteritis","HIV/AIDS","Malaria","Respiratory disease","Chickenpox","Common cold",
                    "Measles","Meningitis","Autoimmune diseases","Lung cancer","Chikungunya","Giardiasis","Viral hemorrhagic fever",
                    "Heart Disease","Kidney disease","Lupus","Parkinson's disease","Polio","Rabies","Tuberculosis"]
        disease_cb = ttk.Combobox(form_area, textvariable=self.name_of_disease, values=diseases, state="readonly", style="Custom.TCombobox", width=45)
        try:
            disease_cb.configure(height=8)
        except Exception:
            pass
        disease_cb.current(0)
        disease_cb.pack(padx=6, pady=(0,6), anchor="w", fill="x")

        # helper for other entries (CTkEntry to keep look same)
        def add_entry(var, placeholder=""):
            ent = ctk.CTkEntry(form_area, textvariable=var, placeholder_text=placeholder, width=400)
            ent.pack(padx=6, pady=(0,6))
            return ent

        add_label(form_area, "REFERENCE NO")
        txtref = add_entry(self.ref, "e.g. REF001")
        add_label(form_area, "DOSE")
        txtDose = add_entry(self.dose)
        add_label(form_area, "NUMBER OF TABLETS")
        txtNoOfTablets = add_entry(self.no_of_tablets)
        add_label(form_area, "LOT")
        txtLot = add_entry(self.lot)

        # dates horizontally (kept same)
        dates_container = ctk.CTkFrame(form_area, fg_color="transparent")
        dates_container.pack(fill="x", padx=6, pady=(6,6))
        dates_container.grid_columnconfigure((0,1), weight=1)
        left_dates = ctk.CTkFrame(dates_container, fg_color="transparent")
        left_dates.grid(row=0, column=0, sticky="we", padx=(0,6))
        right_dates = ctk.CTkFrame(dates_container, fg_color="transparent")
        right_dates.grid(row=0, column=1, sticky="we", padx=(6,0))

        ctk.CTkLabel(left_dates, text="ISSUED DATE", anchor="w", font=ctk.CTkFont(size=10, weight="bold")).pack(fill="x")
        issued_ent = ctk.CTkEntry(left_dates, textvariable=self.issued_date, placeholder_text=datetime.today().strftime("%Y-%m-%d"))
        issued_ent.pack(fill="x", pady=(6,0))

        ctk.CTkLabel(right_dates, text="EXPIRY DATE", anchor="w", font=ctk.CTkFont(size=10, weight="bold")).pack(fill="x")
        expiry_ent = ctk.CTkEntry(right_dates, textvariable=self.expiry_date, placeholder_text="YYYY-MM-DD")
        expiry_ent.pack(fill="x", pady=(6,0))

        add_label(form_area, "DAILY DOSE")
        txtDailyDose = add_entry(self.daily_dose)
        add_label(form_area, "SIDE EFFECTS")
        txtSideEffects = add_entry(self.side_effects)
        add_label(form_area, "FURTHER INFORMATION")
        txtFurtherInfo = add_entry(self.further_info)
        add_label(form_area, "STORAGE ADVICE")
        txtStorageAdvice = add_entry(self.storage_advice)
        add_label(form_area, "MEDICATION INFORMATION")
        txtMedicationInfo = add_entry(self.medication_info)

        ctk.CTkLabel(form_area, text="--- Patient Details ---", text_color="#AAB2C1").pack(pady=(8,6))
        add_label(form_area, "PATIENT ID")
        txtPatientID = add_entry(self.patient_id)
        add_label(form_area, "PATIENT NAME")
        txtPatientName = add_entry(self.patient_name)
        add_label(form_area, "DOB")
        txtDOB = add_entry(self.dob, "YYYY-MM-DD")
        add_label(form_area, "GENDER")
        txtGender = add_entry(self.gender, "M / F / Other")
        add_label(form_area, "PATIENT ADDRESS")
        txtAddress = add_entry(self.patient_address, "Street, City, PIN")

        # action buttons inside bottom_actions
        btn_pres = ctk.CTkButton(bottom_actions, text="PRESCRIPTION", command=self.iprescription, corner_radius=8)
        btn_pres.pack(side="left", padx=8, pady=10)
        btn_add = ctk.CTkButton(bottom_actions, text="PRESCRIPTION DATA", command=self.iperscriptionData, fg_color="#1976D2", hover_color="#165FAD")
        btn_add.pack(side="left", padx=8, pady=10)
        btn_update = ctk.CTkButton(bottom_actions, text="UPDATE", command=self.ipdate_data)
        btn_update.pack(side="left", padx=8, pady=10)

        # Right: tree + preview (kept same look & placements)
        top_right = ctk.CTkFrame(right, fg_color="transparent")
        top_right.pack(fill="x", padx=12, pady=(12,6))
        self.search_var = tk.StringVar()
        search = ctk.CTkEntry(top_right, textvariable=self.search_var, placeholder_text="Search (tablet / patient / ref) — optional visual", width=420)
        search.pack(side="left", padx=(0,12))
        search.bind("<KeyRelease>", self._filter_treeview)
        refresh = ctk.CTkButton(top_right, text="Refresh", width=100, command=self.fetch_data)
        refresh.pack(side="left")

        tree_card = ctk.CTkFrame(right, corner_radius=10)
        tree_card.pack(fill="both", expand=True, padx=12, pady=(6,12))

        # Treeview styling (unchanged)
        tv_style = ttk.Style()
        try:
            tv_style.theme_use("clam")
        except:
            pass
        tv_style.configure("Pretty.Treeview", rowheight=28, font=("Segoe UI", 10), background="#F8FAFC", fieldbackground="#F8FAFC", foreground="#0F1720")
        tv_style.configure("Pretty.Treeview.Heading", font=("Segoe UI", 10, "bold"))

        columns = ("tabletname", "diseasename", "ref", "dose",
                   "nooftablets", "lot", "issueddate", "expirydate",
                   "dailydose", "sideeffects", "furtherinfo", "storageadvice",
                   "medicationinfo", "patientid", "patientname", "dob", "gender",
                   "patientaddress")

        self.hospital_table = ttk.Treeview(tree_card, columns=columns, show="headings", style="Pretty.Treeview")
        for col in columns:
            header = col.replace("name", " Name").replace("tablet", "Tablet").replace("patient", "Patient").title()
            self.hospital_table.heading(col, text=header)
            w = 110
            if col in ("tabletname", "diseasename", "patientname"): w = 160
            if col == "patientaddress": w = 220
            self.hospital_table.column(col, width=w, anchor="center")
        self.hospital_table.pack(side="left", fill="both", expand=True, padx=(8,0), pady=8)

        vsb = ttk.Scrollbar(tree_card, orient="vertical", command=self.hospital_table.yview)
        vsb.pack(side="right", fill="y", padx=(0,8), pady=8)
        self.hospital_table.configure(yscrollcommand=vsb.set)
        self.hospital_table.bind("<ButtonRelease-1>", self.get_cursor)

        preview_card = ctk.CTkFrame(right, corner_radius=8)
        preview_card.pack(fill="x", padx=12, pady=(4,12))
        ctk.CTkLabel(preview_card, text="Prescription Preview", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=10, pady=(8,4))
        self.txtPrescription = tk.Text(preview_card, font=("Segoe UI", 11), height=8, bg="#0B1220", fg="#E6EEF3", bd=0)
        self.txtPrescription.pack(fill="both", expand=True, padx=10, pady=(4,12))

        # right-aligned exit/clear/delete buttons
        spacer = ctk.CTkLabel(bottom_actions, text="", fg_color="transparent")
        spacer.pack(side="left", expand=True)
        btn_exit = ctk.CTkButton(bottom_actions, text="EXIT", command=self.iexit, width=120)
        btn_exit.pack(side="right", padx=12, pady=10)
        btn_clear = ctk.CTkButton(bottom_actions, text="CLEAR", command=self.clear_data, width=120)
        btn_clear.pack(side="right", padx=12, pady=10)
        btn_delete = ctk.CTkButton(bottom_actions, text="DELETE", fg_color="#D32F2F", hover_color="#C62828", command=self.idelete_data, width=120)
        btn_delete.pack(side="right", padx=12, pady=10)

        # initial load
        self.fetch_data()

    # UI helpers
    def toggle_appearance(self):
        if self.mode_switch.get():
            ctk.set_appearance_mode("light")
            self.mode_switch.configure(text="Dark mode")
        else:
            ctk.set_appearance_mode("dark")
            self.mode_switch.configure(text="Light mode")

    def _filter_treeview(self, event=None):
        q = self.search_var.get().strip().lower()
        for iid in self.hospital_table.get_children():
            vals = " ".join([str(x).lower() for x in self.hospital_table.item(iid)["values"]])
            if q in vals:
                self.hospital_table.reattach(iid, "", "end")
            else:
                self.hospital_table.detach(iid)

    # Database / CRUD (unchanged)
    def iperscriptionData(self):
        if self.name_of_tablets.get().strip() == "" or self.ref.get().strip() == "":
            messagebox.showerror("Error", "Tablet name and Reference No. are required!")
            return
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="1234", database="hospital")
            my_cursor = conn.cursor()
            insert_query = """
                INSERT INTO hospital_data (
                    NAME_OF_TABLETS, NAME_OF_DISEASE, REFERENCE_NO, DOSE, NUMBER_OF_TABLETS,
                    LOT, ISSUED_DATE, EXPIR_DATE, DAILY_DOSE, SIDE_EFFECTS,
                    FURTHER_INFORMATION, STORAGE_ADVICE, MEDICATION_INFORMATION,
                    PATIENT_ID, PATIENT_NAME, DOB, GENDER, PATIENT_ADDRESS
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            my_cursor.execute(insert_query, (
                self.name_of_tablets.get(),
                self.name_of_disease.get(),
                self.ref.get().strip(),
                self.dose.get(),
                self.no_of_tablets.get(),
                self.lot.get(),
                self.issued_date.get(),
                self.expiry_date.get(),
                self.daily_dose.get(),
                self.side_effects.get(),
                self.further_info.get(),
                self.storage_advice.get(),
                self.medication_info.get(),
                self.patient_id.get(),
                self.patient_name.get(),
                self.dob.get(),
                self.gender.get(),
                self.patient_address.get()
            ))
            conn.commit()
            my_cursor.close()
            conn.close()
            self.fetch_data()
            messagebox.showinfo("Success", "Prescription data inserted successfully!")
            self.clear_data()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error inserting data:\n{err}")

    def fetch_data(self):
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="1234", database="hospital")
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT * FROM hospital_data")
            rows = my_cursor.fetchall()
            if rows:
                self.hospital_table.delete(*self.hospital_table.get_children())
                for row in rows:
                    self.hospital_table.insert('', tk.END, values=row)
            my_cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching data:\n{err}")

    def get_cursor(self, event=""):
        cursor_row = self.hospital_table.focus()
        if not cursor_row:
            return
        content = self.hospital_table.item(cursor_row)
        row = content.get('values')
        if not row:
            return
        try:
            self.name_of_tablets.set(row[0])
            self.name_of_disease.set(row[1])
            self.ref.set(row[2])
            self.dose.set(row[3])
            self.no_of_tablets.set(row[4])
            self.lot.set(row[5])
            self.issued_date.set(row[6])
            self.expiry_date.set(row[7])
            self.daily_dose.set(row[8])
            self.side_effects.set(row[9])
            self.further_info.set(row[10])
            self.storage_advice.set(row[11])
            self.medication_info.set(row[12])
            self.patient_id.set(row[13])
            self.patient_name.set(row[14])
            self.dob.set(row[15])
            self.gender.set(row[16])
            self.patient_address.set(row[17])
        except IndexError:
            messagebox.showwarning("Warning", "Selected row doesn't match expected format.")

    def ipdate_data(self):
        if self.ref.get().strip() == "":
            messagebox.showerror("Error", "Please select a record to update!")
            return
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="1234", database="hospital")
            my_cursor = conn.cursor()
            ref_no = self.ref.get().strip()
            update_query = """
                UPDATE hospital_data 
                SET 
                    NAME_OF_TABLETS=%s, 
                    NAME_OF_DISEASE=%s,
                    DOSE=%s,
                    NUMBER_OF_TABLETS=%s,
                    LOT=%s,
                    ISSUED_DATE=%s,
                    EXPIR_DATE=%s,
                    DAILY_DOSE=%s,
                    SIDE_EFFECTS=%s,
                    FURTHER_INFORMATION=%s,
                    STORAGE_ADVICE=%s,
                    MEDICATION_INFORMATION=%s,
                    PATIENT_ID=%s,
                    PATIENT_NAME=%s,
                    DOB=%s,
                    GENDER=%s,
                    PATIENT_ADDRESS=%s
                WHERE REFERENCE_NO=%s
            """
            my_cursor.execute(update_query, (
                self.name_of_tablets.get(),
                self.name_of_disease.get(),
                self.dose.get(),
                self.no_of_tablets.get(),
                self.lot.get(),
                self.issued_date.get(),
                self.expiry_date.get(),
                self.daily_dose.get(),
                self.side_effects.get(),
                self.further_info.get(),
                self.storage_advice.get(),
                self.medication_info.get(),
                self.patient_id.get(),
                self.patient_name.get(),
                self.dob.get(),
                self.gender.get(),
                self.patient_address.get(),
                ref_no
            ))
            affected = my_cursor.rowcount
            conn.commit()
            my_cursor.close()
            conn.close()
            self.fetch_data()
            if affected > 0:
                messagebox.showinfo("Success", "Record updated successfully!")
            else:
                messagebox.showwarning("Warning", "No record found for this Reference Number!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error updating data:\n{err}")

    def clear_data(self):
        self.name_of_tablets.set("")
        self.name_of_disease.set("")
        self.ref.set("")
        self.dose.set("")
        self.no_of_tablets.set("")
        self.lot.set("")
        self.issued_date.set("")
        self.expiry_date.set("")
        self.daily_dose.set("")
        self.side_effects.set("")
        self.further_info.set("")
        self.storage_advice.set("")
        self.medication_info.set("")
        self.patient_id.set("")
        self.patient_name.set("")
        self.dob.set("")
        self.gender.set("")
        self.patient_address.set("")
        self.txtPrescription.delete(1.0, tk.END)

    def iprescription(self):
        self.txtPrescription.delete(1.0, tk.END)
        self.txtPrescription.insert(tk.END, "Name of Tablets:\t\t" + self.name_of_tablets.get() + "\n")
        self.txtPrescription.insert(tk.END, "Name of Disease:\t\t" + self.name_of_disease.get() + "\n")
        self.txtPrescription.insert(tk.END, "Reference No:\t\t" + self.ref.get() + "\n")
        self.txtPrescription.insert(tk.END, "Dose:\t\t" + self.dose.get() + "\n")
        self.txtPrescription.insert(tk.END, "Number of Tablets:\t\t" + self.no_of_tablets.get() + "\n")
        self.txtPrescription.insert(tk.END, "Lot:\t\t" + self.lot.get() + "\n")
        self.txtPrescription.insert(tk.END, "Issued Date:\t\t" + self.issued_date.get() + "\n")
        self.txtPrescription.insert(tk.END, "Expiry Date:\t\t" + self.expiry_date.get() + "\n")
        self.txtPrescription.insert(tk.END, "Daily Dose:\t\t" + self.daily_dose.get() + "\n")
        self.txtPrescription.insert(tk.END, "Side Effects:\t\t" + self.side_effects.get() + "\n")
        self.txtPrescription.insert(tk.END, "Further Information:\t\t" + self.further_info.get() + "\n")
        self.txtPrescription.insert(tk.END, "Storage Advice:\t\t" + self.storage_advice.get() + "\n")
        self.txtPrescription.insert(tk.END, "Medication Information:\t\t" + self.medication_info.get() + "\n")
        self.txtPrescription.insert(tk.END, "Patient ID:\t\t" + self.patient_id.get() + "\n")
        self.txtPrescription.insert(tk.END, "Patient Name:\t\t" + self.patient_name.get() + "\n")
        self.txtPrescription.insert(tk.END, "DOB:\t\t" + self.dob.get() + "\n")
        self.txtPrescription.insert(tk.END, "Gender:\t\t" + self.gender.get() + "\n")
        self.txtPrescription.insert(tk.END, "Patient Address:\t\t" + self.patient_address.get() + "\n")

    def idelete_data(self):
        if self.ref.get().strip() == "":
            messagebox.showerror("Error", "Please select a record to delete!")
            return
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="1234", database="hospital")
            my_cursor = conn.cursor()
            ref_no = self.ref.get().strip()
            my_cursor.execute("DELETE FROM hospital_data WHERE REFERENCE_NO=%s", (ref_no,))
            affected = my_cursor.rowcount
            conn.commit()
            my_cursor.close()
            conn.close()
            self.fetch_data()
            if affected > 0:
                messagebox.showinfo("Success", "Record deleted successfully!")
                self.clear_data()
            else:
                messagebox.showwarning("Warning", "No record found for this Reference Number!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error deleting data:\n{err}")

    def iexit(self):
        confirm = messagebox.askyesno("Hospital Management System", "Do you want to exit?")
        if confirm:
            self.root.destroy()

# Run
if __name__ == "__main__":
    app = ctk.CTk()
    Hospital(app)
    app.mainloop()
