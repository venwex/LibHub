import { Component, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute, Router, ParamMap } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { BookService } from '../services/book.service';
import { Book } from '../models/book';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-search-results',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './search-results.component.html',
  styleUrls: ['./search-results.component.css']
})
export class SearchResultsComponent implements OnInit, OnDestroy {
  books: Book[] = [];
  searchQuery: string = '';
  isLoading: boolean = false;
  errorMessage: string = '';
  routeSub!: Subscription;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private bookService: BookService
  ) {}

  ngOnInit() {
    this.routeSub = this.route.paramMap.subscribe((params: ParamMap) => {
      this.searchQuery = params.get('query') || '';
      if (this.searchQuery) {
        this.performSearch();
      } else {
        this.books = [];
        this.errorMessage = 'No search query provided.';
      }
    });
  }

  onSearch() {
    const trimmedQuery = this.searchQuery.trim();
    if (trimmedQuery) {
      this.router.navigate(['/search', trimmedQuery]);
    }
  }

  private performSearch() {
    this.isLoading = true;
    this.errorMessage = '';

    this.bookService.searchBooks(this.searchQuery).subscribe({
      next: (books) => {
        this.books = books;
        this.isLoading = false;
      },
      error: (err) => {
        this.errorMessage = 'Failed to load search results. Please try again.';
        this.isLoading = false;
        console.error('Search error:', err);
      }
    });
  }

  viewBookDetails(bookId: number) {
    this.router.navigate(['/books', bookId]);
  }

  ngOnDestroy() {
    if (this.routeSub) {
      this.routeSub.unsubscribe();
    }
  }
}