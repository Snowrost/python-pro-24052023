from datetime import datetime
import json

from bs4 import BeautifulSoup


def main():
    with open("books.xml", "r") as f:
        soup = BeautifulSoup(f.read(), "xml")

    book_list = []
    for book in soup.find_all("book"):
        book_list.append(
            {
                "id": book["id"],
                "author": book.author.string,
                "title": book.title.string,
                "genre": book.genre.string,
                "price": float(book.price.string),
                "publication_date": str(datetime.strptime(
                    str(book.pub_date.string), "%Y-%m-%d"
                )),
                "review": book.review.string,
            }
        )

    print(json.dumps(book_list, indent=4))



if __name__ == "__main__":
    main()
