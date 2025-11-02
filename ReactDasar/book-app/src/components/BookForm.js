import React, {useState, useEffect} from "react";

function BookForm({ onSubmit, bookToEdit, onCancel}){
  const [formData, setFormData] = useState({
    name: "",
    author: "", 
    rating: "average",
  });

  const [coverImage, setCoverImage] = useState(null);

  useEffect(() => {
    if (bookToEdit) {
      setFormData({
        name: bookToEdit.name,
        author: bookToEdit.author,
        rating: bookToEdit.rating || "average",
      });
      setCoverImage(null); 
    }
  }, [bookToEdit]);
  

  const handleChange = (e) => {
    const { name, value } = e.target; // Destructuring is fine, but not used in the original buggy implementation
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    })
  );
};

  const handleFileChange = (e) => {
    setCoverImage(e.target.files[0]);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const data = new FormData();
    data.append('name', formData.name);
    data.append('author', formData.author);
    data.append('rating', formData.rating);
    if (coverImage) {
      data.append("cover_image", coverImage);
    }
    onSubmit(data);
    setFormData({ name: "", author: "", rating: "average" });
    setCoverImage(null);
    e.target.reset();
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md mb-6" >
      <h2 className="text-2xl font-bold mb-4 text-gray-600">
        {bookToEdit ? "Edit Book" : "Add New Book"}
      </h2>

      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-gray-700 font-semibold mb-2" >
            Name:
          </label>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        <div className="mb-4">
          <label className="block text-gray-700 font-semibold mb-2" >
            Author:
          </label>
          <input
            type="text"
            name="author"
            value={formData.author}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Masukkan nama penulis"
            required
          />
        </div>  

        <div className="mb-4">
          <label className="block text-gray-700 font-semibold mb-2" >
            Rating:
          </label>
          <select
            name="rating"
            value={formData.rating}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="excellent">Excellent</option>
            <option value="average">Average</option>
            <option value="bad">Bad</option>
          </select>
        </div>

        <div className="mb-4">
          <label className="block text-gray-700 font-semibold mb-2">
            Cover Image:
          </label>
          <input
            type="file"
            name="cover_image"
            onChange={handleFileChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg"
          />
        </div>

        <div className="flex gap-2">
          <button
            type="submit"
            className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors" >
            {bookToEdit ? "Update Book" : "Add Book"}
          </button>
          {bookToEdit && (<button type="button" onClick={onCancel} className="bg-gray-500 text-white px-4 py-2 rounded-lg hover:bg-gray-600 transition-colors">
            Cancel
          </button>
          )}
        </div>
      </form>
    </div>
  );
}

export default BookForm;