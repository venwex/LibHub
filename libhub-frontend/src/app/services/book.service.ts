import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of, throwError } from 'rxjs';
import { Book } from '../models/book';

@Injectable({
  providedIn: 'root'
})
export class BookService {
  // Mock data for testing - replace with actual API calls
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

  constructor(private http: HttpClient) {}

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
  console.log('Getting book by ID:', id);
  const book = this.mockBooks.find(b => b.id === id);
  console.log('Found book:', book);
  return book ? of(book) : throwError(() => new Error('Book not found'));
}

  getPopularBooks(): Observable<Book[]> {
    // Return sorted by rating
    return of([...this.mockBooks].sort((a, b) => b.rating - a.rating));
  }
}

/*
export class BookService {
  // !!!!!!!!!!!!!!!!!
  // REALLY IMPORTANT: replace later with api url!!!!!
  // !!!!!!!!!!!!!!!!!
  private apiUrl = 'http://your-api-url.com/api';
  // !!!!!!!!!!!!!!!!!
  // !!!!!!!!!!!!!!!!!

  constructor(private http: HttpClient) {}

  searchBooks(query: string): Observable<Book[]> {
    return this.http.get<Book[]>(`${this.apiUrl}/books/search?q=${encodeURIComponent(query)}`);
  }

  getBookById(id: number): Observable<Book> {
    return this.http.get<Book>(`${this.apiUrl}/books/${id}`);
  }

  getPopularBooks(): Observable<Book[]> {
    return this.http.get<Book[]>(`${this.apiUrl}/books/popular`);
  }
}
*/
