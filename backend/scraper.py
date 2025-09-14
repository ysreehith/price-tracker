import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PriceScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def get_domain(self, url):
        """Extract domain from URL"""
        parsed_url = urlparse(url)
        return parsed_url.netloc.lower()
    
    def clean_price(self, price_text):
        """Clean and extract numeric price from text"""
        if not price_text:
            return None
        
        # Remove currency symbols and extract numbers
        price_clean = re.sub(r'[^\d.,]', '', str(price_text))
        price_clean = price_clean.replace(',', '')
        
        try:
            return float(price_clean)
        except ValueError:
            return None
    
    def scrape_amazon(self, url):
        """Scrape Amazon product page"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Product name
            name_selectors = [
                '#productTitle',
                'h1.a-size-large',
                '.product-title',
                'h1[data-automation-id="product-title"]'
            ]
            
            name = None
            for selector in name_selectors:
                element = soup.select_one(selector)
                if element:
                    name = element.get_text(strip=True)
                    break
            
            # Price
            price_selectors = [
                '.a-price-whole',
                '.a-offscreen',
                '#priceblock_dealprice',
                '#priceblock_ourprice',
                '.a-price-range',
                '[data-automation-id="product-price"]'
            ]
            
            price = None
            for selector in price_selectors:
                element = soup.select_one(selector)
                if element:
                    price_text = element.get_text(strip=True)
                    price = self.clean_price(price_text)
                    if price:
                        break
            
            return {
                'name': name,
                'price': price,
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Error scraping Amazon: {e}")
            return {'name': None, 'price': None, 'success': False, 'error': str(e)}
    
    def scrape_ebay(self, url):
        """Scrape eBay product page"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Product name
            name_selectors = [
                '#x-title-label-lbl',
                '.x-title-label',
                'h1[data-testid="x-title-label"]',
                '.u-flL.condText'
            ]
            
            name = None
            for selector in name_selectors:
                element = soup.select_one(selector)
                if element:
                    name = element.get_text(strip=True)
                    break
            
            # Price
            price_selectors = [
                '.notranslate',
                '#prcIsum',
                '.u-flL.condText',
                '[data-testid="x-price-primary"]'
            ]
            
            price = None
            for selector in price_selectors:
                element = soup.select_one(selector)
                if element:
                    price_text = element.get_text(strip=True)
                    price = self.clean_price(price_text)
                    if price:
                        break
            
            return {
                'name': name,
                'price': price,
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Error scraping eBay: {e}")
            return {'name': None, 'price': None, 'success': False, 'error': str(e)}
    
    def scrape_walmart(self, url):
        """Scrape Walmart product page"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Product name
            name_selectors = [
                '[data-automation-id="product-title"]',
                'h1.prod-ProductTitle',
                '.prod-ProductTitle',
                'h1[data-testid="product-title"]'
            ]
            
            name = None
            for selector in name_selectors:
                element = soup.select_one(selector)
                if element:
                    name = element.get_text(strip=True)
                    break
            
            # Price
            price_selectors = [
                '[data-automation-id="product-price"]',
                '.price-current',
                '.price-group',
                '[data-testid="price-current"]'
            ]
            
            price = None
            for selector in price_selectors:
                element = soup.select_one(selector)
                if element:
                    price_text = element.get_text(strip=True)
                    price = self.clean_price(price_text)
                    if price:
                        break
            
            return {
                'name': name,
                'price': price,
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Error scraping Walmart: {e}")
            return {'name': None, 'price': None, 'success': False, 'error': str(e)}
    
    def scrape_with_selenium(self, url):
        """Fallback scraping method using Selenium for dynamic content"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(url)
            
            # Wait for page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Try to find product name and price
            name = None
            price = None
            
            # Common selectors for product name
            name_selectors = [
                "h1", "[data-testid*='title']", ".product-title", "#productTitle"
            ]
            
            for selector in name_selectors:
                try:
                    element = driver.find_element(By.CSS_SELECTOR, selector)
                    if element and element.text.strip():
                        name = element.text.strip()
                        break
                except:
                    continue
            
            # Common selectors for price
            price_selectors = [
                "[data-testid*='price']", ".price", "[class*='price']", ".cost"
            ]
            
            for selector in price_selectors:
                try:
                    element = driver.find_element(By.CSS_SELECTOR, selector)
                    if element and element.text.strip():
                        price_text = element.text.strip()
                        price = self.clean_price(price_text)
                        if price:
                            break
                except:
                    continue
            
            driver.quit()
            
            return {
                'name': name,
                'price': price,
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Error with Selenium scraping: {e}")
            return {'name': None, 'price': None, 'success': False, 'error': str(e)}
    
    def scrape_product(self, url):
        """Main method to scrape product information"""
        domain = self.get_domain(url)
        
        # Try specific scraper first
        if 'amazon' in domain:
            result = self.scrape_amazon(url)
        elif 'ebay' in domain:
            result = self.scrape_ebay(url)
        elif 'walmart' in domain:
            result = self.scrape_walmart(url)
        else:
            # Generic scraping attempt
            result = self.scrape_with_selenium(url)
        
        # If specific scraper failed, try Selenium as fallback
        if not result['success'] or not result['name'] or not result['price']:
            logger.info("Trying Selenium fallback...")
            selenium_result = self.scrape_with_selenium(url)
            if selenium_result['success'] and selenium_result['name'] and selenium_result['price']:
                result = selenium_result
        
        return result

