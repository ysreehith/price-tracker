# Price Tracker

A full-stack web application for tracking product prices from Amazon, eBay, and Walmart. Built with FastAPI (Python) backend and React (TypeScript) frontend.

## Features

- **Product Tracking**: Add products by URL from Amazon, eBay, and Walmart
- **Price Monitoring**: Automatic price scraping and storage
- **Price History**: Visual charts showing price changes over time
- **Real-time Updates**: Manual price refresh functionality
- **Responsive UI**: Modern, mobile-friendly interface with Tailwind CSS

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: Database ORM
- **SQLite**: Database (easily upgradeable to PostgreSQL)
- **BeautifulSoup + Selenium**: Web scraping
- **Pydantic**: Data validation

### Frontend
- **React 18**: UI library with TypeScript
- **Tailwind CSS**: Utility-first CSS framework
- **Chart.js**: Price history visualization
- **Axios**: HTTP client for API calls

## Project Structure

```
price-tracker/
├── backend/
│   ├── main.py          # FastAPI application
│   ├── database.py      # Database models and setup
│   ├── scraper.py       # Web scraping logic
│   └── models.py        # Pydantic models
├── frontend/
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── api.ts       # API client
│   │   ├── types.ts     # TypeScript types
│   │   └── App.tsx      # Main app component
│   └── package.json
└── requirements.txt
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- Chrome browser (for Selenium)

### Backend Setup

1. Navigate to the project directory:
   ```bash
   cd price-tracker
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the FastAPI server:
   ```bash
   cd backend
   python main.py
   ```

   The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the React development server:
   ```bash
   npm start
   ```

   The app will be available at `http://localhost:3000`

## Usage

1. **Add a Product**: Paste a product URL from Amazon, eBay, or Walmart into the form
2. **View Products**: See all tracked products in the table with current prices
3. **Update Prices**: Click "Update" to refresh the current price
4. **View Price History**: Click "View Chart" to see price trends over time
5. **Delete Products**: Remove products you no longer want to track

## API Endpoints

- `GET /` - API health check
- `POST /products/` - Add a new product
- `GET /products/` - Get all products
- `GET /products/{id}` - Get product with price history
- `POST /products/{id}/update` - Update product price
- `DELETE /products/{id}` - Delete product
- `GET /products/{id}/price-history` - Get price history

## Web Scraping

The application uses a multi-layered scraping approach:

1. **Primary**: BeautifulSoup for static content
2. **Fallback**: Selenium for dynamic content
3. **Site-specific**: Optimized selectors for Amazon, eBay, and Walmart

## Database Schema

- **Products**: Store product information and current price
- **Price History**: Track price changes over time

## Development

### Adding New E-commerce Sites

1. Add site-specific scraping logic in `scraper.py`
2. Update the `get_domain()` method to recognize new domains
3. Test with sample URLs

### Customizing the UI

The frontend uses Tailwind CSS for styling. Modify `tailwind.config.js` to customize the design system.

## Troubleshooting

### Common Issues

1. **Scraping fails**: Some sites may block requests. The app will try Selenium as fallback.
2. **Chrome driver issues**: Ensure Chrome is installed and up to date.
3. **CORS errors**: Make sure the backend is running on port 8000.

### Logs

Check the console for detailed error messages and scraping logs.

## Future Enhancements

- Email notifications for price drops
- Price alerts and thresholds
- Support for more e-commerce sites
- User authentication and personal product lists
- Automated price updates with cron jobs
- Export price data to CSV/Excel

## License

MIT License - feel free to use this project for learning and personal use.

