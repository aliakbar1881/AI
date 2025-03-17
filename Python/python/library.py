import json
import os

# دیتای دیفالت اگه فایل موجود نباشه
default_library = [
    {"title": "Python Basics", "copies": 3, "is_borrowed": False},
    {"title": "Learn Coding", "copies": 2, "is_borrowed": True}
]

# تابع برای خوندن دیتا از فایل یا مقداردهی اولیه
def load_library(filename="library.json"):
    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError):
            print("Error reading file. Loading default data.")
            return default_library
    else:
        print("No library file found. Creating with default data.")
        with open(filename, "w") as file:
            json.dump(default_library, file, indent=4)
        return default_library

# تابع برای ذخیره دیتا توی فایل
def save_library(library, filename="library.json"):
    try:
        with open(filename, "w") as file:
            json.dump(library, file, indent=4)
        print("Library saved successfully!")
    except IOError:
        print("Error saving library to file!")

# تابع برای اضافه کردن کتاب
def add_book(library):
    try:
        title = input("Enter book title: ")
        copies = int(input("Enter number of copies: "))
        if copies < 0:
            print("Copies cannot be negative!")
            return
        new_book = {"title": title, "copies": copies, "is_borrowed": False}
        library.append(new_book)
        save_library(library)
        print(f"Added '{title}' successfully!")
    except ValueError:
        print("Please enter a valid number for copies!")

# تابع برای نمایش کتاب‌ها
def view_books(library):
    if len(library) == 0:
        print("No books in library!")
    else:
        print("\nLibrary Books:")
        for book in library:
            status = "Borrowed" if book["is_borrowed"] else "Available"
            print(f"Title: {book['title']}, Copies: {book['copies']}, Status: {status}")

# تابع برای حذف کتاب
def remove_book(library):
    title = input("Enter title to remove: ")
    for i, book in enumerate(library):
        if book["title"].lower() == title.lower():
            library.pop(i)
            save_library(library)
            print(f"Removed '{title}' successfully!")
            return
    print("Book not found!")

# تابع برای تغییر وضعیت امانت
def toggle_borrow_status(library):
    title = input("Enter title to toggle borrow status: ")
    for book in library:
        if book["title"].lower() == title.lower():
            book["is_borrowed"] = not book["is_borrowed"]
            save_library(library)
            status = "borrowed" if book["is_borrowed"] else "available"
            print(f"'{title}' is now {status}!")
            return
    print("Book not found!")

# تابع برای جستجوی کتاب
def search_book(library):
    query = input("Enter title or part of it to search: ").lower()
    found = False
    for book in library:
        if query in book["title"].lower():
            status = "Borrowed" if book["is_borrowed"] else "Available"
            print(f"Found: {book['title']}, Copies: {book['copies']}, Status: {status}")
            found = True
    if not found:
        print("No matching books found!")

# برنامه اصلی
library = load_library()  # بارگذاری اولیه دیتا

while True:
    print("\nLibrary Management System")
    print("1. Add a book")
    print("2. View all books")
    print("3. Remove a book")
    print("4. Toggle borrow status")
    print("5. Search for a book")
    print("6. Exit")
    choice = input("Enter your choice (1-6): ")

    if choice == "1":
        add_book(library)
    elif choice == "2":
        view_books(library)
    elif choice == "3":
        remove_book(library)
    elif choice == "4":
        toggle_borrow_status(library)
    elif choice == "5":
        search_book(library)
    elif choice == "6":
        save_library(library)
        print("Goodbye!")
        break
    else:
        print("Invalid choice! Please enter a number between 1 and 6.")