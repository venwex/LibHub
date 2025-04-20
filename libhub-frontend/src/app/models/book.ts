export interface Book {
  id: number;
  title: string;
  author: string;
  language: string;
  fileType: string;
  fileUrl: string;
  datePublished: Date;
  dateUploaded: Date;
  rating: number;
  coverImage: string;
  genres: string[]; // a book can have multiple genres
  description?: string; // optional
  pages?: number;
  isbn?: string;
}
