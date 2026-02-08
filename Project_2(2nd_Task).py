import json
import os

class Book:
    def __init__(self, title, author, book_id, issued=False):
        self.title = title
        self.author = author
        self.book_id = book_id
        self.issued = issued

    def to_dict(self):
        return {
            'title': self.title,
            'author': self.author,
            'book_id': self.book_id,
            'issued': self.issued
        }

    @staticmethod
    def from_dict(data):
        return Book(data['title'], data['author'], data['book_id'], data.get('issued', False))

class Library:
    def __init__(self, filename='books.json'):
        self.filename = filename
        self.books = self.load_books()
        self.book_dict = {b.book_id: b for b in self.books}

    def load_books(self):
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, 'r') as f:
            try:
                data = json.load(f)
                return [Book.from_dict(b) for b in data]
            except json.JSONDecodeError:
                return []

    def save_books(self):
        with open(self.filename, 'w') as f:
            json.dump([b.to_dict() for b in self.books], f, indent=2)

    def add_book(self, title, author, book_id):
        if book_id in self.book_dict:
            print(f"Error: Book ID '{book_id}' already exists.")
            return False
        book = Book(title, author, book_id)
        self.books.append(book)
        self.book_dict[book_id] = book
        self.save_books()
        print(f"Book '{title}' added.")
        return True

    def search_books(self, query, by='title'):
        results = []
        for b in self.books:
            if by == 'title' and query.lower() in b.title.lower():
                results.append(b)
            elif by == 'author' and query.lower() in b.author.lower():
                results.append(b)
        return results

    def issue_book(self, book_id):
        book = self.book_dict.get(book_id)
        if not book:
            print(f"Error: Book ID '{book_id}' not found.")
            return False
        if book.issued:
            print(f"Error: Book '{book.title}' is already issued.")
            return False
        book.issued = True
        self.save_books()
        print(f"Book '{book.title}' issued.")
        return True

    def return_book(self, book_id):
        book = self.book_dict.get(book_id)
        if not book:
            print(f"Error: Book ID '{book_id}' not found.")
            return False
        if not book.issued:
            print(f"Error: Book '{book.title}' is not issued.")
            return False
        book.issued = False
        self.save_books()
        print(f"Book '{book.title}' returned.")
        return True

    def report(self):
        total = len(self.books)
        issued = sum(1 for b in self.books if b.issued)
        print(f"Total books: {total}")
        print(f"Issued books: {issued}")
        print(f"Available books: {total - issued}")

    def list_books(self):
        if not self.books:
            print("No books found.")
            return
        print("{:<10} {:<30} {:<20} {:<10}".format("ID", "Title", "Author", "Issued"))
        print("-"*75)
        for b in self.books:
            print("{:<10} {:<30} {:<20} {:<10}".format(b.book_id, b.title, b.author, "Yes" if b.issued else "No"))


def main():
    library = Library()
    while True:
        print("\nLibrary Manager")
        print("1. Add Book")
        print("2. Search Book by Title")
        print("3. Search Book by Author")
        print("4. Issue Book")
        print("5. Return Book")
        print("6. List Books")
        print("7. Report")
        print("8. Exit")
        choice = input("Select an option (1-8): ")
        if choice == '1':
            title = input("Enter title: ")
            author = input("Enter author: ")
            book_id = input("Enter book ID: ")
            library.add_book(title, author, book_id)
        elif choice == '2':
            query = input("Enter title to search: ")
            results = library.search_books(query, by='title')
            if results:
                for b in results:
                    print(f"ID: {b.book_id}, Title: {b.title}, Author: {b.author}, Issued: {'Yes' if b.issued else 'No'}")
            else:
                print("No books found.")
        elif choice == '3':
            query = input("Enter author to search: ")
            results = library.search_books(query, by='author')
            if results:
                for b in results:
                    print(f"ID: {b.book_id}, Title: {b.title}, Author: {b.author}, Issued: {'Yes' if b.issued else 'No'}")
            else:
                print("No books found.")
        elif choice == '4':
            book_id = input("Enter book ID to issue: ")
            library.issue_book(book_id)
        elif choice == '5':
            book_id = input("Enter book ID to return: ")
            library.return_book(book_id)
        elif choice == '6':
            library.list_books()
        elif choice == '7':
            library.report()
        elif choice == '8':
            print("Exiting.")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
