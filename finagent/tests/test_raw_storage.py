import os
import tempfile
import json
import unittest
from unittest.mock import patch, MagicMock

from finagent.raw_storage import store_raw_responses, load_raw_responses


class TestRawStorage(unittest.TestCase):
    """Test cases for the raw_storage module."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        
        # Sample API responses
        self.sample_newsapi_response = {
            "status": "ok",
            "totalResults": 2,
            "articles": [
                {
                    "source": {"id": "source-1", "name": "News Source 1"},
                    "author": "Author 1",
                    "title": "Test Article 1",
                    "description": "Description of test article 1",
                    "url": "https://example.com/article1",
                    "urlToImage": "https://example.com/image1.jpg",
                    "publishedAt": "2023-01-01T12:00:00Z",
                    "content": "Content of test article 1"
                },
                {
                    "source": {"id": "source-2", "name": "News Source 2"},
                    "author": "Author 2",
                    "title": "Test Article 2",
                    "description": "Description of test article 2",
                    "url": "https://example.com/article2",
                    "urlToImage": "https://example.com/image2.jpg",
                    "publishedAt": "2023-01-02T12:00:00Z",
                    "content": "Content of test article 2"
                }
            ]
        }
        
        self.sample_gnews_response = {
            "totalArticles": 2,
            "articles": [
                {
                    "title": "GNews Test Article 1",
                    "description": "Description of GNews test article 1",
                    "content": "Content of GNews test article 1",
                    "url": "https://example.com/gnews1",
                    "image": "https://example.com/gnews_image1.jpg",
                    "publishedAt": "2023-01-01T13:00:00Z",
                    "source": {
                        "name": "GNews Source 1",
                        "url": "https://example.com/gnewssource1"
                    }
                },
                {
                    "title": "GNews Test Article 2",
                    "description": "Description of GNews test article 2",
                    "content": "Content of GNews test article 2",
                    "url": "https://example.com/gnews2",
                    "image": "https://example.com/gnews_image2.jpg",
                    "publishedAt": "2023-01-02T13:00:00Z",
                    "source": {
                        "name": "GNews Source 2",
                        "url": "https://example.com/gnewssource2"
                    }
                }
            ]
        }
        
        # Test stock symbol
        self.test_stock = "AAPL"
    
    def tearDown(self):
        """Clean up test fixtures after tests."""
        # Remove test files and directory
        for file in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, file))
        os.rmdir(self.test_dir)
    
    def test_store_raw_responses(self):
        """Test storing raw API responses."""
        # Call the function to store raw responses
        filepath = store_raw_responses(
            self.test_stock,
            self.sample_newsapi_response,
            self.sample_gnews_response,
            self.test_dir
        )
        
        # Check if the file was created
        self.assertTrue(os.path.exists(filepath))
        
        # Load the file and verify its content
        with open(filepath, 'r') as f:
            saved_data = json.load(f)
        
        # Check that the structure is correct
        self.assertIn('newsapi', saved_data)
        self.assertIn('gnews', saved_data)
        
        # Check that the data is correctly stored
        self.assertEqual(saved_data['newsapi'], self.sample_newsapi_response)
        self.assertEqual(saved_data['gnews'], self.sample_gnews_response)
    
    def test_load_raw_responses(self):
        """Test loading raw API responses."""
        # First store the data
        filepath = store_raw_responses(
            self.test_stock,
            self.sample_newsapi_response,
            self.sample_gnews_response,
            self.test_dir
        )
        
        # Now load it
        loaded_data = load_raw_responses(self.test_stock, self.test_dir)
        
        # Verify that loaded data matches the original data
        self.assertEqual(loaded_data['newsapi'], self.sample_newsapi_response)
        self.assertEqual(loaded_data['gnews'], self.sample_gnews_response)
    
    def test_load_nonexistent_file(self):
        """Test loading from a file that doesn't exist."""
        # Try to load data for a stock that hasn't been saved
        with self.assertRaises(FileNotFoundError):
            load_raw_responses("NONEXISTENT", self.test_dir)
    
    @patch('os.path.exists')
    def test_store_raw_responses_directory_creation(self, mock_exists):
        """Test that the directory is created if it doesn't exist."""
        # Setup the mock to return False, indicating directory doesn't exist
        mock_exists.return_value = False
        
        # Mock os.makedirs to avoid actually creating directories
        with patch('os.makedirs') as mock_makedirs:
            # Call the function
            store_raw_responses(
                self.test_stock,
                self.sample_newsapi_response,
                self.sample_gnews_response,
                self.test_dir
            )
            
            # Verify that makedirs was called with the test directory
            mock_makedirs.assert_called_once_with(self.test_dir, exist_ok=True)
    
    def test_store_and_load_with_none_values(self):
        """Test storing and loading with None values for some responses."""
        # Store with None for gnews
        filepath = store_raw_responses(
            self.test_stock,
            self.sample_newsapi_response,
            None,
            self.test_dir
        )
        
        # Load and verify
        loaded_data = load_raw_responses(self.test_stock, self.test_dir)
        self.assertEqual(loaded_data['newsapi'], self.sample_newsapi_response)
        self.assertEqual(loaded_data['gnews'], {})
        
        # Store with None for newsapi
        filepath = store_raw_responses(
            self.test_stock,
            None,
            self.sample_gnews_response,
            self.test_dir
        )
        
        # Load and verify
        loaded_data = load_raw_responses(self.test_stock, self.test_dir)
        self.assertEqual(loaded_data['newsapi'], {})
        self.assertEqual(loaded_data['gnews'], self.sample_gnews_response)


if __name__ == '__main__':
    unittest.main()