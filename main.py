from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

from database import Base
Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Mobile Library API is running"}


@app.post("/books")
def add_book(
    google_book_id: str,
    title: str,
    author: str,
    image_url: str,
    description: str,
    page_count: int,
    db: Session = Depends(get_db)
):
    if google_book_id.strip() == "" or title.strip() == "" or author.strip() == "":
        return {"message": "Book information cannot be empty"}

    existing_book = db.query(models.Book).filter(
        models.Book.google_book_id == google_book_id
    ).first()

    if existing_book:
        return existing_book

    new_book = models.Book(
        google_book_id=google_book_id,
        title=title,
        author=author,
        image_url=image_url,
        description=description,
        page_count=page_count
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@app.get("/books")
def get_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()


VALID_STATUS = ["Plan to Read", "Reading", "Completed"]


@app.post("/userbooks")
def add_user_book(
    user_id: int,
    book_id: int,
    current_page: int,
    status: str,
    db: Session = Depends(get_db)
):
    if status not in VALID_STATUS:
        return {"message": "Invalid status"}

    existing = db.query(models.UserBook).filter(
        models.UserBook.user_id == user_id,
        models.UserBook.book_id == book_id
    ).first()

    if existing:
        existing.current_page = current_page
        existing.status = status

        db.commit()
        db.refresh(existing)

        return existing

    new_user_book = models.UserBook(
        user_id=user_id,
        book_id=book_id,
        current_page=current_page,
        status=status
    )

    db.add(new_user_book)
    db.commit()
    db.refresh(new_user_book)

    return new_user_book


@app.get("/userbooks")
def get_user_books(db: Session = Depends(get_db)):
    return db.query(models.UserBook).all()


@app.get("/userbooks/{user_id}")
def get_user_books_by_user(user_id: int, db: Session = Depends(get_db)):
    user_books = db.query(models.UserBook).filter(
        models.UserBook.user_id == user_id
    ).all()

    result = []

    for user_book in user_books:
        book = db.query(models.Book).filter(
            models.Book.id == user_book.book_id
        ).first()

        if book:
            result.append({
                "google_book_id": book.google_book_id,
                "title": book.title,
                "author": book.author,
                "image_url": book.image_url,
                "description": book.description,
                "page_count": book.page_count,
                "current_page": user_book.current_page,
                "status": user_book.status
            })

    return result


@app.delete("/userbooks")
def delete_user_book(
    user_id: int,
    google_book_id: str,
    db: Session = Depends(get_db)
):
    book = db.query(models.Book).filter(
        models.Book.google_book_id == google_book_id
    ).first()

    if not book:
        return {"message": "Book not found"}

    user_book = db.query(models.UserBook).filter(
        models.UserBook.user_id == user_id,
        models.UserBook.book_id == book.id
    ).first()

    if not user_book:
        return {"message": "User book not found"}

    db.delete(user_book)
    db.commit()

    return {"message": "Book removed from library"}


@app.put("/userbooks/{id}")
def update_status(id: int, status: str, db: Session = Depends(get_db)):
    if status not in VALID_STATUS:
        return {"message": "Invalid status"}

    userbook = db.query(models.UserBook).filter(models.UserBook.id == id).first()

    if not userbook:
        return {"message": "Not found"}

    userbook.status = status
    db.commit()

    return {"message": "Status updated"}


@app.post("/users")
def add_user(full_name: str, username: str, password: str, db: Session = Depends(get_db)):
    if full_name.strip() == "" or username.strip() == "" or password.strip() == "":
        return {"message": "Full name, username and password cannot be empty"}

    existing_user = db.query(models.User).filter(models.User.username == username).first()

    if existing_user:
        return {"message": "Username already exists"}

    new_user = models.User(
        full_name=full_name,
        username=username,
        password=password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Register successful",
        "user_id": new_user.id,
        "username": new_user.username,
        "full_name": new_user.full_name
    }


@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@app.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    if username.strip() == "" or password.strip() == "":
        return {"message": "Username and password cannot be empty"}

    user = db.query(models.User).filter(models.User.username == username).first()

    if not user:
        return {"message": "User not found"}

    if user.password != password:
        return {"message": "Wrong password"}

    return {
        "message": "Login successful",
        "user_id": user.id,
        "username": user.username,
        "full_name": user.full_name
    }


@app.post("/comments")
def add_comment(user_id: int, book_id: int, text: str, db: Session = Depends(get_db)):
    if text.strip() == "":
        return {"message": "Comment cannot be empty"}

    new_comment = models.Comment(
        user_id=user_id,
        book_id=book_id,
        text=text
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


@app.get("/comments")
def get_comments(db: Session = Depends(get_db)):
    return db.query(models.Comment).all()


@app.post("/journal")
def add_journal_note(user_id: int, book_id: int, note_text: str, db: Session = Depends(get_db)):
    if note_text.strip() == "":
        return {"message": "Journal note cannot be empty"}

    new_note = models.JournalNote(
        user_id=user_id,
        book_id=book_id,
        note_text=note_text
    )

    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return {
        "message": "Journal note added",
        "note_id": new_note.id,
        "user_id": new_note.user_id,
        "book_id": new_note.book_id,
        "note_text": new_note.note_text
    }


@app.get("/journal/{user_id}")
def get_journal_notes(user_id: int, db: Session = Depends(get_db)):
    notes = db.query(models.JournalNote).filter(
        models.JournalNote.user_id == user_id
    ).all()

    return notes

@app.post("/journal_entries")
def add_journal_entry(
    user_id: int,
    google_book_id: str,
    entry_type: str,
    text: str,
    page_number: int = 0,
    db: Session = Depends(get_db)
):
    if text.strip() == "":
        return {"message": "Journal entry cannot be empty"}

    if entry_type not in ["expectation", "note", "quote", "final_thought"]:
        return {"message": "Invalid journal entry type"}

    new_entry = models.JournalEntry(
        user_id=user_id,
        google_book_id=google_book_id,
        entry_type=entry_type,
        page_number=page_number,
        text=text
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return new_entry


@app.get("/journal_entries/{user_id}")
def get_journal_entries(user_id: int, db: Session = Depends(get_db)):
    entries = db.query(models.JournalEntry).filter(
        models.JournalEntry.user_id == user_id
    ).all()

    return entries
@app.delete("/journal_entries")
def delete_journal_entry(
    user_id: int,
    google_book_id: str,
    entry_type: str,
    page_number: int,
    text: str,
    db: Session = Depends(get_db)
):
    entry = db.query(models.JournalEntry).filter(
        models.JournalEntry.user_id == user_id,
        models.JournalEntry.google_book_id == google_book_id,
        models.JournalEntry.entry_type == entry_type,
        models.JournalEntry.page_number == page_number,
        models.JournalEntry.text == text
    ).first()

    if not entry:
        return {"message": "Entry not found"}

    db.delete(entry)
    db.commit()

    return {"message": "Entry deleted"}