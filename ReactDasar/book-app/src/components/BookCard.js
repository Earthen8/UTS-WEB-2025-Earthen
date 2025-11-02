import React from "react";

function MahasiswaCard({ book, onEdit, onDelete }) { 
  const formatDate = (dateString) => {
    if (!dateString) return "Tanggal tidak diketahui";
    const date = new Date(dateString);
    return date.toLocaleDateString("id-ID", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  };

  return (
    <div className="bg-white p-5 rounded-lg shadow-md hover:shadow-lg transition duration-200">
      {book.cover_image && (
        <img
          src={book.cover_image}
          alt={book.name}
          // 'h-48' dihapus dan diganti dengan 'aspect-[2/3]'
          className="w-full aspect-[2/3] object-cover rounded-md mb-4"
        />
      )}
      
      <h3 className="text-xl font-bold text-gray-800 mb-2">
        📚 {book.name} 
      </h3>

      <p className="text-gray-600 mb-2">
        <span className="font-semibold">Author:</span> {book.author}
      </p>

      <p className="text-gray-600 mb-2">
        <span className="font-semibold">Rating:</span> {book.rating}
      </p>

      <p className="text-gray-500 text-sm mb-4">
        Ditambahkan: {formatDate(book.uploaded)}
      </p>
      
      <div className="flex gap-2">
        <button
          onClick={() => onEdit(book)}
          className="bg-yellow-500 text-white px-4 py-2 rounded hover:bg-yellow-600 transition duration-200"
        >
          ✏ Edit
        </button>
        <button
          onClick={() => onDelete(book.id)}
          className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 transition duration-200"
        >
          🗑 Hapus
        </button>
      </div>
    </div>
  );
}

export default MahasiswaCard; // Ganti ekspor juga