import axios from 'axios';

const API_URL = 'http://localhost:8000/basic/';

// Fungsi untuk mengambil semua buku
export const getAllBooks = async (query = "", rating = "") => {
  try {
    const params = { search: query };
    if (rating) {
      params.rating = rating;
    }
    const response = await axios.get(API_URL, { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching books:', error);
    throw error;
  }
};

// Fungsi untuk menambahkan buku baru
export const createBook = async (formData) => {
  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      body: formData,
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
  } catch (error) {
    console.error('Error creating book:', error);
    throw error;
  }
};

// Fungsi untuk delete buku
export const deleteBook = async (id) => {
  try {
    await axios.delete(`${API_URL}${id}/`);
  } catch (error) {
    console.error('Error deleting book:', error);
    throw error;
  }
};

// Fungsi untuk update buku
export const updateBook = async (id, bookData) => {
  try {
    const response = await fetch(`${API_URL}${id}/`, {
      method: 'PATCH',
      body: bookData,
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
  } catch (error) {
    console.error('Error updating book:', error);
    throw error;
  }
};