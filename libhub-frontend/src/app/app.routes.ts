import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { SearchResultsComponent } from './search-results/search-results.component';
import { BookListComponent } from './book-list/book-list.component';
import { BookDetailComponent } from './book-detail/book-detail.component';
import { AboutUsComponent } from './about-us/about-us.component';

export const routes: Routes = [
    { path: '', component: HomeComponent, title: 'LibHub - Home' },
    { path: 'about', component: AboutUsComponent, title: 'About LibHub' },
    { path: 'search/:query', component: SearchResultsComponent, title: 'Search Results' },

    { path: 'books', component: BookListComponent },
    { path: 'books/:id', component: BookDetailComponent },

    { path: '**', redirectTo: '' },
];
