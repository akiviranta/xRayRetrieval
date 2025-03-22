import React, { useState } from 'react';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searchType, setSearchType] = useState('text'); // 'text' or 'image'
  const [imagePreview, setImagePreview] = useState(null);
  const [selectedImage, setSelectedImage] = useState(null);

  const handleTextSearch = async (e) => {
    e.preventDefault();
    
    if (!query.trim()) return;
    
    setLoading(true);
    setError(null);
    
    try {
      console.log('About to send fetch request');
      const response = await fetch('http://localhost:8000/api/search/text', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });
      console.log('Fetch request completed');
      
      if (!response.ok) {
        throw new Error('Search request failed');
      }
      
      const data = await response.json();
      setResults(data.results);
    } catch (err) {
      setError(err.message);
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedImage(file);
      
      // Create a preview URL
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleImageSearch = async (e) => {
    e.preventDefault();
    
    if (!selectedImage) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const formData = new FormData();
      formData.append('image', selectedImage);
      
      const response = await fetch('http://localhost:8000/api/search/image', {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error('Image search request failed');
      }
      
      const data = await response.json();
      setResults(data.results);
    } catch (err) {
      setError(err.message);
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>CLIP Multimodal Search System</h1>
      </header>
      
      <main className="App-main">
        <div className="search-type-selector">
          <button 
            className={`search-type-btn ${searchType === 'text' ? 'active' : ''}`} 
            onClick={() => setSearchType('text')}
          >
            Text Search
          </button>
          <button 
            className={`search-type-btn ${searchType === 'image' ? 'active' : ''}`} 
            onClick={() => setSearchType('image')}
          >
            Image Search
          </button>
        </div>

        {searchType === 'text' ? (
          <form className="search-form" onSubmit={handleTextSearch}>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Enter your search query..."
              className="search-input"
            />
            <button type="submit" className="search-button" disabled={loading}>
              {loading ? 'Searching...' : 'Search'}
            </button>
          </form>
        ) : (
          <form className="search-form" onSubmit={handleImageSearch}>
            <div className="image-upload-container">
              <input
                type="file"
                accept="image/*"
                onChange={handleImageUpload}
                className="image-input"
                id="image-input"
              />
              <label htmlFor="image-input" className="image-input-label">
                {imagePreview ? 'Change Image' : 'Select Image'}
              </label>
              
              {imagePreview && (
                <div className="image-preview">
                  <img src={imagePreview} alt="Preview" />
                </div>
              )}
            </div>
            <button type="submit" className="search-button" disabled={loading || !selectedImage}>
              {loading ? 'Searching...' : 'Search'}
            </button>
          </form>
        )}
        
        {error && <div className="error-message">{error}</div>}
        
        <div className="results-container">
          {results.length > 0 ? (
            <div>
              <h2>Search Results</h2>
              <ul className="results-list">
                {results.map((result, index) => (
                  <li key={result.id || index} className="result-item">
                    <div className="result-score">Score: {result.score.toFixed(4)}</div>
                    <div className="result-payload">
                      {result.payload && result.payload.decoded_texts && (
                        <div className="payload-text">
                          <strong>Text:</strong> {result.payload.decoded_texts}
                        </div>
                      )}
                      {result.payload && result.payload.source && (
                        <div className="payload-source">
                          <strong>Source:</strong> {result.payload.source}
                        </div>
                      )}
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          ) : !loading && ((searchType === 'text' && query) || 
                           (searchType === 'image' && selectedImage)) && !error ? (
            <p>No results found</p>
          ) : null}
        </div>
      </main>
    </div>
  );
}

export default App;