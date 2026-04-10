import requests
import json
import os
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
import time
import re

class InternetMedicineService:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def search_medicine_online(self, medicine_name: str) -> Dict:
        """
        Search for medicine information from online sources
        Returns structured data similar to dataset format
        """
        try:
            # Try multiple sources
            results = []
            
            # Source 1: Basic web search results
            search_result = self._web_search(medicine_name)
            if search_result:
                results.append(search_result)
            
            # Source 2: Pharma websites (if accessible)
            pharma_result = self._search_pharma_sites(medicine_name)
            if pharma_result:
                results.append(pharma_result)
            
            # Source 3: Generic medicine database search
            generic_result = self._search_generic_db(medicine_name)
            if generic_result:
                results.append(generic_result)
            
            # Combine and return best result
            if results:
                return self._combine_results(results, medicine_name)
            else:
                return {"error": "No information found online"}
                
        except Exception as e:
            return {"error": f"Internet search failed: {str(e)}"}
    
    def _web_search(self, medicine_name: str) -> Optional[Dict]:
        """Perform web search for medicine information"""
        try:
            # Use DuckDuckGo for search (no API key needed)
            search_url = f"https://duckduckgo.com/html/?q={medicine_name}+medicine+price+India"
            response = self.session.get(search_url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                results = soup.find_all('div', class_='result')
                
                if results:
                    first_result = results[0]
                    title = first_result.find('a', class_='result__a')
                    snippet = first_result.find('a', class_='result__snippet')
                    
                    if title:
                        return {
                            "source": "web_search",
                            "title": title.get_text().strip(),
                            "snippet": snippet.get_text().strip() if snippet else "",
                            "url": title.get('href', ''),
                            "medicine_name": medicine_name
                        }
        except:
            pass
        return None
    
    def _search_pharma_sites(self, medicine_name: str) -> Optional[Dict]:
        """Search known pharmaceutical websites"""
        pharma_sites = [
            "https://www.1mg.com",
            "https://www.netmeds.com", 
            "https://www.pharmeasy.in"
        ]
        
        for site in pharma_sites:
            try:
                search_query = f"{medicine_name} site:{site}"
                search_url = f"https://duckduckgo.com/html/?q={search_query}"
                response = self.session.get(search_url, timeout=8)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    results = soup.find_all('div', class_='result')
                    
                    if results:
                        first_result = results[0]
                        title_elem = first_result.find('a', class_='result__a')
                        snippet_elem = first_result.find('a', class_='result__snippet')
                        
                        if title_elem and medicine_name.lower() in title_elem.get_text().lower():
                            return {
                                "source": "pharma_site",
                                "site": site,
                                "title": title_elem.get_text().strip(),
                                "snippet": snippet_elem.get_text().strip() if snippet_elem else "",
                                "url": title_elem.get('href', ''),
                                "medicine_name": medicine_name
                            }
            except:
                continue
        return None
    
    def _search_generic_db(self, medicine_name: str) -> Optional[Dict]:
        """Search generic medicine databases"""
        try:
            # Try to extract salt/composition from medicine name
            salts = self._extract_possible_salts(medicine_name)
            
            for salt in salts:
                search_url = f"https://duckduckgo.com/html/?q={salt}+generic+medicine+composition"
                response = self.session.get(search_url, timeout=8)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    results = soup.find_all('div', class_='result')
                    
                    if results:
                        first_result = results[0]
                        title_elem = first_result.find('a', class_='result__a')
                        snippet_elem = first_result.find('a', class_='result__snippet')
                        
                        if title_elem:
                            return {
                                "source": "generic_db",
                                "salt": salt,
                                "title": title_elem.get_text().strip(),
                                "snippet": snippet_elem.get_text().strip() if snippet_elem else "",
                                "url": title_elem.get('href', ''),
                                "medicine_name": medicine_name
                            }
        except:
            pass
        return None
    
    def _extract_possible_salts(self, medicine_name: str) -> List[str]:
        """Extract possible salt compositions from medicine name"""
        # Common salt patterns in Indian medicines
        common_salts = [
            "paracetamol", "acetaminophen", "ibuprofen", "aspirin", "amoxicillin",
            "azithromycin", "ciprofloxacin", "ofloxacin", "levofloxacin",
            "metformin", "glimepiride", "atorvastatin", "rosuvastatin",
            "omeprazole", "pantoprazole", "ranitidine", "ondansetron",
            "domperidone", "levocetirizine", "montelukast", "salbutamol"
        ]
        
        medicine_lower = medicine_name.lower()
        found_salts = []
        
        for salt in common_salts:
            if salt in medicine_lower:
                found_salts.append(salt)
        
        # If no salts found, return the medicine name as potential salt
        if not found_salts:
            found_salts.append(medicine_name)
        
        return found_salts[:3]  # Return max 3 salts
    
    def _combine_results(self, results: List[Dict], medicine_name: str) -> Dict:
        """Combine multiple search results into structured format"""
        if not results:
            return {"error": "No results found"}
        
        # Use the first/best result as primary
        primary_result = results[0]
        
        # Create structured response similar to dataset format
        structured_response = {
            "medicine": medicine_name,
            "price": self._extract_price(primary_result),
            "therapeutic_class": self._extract_therapeutic_class(primary_result),
            "manufacturer": self._extract_manufacturer(primary_result),
            "source": primary_result.get("source", "internet"),
            "alternatives": self._generate_alternatives(results, medicine_name),
            "note": f"Data fetched from {primary_result.get('source', 'internet')} sources",
            "raw_data": primary_result
        }
        
        return structured_response
    
    def _extract_price(self, result: Dict) -> float:
        """Extract price from search result"""
        snippet = result.get("snippet", "").lower()
        
        # Look for price patterns
        price_patterns = [
            r'rs\.?\s*(\d+)',
            r'(\d+)\s*rs',
            r'rupees?\s*(\d+)',
            r'(\d+)\s*rupees?',
            r'(\d+)\s*inr',
            r'inr\s*(\d+)'
        ]
        
        for pattern in price_patterns:
            match = re.search(pattern, snippet)
            if match:
                try:
                    return float(match.group(1))
                except:
                    continue
        
        # Default estimated price if not found
        return 150.0  # Reasonable estimate for generic medicines
    
    def _extract_therapeutic_class(self, result: Dict) -> Optional[str]:
        """Extract therapeutic class from search result"""
        snippet = result.get("snippet", "").lower()
        title = result.get("title", "").lower()
        text = f"{title} {snippet}"
        
        # Common therapeutic classes
        classes = [
            "antibiotic", "antibacterial", "antiviral", "antifungal",
            "analgesic", "antipyretic", "anti-inflammatory",
            "antihistamine", "antiallergic",
            "antidiabetic", "antihypertensive", "cardiovascular",
            "gastrointestinal", "antiulcer",
            "respiratory", "bronchodilator"
        ]
        
        for cls in classes:
            if cls in text:
                return cls.title()
        
        return "General Medicine"
    
    def _extract_manufacturer(self, result: Dict) -> Optional[str]:
        """Extract manufacturer from search result"""
        snippet = result.get("snippet", "")
        title = result.get("title", "")
        text = f"{title} {snippet}"
        
        # Common pharmaceutical companies
        companies = [
            "cipla", "sun pharma", "dr. reddy's", "lupin", "abbott",
            "gsk", "pfizer", "novartis", "johnson & johnson",
            "bayer", "torrent", "mankind", "zydus", "ajanta"
        ]
        
        for company in companies:
            if company.lower() in text.lower():
                return company.title()
        
        return "Unknown"
    
    def _generate_alternatives(self, results: List[Dict], medicine_name: str) -> List[Dict]:
        """Generate alternative medicines from search results"""
        alternatives = []
        
        # Use additional results as alternatives
        for i, result in enumerate(results[1:4], 1):  # Max 3 alternatives
            alt = {
                "brand_name": f"Alternative {i}",
                "price": self._extract_price(result),
                "manufacturer": self._extract_manufacturer(result),
                "savings_percent": round((150.0 - self._extract_price(result)) / 150.0 * 100, 1),
                "source": result.get("source", "internet")
            }
            alternatives.append(alt)
        
        return alternatives

# Global instance
internet_service = InternetMedicineService()

def get_medicine_from_internet(medicine_name: str) -> Dict:
    """Main function to get medicine data from internet"""
    return internet_service.search_medicine_online(medicine_name)
