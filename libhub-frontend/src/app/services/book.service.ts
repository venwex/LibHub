import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { Book } from '../models/book';

@Injectable({
  providedIn: 'root'
})
export class BookService {

  private apiUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  searchBooks(query: string): Observable<Book[]> {
    return this.http.get<any[]>(`${this.apiUrl}/books/search/?q=${encodeURIComponent(query)}`).pipe(
      map(books => books.map(book => this.mapToBook(book)))
    );
  }

  getBookById(id: number): Observable<Book> {
    return this.http.get<any>(`${this.apiUrl}/books/${id}/`).pipe(
      map(book => this.mapToBook(book))
    );
  }

  getPopularBooks(): Observable<Book[]> {
    return this.http.get<any[]>(`${this.apiUrl}/books/popular/`).pipe(
      map(books => books.map(book => this.mapToBook(book)))
    );
  }

  private mapToBook(raw: any): Book {
    return {
      id: raw.id,
      title: raw.title,
      author: raw.author,
      language: raw.language,
      fileType: raw.file_type,
      fileUrl: raw.file_url,
      datePublished: new Date(raw.date_published),
      dateUploaded: new Date(raw.date_uploaded),
      rating: raw.rating,
      coverImage: raw.coverImage,
      genres: raw.genres,
      description: raw.description,
      pages: raw.pages,
      isbn: raw.isbn
    };
  }
}

 /*
  // Если вдруг понадобится тест без сервера — можно раскомментировать ↓↓↓

  private mockBooks: Book[] = [
    {
      id: 1,
      title: 'The Great Gatsby',
      author: 'F. Scott Fitzgerald',
      language: 'English',
      fileType: 'PDF',
      fileUrl: '#',
      datePublished: new Date('1925-04-10'),
      dateUploaded: new Date(),
      rating: 4.5,
      coverImage: 'https://m.media-amazon.com/images/I/71FTb9X6wsL._AC_UF1000,1000_QL80_.jpg',
      genres: ['Classic', 'Fiction'],
      description: 'A story of wealth, love, and the American Dream in the 1920s.',
      pages: 218
    },
    {
      id: 2,
      title: 'To Kill a Mockingbird',
      author: 'Harper Lee',
      language: 'English',
      fileType: 'EPUB',
      fileUrl: '#',
      datePublished: new Date('1960-07-11'),
      dateUploaded: new Date(),
      rating: 4.8,
      coverImage: 'https://m.media-amazon.com/images/I/71FxgtFKcQL._AC_UF1000,1000_QL80_.jpg',
      genres: ['Classic', 'Drama'],
      description: 'A powerful story of racial injustice and moral growth.',
      pages: 281
    }
  ];

  searchBooks(query: string): Observable<Book[]> {
    const term = query.toLowerCase();
    return of(
      this.mockBooks.filter(book =>
        book.title.toLowerCase().includes(term) ||
        book.author.toLowerCase().includes(term)
      )
    );
  }

  getBookById(id: number): Observable<Book> {
    const book = this.mockBooks.find(b => b.id === id);
    return book ? of(book) : throwError(() => new Error('Book not found'));
  }

  getPopularBooks(): Observable<Book[]> {
    return of([...this.mockBooks].sort((a, b) => b.rating - a.rating));
  }
  */