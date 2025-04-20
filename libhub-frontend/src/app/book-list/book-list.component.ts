import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Book } from '../models/book';
import { BookService } from '../services/book.service';

@Component({
  selector: 'app-book-list',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './book-list.component.html',
  styleUrls: ['./book-list.component.css']
})
export class BookListComponent implements OnInit {
  books: Book[] = [];
  isLoading = true;

  constructor(private bookService: BookService) {
    console.log('BookListComponent created'); // Debug log
  }

  ngOnInit() {
    console.log('Fetching books...'); // Debug log
    this.bookService.getPopularBooks().subscribe({
      next: (books) => {
        console.log('Books received:', books); // Debug log
        this.books = books;
        this.isLoading = false;
      },
      error: (err) => {
        console.error('Error loading books:', err);
        this.isLoading = false;
      }
    });
  }

  
}
