import React, { useState, useEffect, useCallback } from "react";
import BookForm from "./components/BookForm";
import BookCard from "./components/BookCard";
import {
  getAllBooks,
  createBook,
  updateBook,
  deleteBook,
} from "./services/bookService";

function App() {
  const [books, setBooks] = useState([]);
  const [bookToEdit, setBookToEdit] = useState(null);
  const [loading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [ratingFilter, setRatingFilter] = useState("");
  const loadBooks = useCallback(async () => {
    try {
      setIsLoading(true);
      const data = await getAllBooks(searchQuery, ratingFilter);
      setBooks(data);
      setError(null);
    } catch (err) {
      setError("Gagal memuat data buku. Pastikan server berjalan.");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  }, [searchQuery, ratingFilter])

  useEffect(() => {
    loadBooks();
  }, [loadBooks]);

  const handleSubmit = async (data) => {
    try {
      if (bookToEdit) {
        await updateBook(bookToEdit.id, data);
        alert("Buku berhasil diupdate!");
        setBookToEdit(null);
      } else {
        await createBook(data);
        alert("Buku berhasil ditambahkan!");
      }
      loadBooks();
    } catch (err) {
      console.error(err);
    }
  };

  const handleEdit = (book) => {
    setBookToEdit(book);

    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleCancelEdit = () => {
    setBookToEdit(null);
  };

  const handleDelete = async (id) => {
    if (window.confirm("Apakah Anda yakin ingin menghapus buku ini?")) {
      try {
        await deleteBook(id);
        alert("Buku berhasil dihapus!");
        loadBooks();
      } catch (err) {
        console.error(err);
      }
    }
  };

  const ratingOptions = [
    { label: "Semua", value: "" },
    { label: "⭐⭐⭐", value: "excellent" },
    { label: "⭐⭐", value: "average" },
    { label: "⭐", value: "bad" },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 py-8">
      <div className="container mx-auto px-4 max-w-6xl">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            📚 Perpustakaan Digital
          </h1>
          <p className="text-gray-600">
            Kelola koleksi buku favoritmu dengan mudah!
          </p>
        </div>

        {/* Form Tambah/Edit Buku */}
        <BookForm
          onSubmit={handleSubmit}
          bookToEdit={bookToEdit}
          onCancel={handleCancelEdit}
        />

        {/* Search bar */}
        <div className="mb-6 bg-white p-4 rounded-lg shadow-md">
          <input
            type="text"
            placeholder="🔍 Cari buku berdasarkan judul atau penulis..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {/* Filter berdasarkan rating */}
        <div className="flex justify-center gap-2 mb-6">
          {ratingOptions.map((option) => (
            <button
              key={option.value}
              onClick={() => setRatingFilter(option.value)}
              className={`
                px-4 py-2 rounded-lg font-semibold transition-all
                ${ratingFilter === option.value
                  ? "bg-blue-600 text-white shadow-md"
                  : "bg-white text-gray-700 hover:bg-gray-100"
                }
              `}
            >
              {option.label}
            </button>
          ))}
        </div>

        {/* Tampilkan Loading */}
        {loading && (
          <div className="text-center py-8">
            <p className="text-xl text-gray-600">⏳ Memuat data...</p>
          </div>
        )}

        {/* Tampilkan Error */}
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            <p>{error}</p>
          </div>
        )}

        {/* Daftar Buku */}
        {!loading && !error && (
          <div>
            <h2 className="text-2xl font-bold text-gray-800 mb-4">
              Daftar Buku ({books.length})
            </h2>

            {books.length === 0 ? (
              <div className="text-center py-12 bg-white rounded-lg shadow-md">
                <p className="text-xl text-gray-500">
                  📭 Belum ada buku. Yuk tambah buku!
                </p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {books.map((book) => (
                  <BookCard
                    key={book.id}
                    book={book}
                    onEdit={handleEdit}
                    onDelete={handleDelete}
                  />
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
export default App;