import tkinter as tk
from tkinter import messagebox
from tkinter import *
from tkinter import filedialog, simpledialog, ttk
from tkPDFViewer2 import tkPDFViewer as pdf
from PIL import Image, ImageTk
import mysql.connector
import os

root =tk.Tk()

class LibraryApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Knowledge Treasure Library")
        self.master.geometry("668x774")

        # Connect to MySQL database
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="895952",
            database="library"
        )
        self.cursor = self.db.cursor()
        # Load background image
        image = Image.open("background.jpg")
        image = image.resize((768, 1024), Image.BILINEAR)
        self.background_image = ImageTk.PhotoImage(image)

        # Set background image
        self.background_label = tk.Label(master, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)
        
        #title text
        self.label = tk.Label(master, text="Knowledge Treasure Library",
                              font=("Helvetica", 30, "bold"))
        self.label.pack(pady=20)

        # Buttons
        self.read_books_button = tk.Button(master, text="Read Books",
                                           command=self.open_read_books_window,
                                           bg='black',fg='white', width=24,
                                           font='arial 40',bd=4)
        self.read_books_button.pack(pady=20)

        self.add_book_button = tk.Button(master, text="Add Book Entry",
                                         command=self.add_book_entry,bg='black',
                                         fg='white',width=24,
                                         font='arial 40',bd=4)
        self.add_book_button.pack(pady=20)

        self.show_books_button = tk.Button(master, text="Show Books",
                                           command=self.show_books_window,
                                           bg='black',fg='white', width=24,
                                           font='arial 40',bd=4)
        self.show_books_button.pack(pady=20)

        self.delete_book_button = tk.Button(master, text="Delete Book Entry",
                                            command=self.delete_book_entry,
                                            bg='black',fg='white', width=24,
                                           font='arial 40',bd=4)
        self.delete_book_button.pack(pady=20)

        self.troubleshoot_button = tk.Button(master, text="Database Troubleshoot",
                                             command=self.troubleshoot_database,
                                             bg='orange', fg='white', width=24,
                                             font='arial 40', bd=4)
        self.troubleshoot_button.pack(pady=20)

    def troubleshoot_database(self):
        try:
            # First connect to the MySQL server without specifying the database
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="895952",
                database='library'
            )
            cursor = connection.cursor()

            # Check if the 'library' database exists
            cursor.execute("SHOW DATABASES LIKE 'library'")
            
            result = cursor.fetchone()
            
            if result:
        
                
                cursor.execute("create table Books(bkid int primary key, title varchar(255), author varchar(255), year int);")
                
                messagebox.showinfo("Success", "table 'Books' created successfully.")
            
            
            # Clean up
            cursor.close()
            connection.close()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    def open_read_books_window(self):
        read_window = tk.Toplevel(self.master)
        read_window.title("Read Books")
        read_window.geometry("768x1024")
        
        self.background_label = tk.Label(read_window, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)
        def openfiles():
            filename=filedialog.askopenfilename(initialdir=os.getcwd(),
            title="select book file",
            filetype=(("pdf File", ".pdf"),
                      ("PDF file", ".PDF"),
                      ("ALL file", ".txt")))
            v1=pdf.ShowPdf()
            v2=v1.pdf_view(read_window,pdf_location=open(filename, "r"),width=77, height=100)
            v2.pack(pady=(0,0))
        open_books_button = tk.Button(read_window, text="Browse Books",
                                      command=openfiles,bg='black',fg='white', width=40,
                                      font='Helvetica 30',bd=5).pack(pady=4)
    def add_book_entry(self):
         bkid = simpledialog.askinteger("Add Book Id", "Enter Book Id:")

         if bkid is None:
             return
         title = simpledialog.askstring("Add Book Entry", "Enter Title:")

         if title is None:
             return
         author = simpledialog.askstring("Add Book Entry", "Enter Author:")

         if author is None:
             return
         year = simpledialog.askinteger("Add Book Entry", "Enter Year:")

         if year is None:
             return

         if bkid and title and author and year:
             query = "INSERT INTO books (bkid, title, author, year) VALUES (%s, %s, %s, %s)"
             values = (bkid, title, author, year)

             try:
                 self.cursor.execute(query, values)
                 self.db.commit()
                 messagebox.showinfo("Success", "Book entry added successfully.")
             except Exception as e:
                 messagebox.showerror("Error", f"Error: {e}")
         else:
             messagebox.showwarning("Warning", "Please provide valid input for all fields.")

    def show_books_window(self):
        show_books_window = tk.Toplevel(self.master)
        show_books_window.title("Show Books")
        show_books_window.geometry("600x800")

        query = "SELECT * FROM books"
        try:
            self.cursor.execute(query)
            books = self.cursor.fetchall()

            for book in books:
                book_info = f"Title: {book[1]}\nAuthor: {book[2]}\nYear: {book[3]}\n\n"
                
                # Display book information with left alignment
                tk.Label(show_books_window, text=book_info, font=("Helvetica", 12), anchor="w", justify="left").pack()

                # Add a horizontal line between each book entry
                ttk.Separator(show_books_window, orient="horizontal").pack(fill="x", pady=5)


        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")
    

    def delete_book_entry(self):
        book_id = simpledialog.askinteger("Delete Book Entry", "Enter Book ID to delete:")

        if book_id:
            query = "DELETE FROM books WHERE bkid = %s"
            value = (book_id,)

            try:
                self.cursor.execute(query, value)
                self.db.commit()
                messagebox.showinfo("Success", "Book entry deleted successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Error: {e}")
        else:
            messagebox.showwarning("Warning", "Please provide a valid Book ID.")


    
app = LibraryApp(root)
root.mainloop()

