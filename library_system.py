import asyncio
from datetime import datetime, timedelta
from typing import Dict, List


# BOOK DATABASE

books: List[Dict] = [
    {"id": 1, "title": "Python Basics", "author": "Tanu Jalloh", "category": "Programming", "available": True},
    {"id": 2, "title": "Web Design Mastery", "author": "Alhaji Mustapha", "category": "Design", "available": True},
    {"id": 3, "title": "Database Systems", "author": "Amina Diallo", "category": "IT", "available": True},
    {"id": 4, "title": "AI Introduction", "author": "Fatmata Diallo", "category": "AI", "available": True},
    {"id": 5, "title": "Networking Fundamentals", "author": "Abdulai Jalloh", "category": "IT", "available": True}
]

# user_id -> {book_id -> borrow info}
borrow_records: Dict[int, Dict[int, Dict]] = {}

lock = asyncio.Lock()

# BORROW BOOK

async def borrow_book(user_id: int, book_id: int):
    await asyncio.sleep(1)

    async with lock:
        for book in books:
            if book["id"] == book_id:

                if not book["available"]:
                    return f"User {user_id}: Book not available"

                book["available"] = False
                due_date = datetime.now() + timedelta(days=7)

                if user_id not in borrow_records:
                    borrow_records[user_id] = {}

                borrow_records[user_id][book_id] = {
                    "due_date": due_date
                }

                return f"User {user_id} borrowed {book['title']}"

        return f"User {user_id}: Book not found"


# RETURN BOOK

async def return_book(user_id: int, book_id: int):
    await asyncio.sleep(1)

    async with lock:

        if user_id not in borrow_records or book_id not in borrow_records[user_id]:
            return f"User {user_id}: No record found"

        record = borrow_records[user_id][book_id]
        due_date = record["due_date"]

        # mark available
        for book in books:
            if book["id"] == book_id:
                book["available"] = True
                book_title = book["title"]

        # fine calculation
        fine = 0
        if datetime.now() > due_date:
            fine = (datetime.now() - due_date).days * 1000

        del borrow_records[user_id][book_id]
        if not borrow_records[user_id]:
            del borrow_records[user_id]

        return f"User {user_id} returned {book_title} | Fine: {fine}"


# MAIN (CONCURRENT TEST)

async def main():

    print("\n--- BORROWING (MULTIPLE USERS) ---")

    results = await asyncio.gather(
        borrow_book(1, 1),   # success
        borrow_book(2, 1),   # fails (same book)
        borrow_book(3, 2)    # success
    )

    for r in results:
        print(r)

    print("\n--- RETURN & RE-BORROW ---")

    results2 = await asyncio.gather(
        return_book(1, 1),   # return book
        borrow_book(4, 1)    # another user borrows same book
    )

    for r in results2:
        print(r)

# RUN PROGRAM
asyncio.run(main())