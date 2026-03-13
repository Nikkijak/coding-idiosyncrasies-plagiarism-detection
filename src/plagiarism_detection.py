import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

from winnowing import compare_fingerprints, process_text


CODE_FILE_TYPES = [
    ("Python files", "*.py"),
    ("Java files", "*.java"),
    ("C++ files", "*.cpp"),
    ("C files", "*.c"),
    ("All files", "*.*"),
]

class PlagiarismDetectionTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Plagiarism Detection Tool")
        self.root.geometry("800x600")
        self.root.configure(bg="#d0e6f6")

        self.student_uploaded_file = None
        self.teacher_uploaded_files = []
        self.users = ["student1", "student2", "teacher1", "admin"]

        frame_font = ("Arial", 14, "bold")
        button_font = ("Arial", 12)

        student_frame = tk.LabelFrame(
            root,
            text="Student Actions",
            padx=20,
            pady=20,
            bg="#e1f5fe",
            font=frame_font,
            bd=3,
            relief=tk.GROOVE,
        )
        student_frame.pack(padx=20, pady=20, fill="both", expand="yes")

        teacher_frame = tk.LabelFrame(
            root,
            text="Teacher Actions",
            padx=20,
            pady=20,
            bg="#e1f5fe",
            font=frame_font,
            bd=3,
            relief=tk.GROOVE,
        )
        teacher_frame.pack(padx=20, pady=20, fill="both", expand="yes")

        admin_frame = tk.LabelFrame(
            root,
            text="Admin Actions",
            padx=20,
            pady=20,
            bg="#e1f5fe",
            font=frame_font,
            bd=3,
            relief=tk.GROOVE,
        )
        admin_frame.pack(padx=20, pady=20, fill="both", expand="yes")

        tk.Button(
            student_frame,
            text="Submit Code for Analysis",
            font=button_font,
            bg="#ffffff",
            fg="#333333",
            activebackground="#b0e0e6",
            activeforeground="#000000",
            relief=tk.RAISED,
            bd=2,
            cursor="hand2",
            padx=10,
            pady=5,
            width=25,
            command=self.submit_code_student,
        ).pack(pady=10)

        tk.Button(
            student_frame,
            text="Receive Plagiarism Report",
            font=button_font,
            bg="#ffffff",
            fg="#333333",
            activebackground="#b0e0e6",
            activeforeground="#000000",
            relief=tk.RAISED,
            bd=2,
            cursor="hand2",
            padx=10,
            pady=5,
            width=25,
            command=self.receive_report_student,
        ).pack(pady=10)

        tk.Button(
            teacher_frame,
            text="Upload Student Files",
            font=button_font,
            bg="#ffffff",
            fg="#333333",
            activebackground="#b0e0e6",
            activeforeground="#000000",
            relief=tk.RAISED,
            bd=2,
            cursor="hand2",
            padx=10,
            pady=5,
            width=25,
            command=self.upload_files_teacher,
        ).pack(pady=10)

        tk.Button(
            teacher_frame,
            text="Generate Detailed Report",
            font=button_font,
            bg="#ffffff",
            fg="#333333",
            activebackground="#b0e0e6",
            activeforeground="#000000",
            relief=tk.RAISED,
            bd=2,
            cursor="hand2",
            padx=10,
            pady=5,
            width=25,
            command=self.generate_report_teacher,
        ).pack(pady=10)

        tk.Button(
            admin_frame,
            text="View Users",
            font=button_font,
            bg="#ffffff",
            fg="#333333",
            activebackground="#b0e0e6",
            activeforeground="#000000",
            relief=tk.RAISED,
            bd=2,
            cursor="hand2",
            padx=10,
            pady=5,
            width=25,
            command=self.view_users,
        ).pack(pady=10)

        tk.Button(
            admin_frame,
            text="Add User",
            font=button_font,
            bg="#ffffff",
            fg="#333333",
            activebackground="#b0e0e6",
            activeforeground="#000000",
            relief=tk.RAISED,
            bd=2,
            cursor="hand2",
            padx=10,
            pady=5,
            width=25,
            command=self.add_user,
        ).pack(pady=10)

        tk.Button(
            admin_frame,
            text="Remove User",
            font=button_font,
            bg="#ffffff",
            fg="#333333",
            activebackground="#b0e0e6",
            activeforeground="#000000",
            relief=tk.RAISED,
            bd=2,
            cursor="hand2",
            padx=10,
            pady=5,
            width=25,
            command=self.remove_user,
        ).pack(pady=10)

    def submit_code_student(self):
        filename = filedialog.askopenfilename(
            title="Select Code File",
            filetypes=CODE_FILE_TYPES,
        )
        if filename:
            self.student_uploaded_file = filename
            messagebox.showinfo("Code Submission", f"File submitted:\n{filename}")

    def receive_report_student(self):
        if not self.student_uploaded_file:
            messagebox.showwarning("No File", "No code file has been submitted for analysis.")
            return

        messagebox.showinfo(
            "Plagiarism Report",
            f"File '{self.student_uploaded_file}' has been submitted and will be analyzed.",
        )

    def upload_files_teacher(self):
        filenames = filedialog.askopenfilenames(
            title="Select Student Code Files",
            filetypes=CODE_FILE_TYPES,
        )
        if filenames:
            self.teacher_uploaded_files = list(filenames)
            file_list = "\n".join(os.path.basename(name) for name in filenames)
            messagebox.showinfo("Files Uploaded", f"Student files uploaded:\n{file_list}")

    def generate_report_teacher(self):
        if not self.teacher_uploaded_files:
            messagebox.showwarning("No Files", "No files have been uploaded for comparison.")
            return

        fingerprint_cache = {
            file_path: process_text(file_path)
            for file_path in self.teacher_uploaded_files
        }

        reports = []

        for i in range(len(self.teacher_uploaded_files)):
            for j in range(i + 1, len(self.teacher_uploaded_files)):
                file1 = self.teacher_uploaded_files[i]
                file2 = self.teacher_uploaded_files[j]

                fingerprints1 = fingerprint_cache[file1]
                fingerprints2 = fingerprint_cache[file2]

                similarity_score, matching_fingerprints = compare_fingerprints(
                    fingerprints1,
                    fingerprints2,
                )

                name1 = os.path.basename(file1)
                name2 = os.path.basename(file2)

                reports.append(
                    f"{name1} vs {name2}: {similarity_score:.2f}% similarity\n"
                    f"Matching fingerprints: {matching_fingerprints}\n"
                )

        if reports:
            report_text = "\n".join(reports)
            messagebox.showinfo("Detailed Report", report_text)
        else:
            messagebox.showinfo(
                "Detailed Report",
                "No similarities detected between the uploaded files.",
            )

    def view_users(self):
        user_list = "\n".join(self.users)
        messagebox.showinfo("View Users", f"Current Users:\n{user_list}")

    def add_user(self):
        new_user = simpledialog.askstring("Add User", "Enter new username:")
        if not new_user:
            return

        if new_user in self.users:
            messagebox.showwarning("Add User", f"User '{new_user}' already exists.")
        else:
            self.users.append(new_user)
            messagebox.showinfo("Add User", f"User '{new_user}' added successfully.")

    def remove_user(self):
        remove_user = simpledialog.askstring("Remove User", "Enter username to remove:")
        if not remove_user:
            return

        if remove_user in self.users:
            self.users.remove(remove_user)
            messagebox.showinfo("Remove User", f"User '{remove_user}' removed successfully.")
        else:
            messagebox.showwarning("Remove User", f"User '{remove_user}' does not exist.")


if __name__ == "__main__":
    root = tk.Tk()
    app = PlagiarismDetectionTool(root)
    root.mainloop()