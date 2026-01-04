"""
Distributor Product Recommendation Engine

This module provides product recommendations from various distributors
based on door specifications. New distributors can be added by creating
a new class that inherits from BaseDistributor.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class ProductRecommendation:
    """Represents a product recommendation from a distributor."""
    
    def __init__(
        self,
        name: str,
        category: str,
        description: str,
        url: str,
        image_url: Optional[str] = None,
        model_numbers: Optional[List[str]] = None,
        features: Optional[List[str]] = None,
        specs_match: Optional[Dict[str, Any]] = None,
        price_range: Optional[str] = None,
        distributor: str = ""
    ):
        self.name = name
        self.category = category
        self.description = description
        self.url = url
        self.image_url = image_url
        self.model_numbers = model_numbers or []
        self.features = features or []
        self.specs_match = specs_match or {}
        self.price_range = price_range
        self.distributor = distributor
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "url": self.url,
            "image_url": self.image_url,
            "model_numbers": self.model_numbers,
            "features": self.features,
            "specs_match": self.specs_match,
            "price_range": self.price_range,
            "distributor": self.distributor
        }


class BaseDistributor(ABC):
    """Base class for all distributors. Extend this to add new distributors."""
    
    name: str = "Base Distributor"
    website: str = ""
    logo_url: str = ""
    
    @abstractmethod
    def get_recommendations(self, specs: Dict[str, Any]) -> List[ProductRecommendation]:
        """
        Return product recommendations based on door specifications.
        
        Args:
            specs: Dictionary containing door specifications like:
                - width, height, thickness
                - doorType, material
                - hardware list
                - fireRating
                - hasGlass, glassType
                etc.
        
        Returns:
            List of ProductRecommendation objects
        """
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "website": self.website,
            "logo_url": self.logo_url
        }


class DormakabaDistributor(BaseDistributor):
    """Dormakaba product recommendations for commercial door hardware."""
    
    name = "Dormakaba"
    website = "https://www.dormakaba.com/us-en"
    logo_url = "https://www.dormakaba.com/resource/image/27440/landscape_ratio16x9/1920/1080/bb5bad74bf8ad14ec6969bb6c6a0d6c/uD/dormakaba-logo-sharing.jpg"
    
    # Product catalog with matching criteria
    PRODUCTS = {
        "door_closers": {
            "surface_mounted": [
                {
                    "name": "8600 Series Surface Door Closer",
                    "description": "Heavy-duty surface mounted closer for high-traffic commercial applications. Features adjustable closing and latching speeds.",
                    "url": "https://www.dormakaba.com/us-en/offering/products/door-hardware/door-closers",
                    "model_numbers": ["8616", "8626", "8646"],
                    "features": ["Adjustable backcheck", "Delayed action option", "Hold-open arm available"],
                    "door_types": ["commercial", "exterior-entry"],
                    "fire_rated": True,
                    "max_door_width": 48,
                    "price_range": "$150-300"
                },
                {
                    "name": "7400 Series Surface Door Closer",
                    "description": "Standard duty surface closer ideal for interior and light commercial doors.",
                    "url": "https://www.dormakaba.com/us-en/offering/products/door-hardware/door-closers",
                    "model_numbers": ["7416", "7426"],
                    "features": ["Tri-pack installation", "Adjustable spring power"],
                    "door_types": ["interior", "commercial"],
                    "fire_rated": True,
                    "max_door_width": 42,
                    "price_range": "$100-200"
                }
            ],
            "concealed": [
                {
                    "name": "RTS88 Concealed Overhead Closer",
                    "description": "Concealed in-frame closer for a clean architectural appearance. Ideal for aluminum and glass doors.",
                    "url": "https://www.dormakaba.com/us-en/offering/products/door-hardware/door-closers",
                    "model_numbers": ["RTS88"],
                    "features": ["Concealed installation", "Adjustable backcheck", "Hold-open function"],
                    "door_types": ["commercial", "exterior-entry", "interior"],
                    "fire_rated": True,
                    "max_door_width": 48,
                    "price_range": "$300-500"
                }
            ]
        },
        "mechanical_locks": {
            "mortise": [
                {
                    "name": "8200 Series Mortise Lock",
                    "description": "Heavy-duty mortise lock for commercial applications. Multiple function options available.",
                    "url": "https://www.dormakaba.com/us-en/offering/products/door-hardware/mechanical-door-locks",
                    "model_numbers": ["8215", "8217", "8225", "8243"],
                    "features": ["Grade 1 certified", "Fire rated", "Multiple lever styles"],
                    "door_types": ["commercial", "exterior-entry"],
                    "thickness_min": "1-3/4",
                    "fire_rated": True,
                    "price_range": "$300-600"
                }
            ],
            "cylindrical": [
                {
                    "name": "W Series Cylindrical Lock",
                    "description": "Heavy-duty cylindrical lock for commercial and institutional applications.",
                    "url": "https://www.dormakaba.com/us-en/offering/products/door-hardware/mechanical-door-locks",
                    "model_numbers": ["W101", "W301", "W501"],
                    "features": ["Grade 1 certified", "Large variety of lever designs", "IC core compatible"],
                    "door_types": ["commercial", "interior"],
                    "thickness_min": "1-3/8",
                    "fire_rated": True,
                    "price_range": "$150-350"
                },
                {
                    "name": "QCL Series Cylindrical Lock",
                    "description": "QuickConnect technology for easy installation. Ideal for educational and healthcare facilities.",
                    "url": "https://www.dormakaba.com/us-en/offering/products/door-hardware/mechanical-door-locks",
                    "model_numbers": ["QCL150", "QCL170", "QCL230"],
                    "features": ["Tool-free installation", "Grade 2 certified", "Classroom function available"],
                    "door_types": ["interior", "commercial"],
                    "thickness_min": "1-3/8",
                    "fire_rated": True,
                    "price_range": "$100-250"
                }
            ],
            "deadbolt": [
                {
                    "name": "DB Series Deadbolt",
                    "description": "Heavy-duty deadbolt for maximum security. Available in single and double cylinder options.",
                    "url": "https://www.dormakaba.com/us-en/offering/products/door-hardware/mechanical-door-locks",
                    "model_numbers": ["DB1000", "DB2000"],
                    "features": ["Grade 1 certified", "1\" throw bolt", "IC core compatible"],
                    "door_types": ["exterior-entry", "commercial"],
                    "fire_rated": False,
                    "price_range": "$80-200"
                }
            ]
        },
        "exit_devices": {
            "rim": [
                {
                    "name": "9000 Series Rim Exit Device",
                    "description": "Heavy-duty rim exit device for high-traffic emergency egress. Touch bar or cross bar options.",
                    "url": "https://www.dormakaba.com/us-en/offering/products/door-hardware/door-hardware-exit-devices",
                    "model_numbers": ["9100", "9200", "9300"],
                    "features": ["Grade 1 certified", "Fire rated up to 3 hours", "Dogging function"],
                    "door_types": ["commercial", "exterior-entry"],
                    "fire_rated": True,
                    "min_door_width": 30,
                    "max_door_width": 48,
                    "price_range": "$400-800"
                }
            ],
            "narrow_stile": [
                {
                    "name": "9000NS Narrow Stile Exit Device",
                    "description": "Designed for aluminum and glass storefront doors with narrow stile profiles.",
                    "url": "https://www.dormakaba.com/us-en/offering/products/door-hardware/door-hardware-exit-devices",
                    "model_numbers": ["9100NS", "9200NS"],
                    "features": ["Fits 1-3/4\" to 2\" stiles", "Touch bar operation", "Field reversible"],
                    "door_types": ["commercial"],
                    "has_glass": True,
                    "price_range": "$500-900"
                }
            ]
        },
        "low_energy_operators": [
            {
                "name": "ED900 Low Energy Swing Door Operator",
                "description": "Electromechanical operator for ADA-compliant automatic door opening. Push-and-go activation.",
                "url": "https://www.dormakaba.com/us-en/offering/products/door-hardware/low-energy-swing-door-operators",
                "model_numbers": ["ED900", "ED910", "ED920"],
                "features": ["ADA compliant", "Push-and-go", "Obstacle detection", "Battery backup option"],
                "door_types": ["commercial", "exterior-entry", "interior"],
                "fire_rated": True,
                "max_door_width": 48,
                "price_range": "$1,500-3,000"
            },
            {
                "name": "ED700 Electrified Door Operator",
                "description": "Full-featured automatic operator for high-traffic entrances and ADA accessibility.",
                "url": "https://www.dormakaba.com/us-en/offering/products/door-hardware/low-energy-swing-door-operators",
                "model_numbers": ["ED700"],
                "features": ["Touchless activation", "Integration with access control", "Hold-open function"],
                "door_types": ["commercial", "exterior-entry"],
                "price_range": "$2,000-4,000"
            }
        ],
        "fire_life_safety": [
            {
                "name": "Electromagnetic Door Holder",
                "description": "Holds fire doors open and releases on fire alarm signal. Wall or floor mounted options.",
                "url": "https://www.dormakaba.com/us-en/offering/products/door-hardware/firelife-safety-devices",
                "model_numbers": ["EM200", "EM500"],
                "features": ["24V DC operation", "Manual release", "Floor or wall mount"],
                "door_types": ["commercial", "interior"],
                "fire_rated": True,
                "price_range": "$100-300"
            },
            {
                "name": "Closer/Holder Combination",
                "description": "Combined door closer with electromagnetic hold-open function. Releases on fire alarm.",
                "url": "https://www.dormakaba.com/us-en/offering/products/door-hardware/firelife-safety-devices",
                "model_numbers": ["8916", "8926"],
                "features": ["Integrated closer and holder", "Smoke detector compatible", "Fire rated"],
                "door_types": ["commercial"],
                "fire_rated": True,
                "price_range": "$400-700"
            }
        ],
        "simplex_locks": [
            {
                "name": "Simplex 5000 Series Pushbutton Lock",
                "description": "Mechanical pushbutton lock requiring no power or batteries. Keyless convenience.",
                "url": "https://www.dormakaba.com/us-en/offering/products/door-hardware/simplex-mechanical-pushbutton-locks",
                "model_numbers": ["5021", "5041", "5051"],
                "features": ["No batteries required", "Up to 1,000 combinations", "Key override option"],
                "door_types": ["interior", "commercial"],
                "price_range": "$300-600"
            },
            {
                "name": "Simplex L1000 Series",
                "description": "Light-duty mechanical pushbutton lock for interior doors with privacy function.",
                "url": "https://www.dormakaba.com/us-en/offering/products/door-hardware/simplex-mechanical-pushbutton-locks",
                "model_numbers": ["L1011", "L1021", "L1031"],
                "features": ["Compact design", "Passage function", "Easy code change"],
                "door_types": ["interior"],
                "price_range": "$200-400"
            }
        ],
        "electronic_access": [
            {
                "name": "Kaba E-Plex 5x00 Series",
                "description": "Electronic pushbutton lock with audit trail capability. Ideal for access control applications.",
                "url": "https://www.dormakaba.com/us-en/offering/products/electronic-access-data",
                "model_numbers": ["E5031", "E5051", "E5071"],
                "features": ["100 user codes", "Audit trail", "Time zone scheduling", "Key override"],
                "door_types": ["interior", "commercial"],
                "price_range": "$500-900"
            },
            {
                "name": "Kaba X-10 Standalone Electronic Lock",
                "description": "Multi-technology reader with keypad. Supports cards, fobs, and PIN codes.",
                "url": "https://www.dormakaba.com/us-en/offering/products/electronic-access-data",
                "model_numbers": ["X-10"],
                "features": ["Multi-credential support", "Weatherproof option", "Audit trail"],
                "door_types": ["exterior-entry", "commercial"],
                "price_range": "$800-1,200"
            }
        ]
    }
    
    def get_recommendations(self, specs: Dict[str, Any]) -> List[ProductRecommendation]:
        recommendations = []
        
        door_type = specs.get('doorType', 'interior')
        hardware_list = [h.lower() for h in specs.get('hardware', [])]
        fire_rating = specs.get('fireRating', 'none')
        has_glass = specs.get('hasGlass', False)
        width = specs.get('width', 36)
        thickness = specs.get('thickness', '1-3/4')
        prep_type = specs.get('prepType', 'single-bore')
        
        is_fire_rated = fire_rating != 'none'
        is_commercial = door_type in ['commercial', 'exterior-entry']
        
        # Door Closers - recommend based on door type
        if 'doorcloser' in hardware_list or is_commercial:
            closers = self.PRODUCTS['door_closers']
            if is_commercial:
                for closer in closers['surface_mounted']:
                    if width <= closer.get('max_door_width', 48):
                        recommendations.append(self._create_recommendation(closer, "Door Closers"))
            recommendations.append(self._create_recommendation(closers['concealed'][0], "Door Closers"))
        
        # Mechanical Locks
        if 'lockset' in hardware_list or 'handle' in hardware_list:
            locks = self.PRODUCTS['mechanical_locks']
            
            if prep_type == 'mortise' or is_commercial:
                for lock in locks['mortise']:
                    recommendations.append(self._create_recommendation(lock, "Mechanical Locks"))
            
            for lock in locks['cylindrical']:
                recommendations.append(self._create_recommendation(lock, "Mechanical Locks"))
        
        # Deadbolts
        if 'deadbolt' in hardware_list:
            for deadbolt in self.PRODUCTS['mechanical_locks']['deadbolt']:
                recommendations.append(self._create_recommendation(deadbolt, "Mechanical Locks"))
        
        # Exit Devices - for commercial/egress applications
        if door_type == 'commercial' or (door_type == 'exterior-entry' and width >= 30):
            exits = self.PRODUCTS['exit_devices']
            if has_glass:
                for device in exits['narrow_stile']:
                    recommendations.append(self._create_recommendation(device, "Exit Devices"))
            else:
                for device in exits['rim']:
                    if width >= device.get('min_door_width', 30) and width <= device.get('max_door_width', 48):
                        recommendations.append(self._create_recommendation(device, "Exit Devices"))
        
        # Low Energy Operators - for accessibility/commercial
        if door_type in ['commercial', 'exterior-entry']:
            for operator in self.PRODUCTS['low_energy_operators']:
                recommendations.append(self._create_recommendation(operator, "Door Operators"))
        
        # Fire/Life Safety
        if is_fire_rated:
            for device in self.PRODUCTS['fire_life_safety']:
                recommendations.append(self._create_recommendation(device, "Fire/Life Safety"))
        
        # Simplex/Electronic Locks - for keyless entry needs
        if door_type in ['commercial', 'interior']:
            for lock in self.PRODUCTS['simplex_locks'][:1]:  # Limit to 1
                recommendations.append(self._create_recommendation(lock, "Keyless Entry"))
            for lock in self.PRODUCTS['electronic_access'][:1]:  # Limit to 1
                recommendations.append(self._create_recommendation(lock, "Electronic Access"))
        
        return recommendations
    
    def _create_recommendation(self, product: Dict, category: str) -> ProductRecommendation:
        return ProductRecommendation(
            name=product['name'],
            category=category,
            description=product['description'],
            url=product['url'],
            model_numbers=product.get('model_numbers', []),
            features=product.get('features', []),
            price_range=product.get('price_range'),
            distributor=self.name
        )


class SecLockDistributor(BaseDistributor):
    """
    SecLock - Premier Commercial Door Hardware Distributor
    https://www.seclock.com/
    
    SecLock is a wholesale-only commercial door hardware distributor
    providing same-day access to all major product brands.
    """
    
    name = "SecLock"
    website = "https://www.seclock.com"
    logo_url = "https://www.seclock.com/logo.png"
    phone = "800-847-5625"
    
    # Comprehensive product catalog from multiple manufacturers
    PRODUCTS = {
        # Door Closers
        "door_closers": {
            "lcn": [
                {
                    "name": "LCN 4040XP Series Heavy Duty Door Closer",
                    "description": "Extra heavy-duty cast iron door closer with adjustable backcheck, sweep speed, and latch speed. Ideal for high-traffic openings.",
                    "url": "https://www.seclock.com/catalog/price-books/lcn",
                    "model_numbers": ["4040XP", "4040XP-RW/PA", "4040XP-CUSH", "4040XP-EDA"],
                    "features": ["Cast iron construction", "Adjustable closing speeds", "Optional hold-open arm", "ADA compliant options"],
                    "price_range": "$280-$550",
                    "manufacturer": "LCN"
                },
                {
                    "name": "LCN 1461 Series Surface Mounted Closer",
                    "description": "Standard duty surface mounted door closer for interior openings. Smooth, quiet operation with full rack-and-pinion design.",
                    "url": "https://www.seclock.com/catalog/price-books/lcn",
                    "model_numbers": ["1461", "1461T", "1461-H"],
                    "features": ["Aluminum body", "Adjustable spring power", "Delayed action available", "Non-handed"],
                    "price_range": "$150-$280",
                    "manufacturer": "LCN"
                }
            ],
            "norton": [
                {
                    "name": "Norton 7500 Series Door Closer",
                    "description": "Architectural grade surface door closer with precision-machined components for reliable, long-lasting performance.",
                    "url": "https://www.seclock.com/catalog/price-books/norton",
                    "model_numbers": ["7500", "7500H", "7500-689"],
                    "features": ["Tri-style mounting", "Full cover included", "Adjustable closing speeds", "10-year warranty"],
                    "price_range": "$200-$400",
                    "manufacturer": "Norton"
                }
            ],
            "sargent": [
                {
                    "name": "Sargent 1431 Series Surface Closer",
                    "description": "Versatile surface-mounted closer designed for high-frequency applications with durable construction.",
                    "url": "https://www.seclock.com/catalog/price-books/sargent",
                    "model_numbers": ["1431", "1431-CPS", "1431-H"],
                    "features": ["Multi-size spring", "Optional PowerGlide arm", "Hold-open available", "Barrier-free option"],
                    "price_range": "$175-$350",
                    "manufacturer": "Sargent"
                }
            ]
        },
        # Locks - Cylindrical & Mortise
        "locks": {
            "schlage": [
                {
                    "name": "Schlage ND Series Cylindrical Lock",
                    "description": "Heavy-duty cylindrical lever lock designed for high-traffic commercial applications. BHMA Grade 1 certified.",
                    "url": "https://www.seclock.com/catalog/price-books/schlage",
                    "model_numbers": ["ND50PD", "ND80PD", "ND53PD", "ND70PD"],
                    "features": ["Grade 1 certified", "2M cycle tested", "Vandal resistant", "UL listed for 3-hour fire doors"],
                    "price_range": "$180-$400",
                    "manufacturer": "Schlage"
                },
                {
                    "name": "Schlage L Series Mortise Lock",
                    "description": "Premier mortise lock with modular construction for maximum flexibility and security in institutional and commercial settings.",
                    "url": "https://www.seclock.com/catalog/price-books/schlage",
                    "model_numbers": ["L9453", "L9456", "L9480", "L9010"],
                    "features": ["BHMA Grade 1", "Modular design", "Field reversible", "Anti-friction latchbolt"],
                    "price_range": "$400-$800",
                    "manufacturer": "Schlage"
                },
                {
                    "name": "Schlage ALX Series Cylindrical Lock",
                    "description": "Commercial-grade cylindrical lock with improved security features and modern aesthetics for mid-range applications.",
                    "url": "https://www.seclock.com/catalog/price-books/schlage",
                    "model_numbers": ["ALX50P", "ALX70P", "ALX80P"],
                    "features": ["ANSI/BHMA Grade 2", "Snap-on rose design", "Easy rekeying", "Interchangeable core option"],
                    "price_range": "$120-$250",
                    "manufacturer": "Schlage"
                }
            ],
            "corbin_russwin": [
                {
                    "name": "Corbin Russwin CL3300 Series Cylindrical Lock",
                    "description": "Extra heavy-duty cylindrical lever lock designed for healthcare, education, and high-abuse environments.",
                    "url": "https://www.seclock.com/catalog/price-books/corbin",
                    "model_numbers": ["CL3351", "CL3357", "CL3355"],
                    "features": ["BHMA Grade 1", "Clutching lever", "Anti-microbial option", "6-pin solid brass cylinder"],
                    "price_range": "$250-$500",
                    "manufacturer": "Corbin Russwin"
                },
                {
                    "name": "Corbin Russwin ML2000 Series Mortise Lock",
                    "description": "High-security mortise lock with exceptional durability for demanding commercial and institutional applications.",
                    "url": "https://www.seclock.com/catalog/price-books/corbin",
                    "model_numbers": ["ML2010", "ML2051", "ML2055", "ML2067"],
                    "features": ["BHMA Grade 1", "Modular cylinder design", "Fire rated to 3 hours", "Electrified options"],
                    "price_range": "$450-$900",
                    "manufacturer": "Corbin Russwin"
                }
            ],
            "sargent": [
                {
                    "name": "Sargent 10 Line Cylindrical Lock",
                    "description": "Standard duty bored lock for commercial applications with reliable performance and variety of functions.",
                    "url": "https://www.seclock.com/catalog/price-books/sargent",
                    "model_numbers": ["10U15", "10U65", "10U94"],
                    "features": ["ANSI Grade 1", "6-pin cylinder", "ADA compliant levers", "UL fire rated"],
                    "price_range": "$200-$380",
                    "manufacturer": "Sargent"
                },
                {
                    "name": "Sargent 8200 Series Mortise Lock",
                    "description": "Heavy-duty mortise lock engineered for high-traffic commercial and institutional environments.",
                    "url": "https://www.seclock.com/catalog/price-books/sargent",
                    "model_numbers": ["8204", "8205", "8265", "8270"],
                    "features": ["BHMA Grade 1", "Sectional trim", "Anti-friction bolt", "Optional security rose"],
                    "price_range": "$400-$750",
                    "manufacturer": "Sargent"
                }
            ],
            "yale": [
                {
                    "name": "Yale 8800FL Series Mortise Lock",
                    "description": "Premium mortise lock with electromechanical options for access control integration.",
                    "url": "https://www.seclock.com/catalog/price-books/yale",
                    "model_numbers": ["8802FL", "8822FL", "8891FL"],
                    "features": ["BHMA Grade 1", "Fail-safe/fail-secure options", "Monitoring switches", "Request-to-exit"],
                    "price_range": "$500-$1200",
                    "manufacturer": "Yale"
                }
            ]
        },
        # Exit Devices
        "exit_devices": {
            "von_duprin": [
                {
                    "name": "Von Duprin 99 Series Exit Device",
                    "description": "Industry-leading rim exit device for heavy-duty commercial applications. Smooth, quiet operation with maximum security.",
                    "url": "https://www.seclock.com/catalog/price-books/vonduprin",
                    "model_numbers": ["99L", "99L-06", "99NL", "99EO"],
                    "features": ["Hex-key dogging", "LBR option", "UL listed", "Fire exit hardware"],
                    "price_range": "$450-$900",
                    "manufacturer": "Von Duprin"
                },
                {
                    "name": "Von Duprin 98/99 Series Vertical Rod",
                    "description": "Heavy-duty vertical rod exit device for double doors requiring top and bottom latching.",
                    "url": "https://www.seclock.com/catalog/price-books/vonduprin",
                    "model_numbers": ["9827", "9927", "9847", "9947"],
                    "features": ["Less bottom rod option", "Concealed vertical rod", "Fire rated", "Electric options"],
                    "price_range": "$800-$1500",
                    "manufacturer": "Von Duprin"
                }
            ],
            "falcon": [
                {
                    "name": "Falcon 24/25 Series Exit Device",
                    "description": "Heavy-duty wide stile exit device with smooth touchbar operation and durable construction.",
                    "url": "https://www.seclock.com/catalog/price-books/falcon",
                    "model_numbers": ["24-R-EO", "25-R-EO", "24-V-EO"],
                    "features": ["Non-handed", "UL listed", "Modular design", "Electric latch retraction"],
                    "price_range": "$380-$750",
                    "manufacturer": "Falcon"
                }
            ],
            "sargent": [
                {
                    "name": "Sargent 80 Series Exit Device",
                    "description": "Premium exit device with patented Powerglide mechanism for smooth, quiet operation under heavy use.",
                    "url": "https://www.seclock.com/catalog/price-books/sargent",
                    "model_numbers": ["8804", "8810", "8813", "8888"],
                    "features": ["Powerglide mechanism", "Modular design", "Delayed egress option", "Heavy-duty construction"],
                    "price_range": "$500-$1000",
                    "manufacturer": "Sargent"
                }
            ],
            "detex": [
                {
                    "name": "Detex ECL-230X Exit Control Lock",
                    "description": "Battery-powered alarmed exit device for emergency exits that require security monitoring.",
                    "url": "https://www.seclock.com/catalog/price-books/detex",
                    "model_numbers": ["ECL-230X", "ECL-230X-W"],
                    "features": ["95dB alarm", "Battery powered", "LED status indicator", "Delayed egress option"],
                    "price_range": "$350-$600",
                    "manufacturer": "Detex"
                }
            ]
        },
        # Hinges
        "hinges": {
            "mckinney": [
                {
                    "name": "McKinney TA2714 Heavy Weight Hinge",
                    "description": "Five-knuckle architectural hinge designed for heavy doors in high-frequency applications.",
                    "url": "https://www.seclock.com/catalog/price-books/mckinney",
                    "model_numbers": ["TA2714", "TA2714-4.5x4.5", "TA2714-5x5"],
                    "features": ["Heavy weight bearing", "Non-removable pin option", "Ball bearing", "NRP available"],
                    "price_range": "$25-$60 each",
                    "manufacturer": "McKinney"
                },
                {
                    "name": "McKinney T4A3786 Electric Hinge",
                    "description": "Electrified hinge for transferring power to door-mounted hardware without surface wiring.",
                    "url": "https://www.seclock.com/catalog/price-books/mckinney",
                    "model_numbers": ["T4A3786", "T4A3386"],
                    "features": ["Concealed wiring", "Multiple wire options", "Fire rated", "Ball bearing"],
                    "price_range": "$120-$250 each",
                    "manufacturer": "McKinney"
                }
            ],
            "hager": [
                {
                    "name": "Hager BB1279 Full Mortise Hinge",
                    "description": "Standard weight ball bearing hinge for commercial interior doors with high cycle life.",
                    "url": "https://www.seclock.com/catalog/price-books/hager",
                    "model_numbers": ["BB1279", "BB1279-4.5x4.5"],
                    "features": ["Ball bearing", "Template production", "Multiple finishes", "Lifetime warranty"],
                    "price_range": "$15-$40 each",
                    "manufacturer": "Hager"
                }
            ],
            "ives": [
                {
                    "name": "Ives 5BB1 Ball Bearing Hinge",
                    "description": "Five-knuckle ball bearing hinge for standard commercial applications with reliable performance.",
                    "url": "https://www.seclock.com/catalog/price-books/ives",
                    "model_numbers": ["5BB1", "5BB1-4.5x4.5", "5BB1HW"],
                    "features": ["Ball bearing", "Template drilled", "Steel or stainless", "NRP option"],
                    "price_range": "$18-$45 each",
                    "manufacturer": "Ives"
                }
            ]
        },
        # Electronic Access Control
        "electronic_access": {
            "hes": [
                {
                    "name": "HES 1006 Electric Strike",
                    "description": "Heavy-duty electric strike for cylindrical locksets with adjustable keeper for precise fit.",
                    "url": "https://www.seclock.com/catalog/price-books/hes",
                    "model_numbers": ["1006", "1006-12/24D-630", "1006CLB"],
                    "features": ["Fail-safe/fail-secure", "Adjustable keeper", "Dual voltage", "Latchbolt monitor"],
                    "price_range": "$150-$350",
                    "manufacturer": "HES"
                },
                {
                    "name": "HES 9600 Series Electric Strike",
                    "description": "Surface-mounted electric strike for rim exit devices with rugged construction.",
                    "url": "https://www.seclock.com/catalog/price-books/hes",
                    "model_numbers": ["9600", "9600-12/24D-630"],
                    "features": ["Surface mounted", "1500 lb holding force", "Dual voltage", "Fire rated"],
                    "price_range": "$200-$400",
                    "manufacturer": "HES"
                }
            ],
            "securitron": [
                {
                    "name": "Securitron M62 Magnalock",
                    "description": "Heavy-duty electromagnetic lock with 1200 lb holding force for high-security applications.",
                    "url": "https://www.seclock.com/catalog/price-books/securitron",
                    "model_numbers": ["M62", "M62D", "M62DGB"],
                    "features": ["1200 lb holding force", "LED status indicator", "Bond sensor option", "UL294 listed"],
                    "price_range": "$250-$450",
                    "manufacturer": "Securitron"
                }
            ],
            "alarm_lock": [
                {
                    "name": "Alarm Lock Trilogy T2 Digital Lock",
                    "description": "Standalone digital keypad lock with audit trail and multiple user codes.",
                    "url": "https://www.seclock.com/catalog/price-books/alarmlock",
                    "model_numbers": ["DL2700", "DL2800", "DL3000"],
                    "features": ["100 user codes", "Audit trail", "Weatherproof option", "BHMA Grade 1"],
                    "price_range": "$400-$700",
                    "manufacturer": "Alarm Lock"
                }
            ],
            "schlage_electronics": [
                {
                    "name": "Schlage CO-100 Cylindrical Electronic Lock",
                    "description": "Battery-powered standalone access control lock with keypad or card reader options.",
                    "url": "https://www.seclock.com/catalog/price-books/schlageele",
                    "model_numbers": ["CO-100", "CO-200", "CO-250"],
                    "features": ["Standalone or networked", "Up to 500 users", "Audit trail", "BHMA Grade 1"],
                    "price_range": "$500-$1000",
                    "manufacturer": "Schlage Electronics"
                }
            ]
        },
        # Locksets - Deadbolts & Specialty
        "deadbolts": {
            "schlage": [
                {
                    "name": "Schlage B Series Commercial Deadbolt",
                    "description": "Heavy-duty commercial deadbolt with Grade 1 security for maximum protection.",
                    "url": "https://www.seclock.com/catalog/price-books/schlage",
                    "model_numbers": ["B560P", "B562P", "B563P", "B580P"],
                    "features": ["ANSI Grade 1", "1\" throw bolt", "Anti-saw pins", "Hardened steel insert"],
                    "price_range": "$100-$250",
                    "manufacturer": "Schlage"
                }
            ],
            "medeco": [
                {
                    "name": "Medeco Maxum Commercial Deadbolt",
                    "description": "High-security deadbolt with patented key control and pick-resistant design.",
                    "url": "https://www.seclock.com/catalog/price-books/medeco",
                    "model_numbers": ["11-0102", "11-0202", "11-0602"],
                    "features": ["UL437 listed", "Bump resistant", "Drill resistant", "Patented key control"],
                    "price_range": "$350-$600",
                    "manufacturer": "Medeco"
                }
            ]
        },
        # Door Protection & Accessories
        "door_accessories": {
            "don_jo": [
                {
                    "name": "Don-Jo Wrap Around Plate",
                    "description": "Door reinforcement plate to protect and strengthen lock installation area.",
                    "url": "https://www.seclock.com/catalog/price-books/donjo",
                    "model_numbers": ["504-CW", "504-S-CW", "942-CW"],
                    "features": ["Steel construction", "Multiple finishes", "Easy installation", "Custom sizes"],
                    "price_range": "$25-$80",
                    "manufacturer": "Don-Jo"
                },
                {
                    "name": "Don-Jo Latch Protector",
                    "description": "Security plate to prevent forced entry through latch manipulation.",
                    "url": "https://www.seclock.com/catalog/price-books/donjo",
                    "model_numbers": ["LP-107", "LP-207", "OSLP-107"],
                    "features": ["14 gauge steel", "Pin and barrel hinge protection", "Multiple sizes", "Stainless available"],
                    "price_range": "$20-$60",
                    "manufacturer": "Don-Jo"
                }
            ],
            "rockwood": [
                {
                    "name": "Rockwood 85 Push/Pull Plate",
                    "description": "Architectural push and pull plates for commercial door aesthetics and protection.",
                    "url": "https://www.seclock.com/catalog/price-books/rockwood",
                    "model_numbers": ["85", "85-4x16", "85-6x16"],
                    "features": ["Multiple materials", "Custom sizing", "Beveled edges", "Fastener concealment"],
                    "price_range": "$40-$150",
                    "manufacturer": "Rockwood"
                },
                {
                    "name": "Rockwood RM3 Door Stop",
                    "description": "Heavy-duty floor-mounted door stop with solid construction.",
                    "url": "https://www.seclock.com/catalog/price-books/rockwood",
                    "model_numbers": ["RM3", "RM3-HT", "RM2"],
                    "features": ["Cast brass/bronze", "Concealed mounting", "Rubber bumper", "Multiple finishes"],
                    "price_range": "$15-$50",
                    "manufacturer": "Rockwood"
                }
            ],
            "ives": [
                {
                    "name": "Ives FB61 Flush Bolt",
                    "description": "Automatic flush bolt for securing inactive leaf of double doors.",
                    "url": "https://www.seclock.com/catalog/price-books/ives",
                    "model_numbers": ["FB61", "FB61P", "FB61T"],
                    "features": ["Automatic operation", "UL listed", "Fire rated", "Concealed design"],
                    "price_range": "$80-$200",
                    "manufacturer": "Ives"
                }
            ]
        },
        # Fire/Life Safety
        "fire_safety": {
            "lcn": [
                {
                    "name": "LCN 4640 Series Electromagnetic Holder",
                    "description": "Fire-rated electromagnetic door holder with wall or floor mounting options.",
                    "url": "https://www.seclock.com/catalog/price-books/lcn",
                    "model_numbers": ["4640", "4640-3049"],
                    "features": ["UL/cUL listed", "25-35 lb holding force", "Wall or floor mount", "Releases on alarm"],
                    "price_range": "$100-$200",
                    "manufacturer": "LCN"
                }
            ],
            "norton": [
                {
                    "name": "Norton 6000 Series Fire Door Holder",
                    "description": "Electromagnetic hold-open device for fire door applications with reliable release.",
                    "url": "https://www.seclock.com/catalog/price-books/norton",
                    "model_numbers": ["6000", "6000-689"],
                    "features": ["UL listed", "Tie-in to fire alarm", "Adjustable holding force", "Surface mount"],
                    "price_range": "$90-$180",
                    "manufacturer": "Norton"
                }
            ]
        },
        # Weatherstripping & Seals
        "weatherstripping": {
            "pemko": [
                {
                    "name": "Pemko S88 Door Bottom Seal",
                    "description": "Heavy-duty aluminum door bottom with silicone seal for weather and sound protection.",
                    "url": "https://www.seclock.com/catalog/price-books/pemko",
                    "model_numbers": ["S88D", "S88BL", "S88SL"],
                    "features": ["Silicone insert", "Aluminum housing", "Easy installation", "Sound reduction"],
                    "price_range": "$30-$80",
                    "manufacturer": "Pemko"
                },
                {
                    "name": "Pemko 303 Threshold",
                    "description": "Aluminum saddle threshold for commercial door openings.",
                    "url": "https://www.seclock.com/catalog/price-books/pemko",
                    "model_numbers": ["303AS", "303AV", "303ANB"],
                    "features": ["Aluminum construction", "ADA compliant heights", "Thermal break option", "Multiple widths"],
                    "price_range": "$25-$100",
                    "manufacturer": "Pemko"
                }
            ],
            "ngp": [
                {
                    "name": "NGP Door Smoke Seal",
                    "description": "Intumescent smoke seal for fire-rated door assemblies.",
                    "url": "https://www.seclock.com/catalog/price-books/ngp",
                    "model_numbers": ["970", "970N"],
                    "features": ["UL listed", "Expands with heat", "Smoke and draft seal", "Meets positive pressure"],
                    "price_range": "$20-$60",
                    "manufacturer": "NGP"
                }
            ]
        },
        # Automatic Door Operators
        "auto_operators": {
            "lcn": [
                {
                    "name": "LCN 4640 SENIOR SWING Low Energy Operator",
                    "description": "ADA-compliant low energy automatic door operator for accessibility applications.",
                    "url": "https://www.seclock.com/catalog/price-books/lcn",
                    "model_numbers": ["4640-3049T", "4640-3077T"],
                    "features": ["ADA compliant", "Low energy operation", "Push button activation", "Safety sensors"],
                    "price_range": "$1500-$2500",
                    "manufacturer": "LCN"
                }
            ],
            "norton": [
                {
                    "name": "Norton 5600 ADAEZ PRO Operator",
                    "description": "Integrated automatic door operator designed for ADA accessibility retrofits.",
                    "url": "https://www.seclock.com/catalog/price-books/norton",
                    "model_numbers": ["5600", "5610", "5620"],
                    "features": ["Easy retrofit", "No header needed", "ADA compliant", "Power open/close"],
                    "price_range": "$1800-$3000",
                    "manufacturer": "Norton"
                }
            ]
        },
        # Key Control & Cylinders
        "cylinders": {
            "medeco": [
                {
                    "name": "Medeco M3 High Security Cylinder",
                    "description": "Patented high-security cylinder with anti-pick, anti-drill, and bump-resistant features.",
                    "url": "https://www.seclock.com/catalog/price-books/medeco",
                    "model_numbers": ["20-0100", "20-0200", "20-0300"],
                    "features": ["UL437 listed", "Key control", "Bump resistant", "Retrofit compatible"],
                    "price_range": "$100-$250",
                    "manufacturer": "Medeco"
                }
            ],
            "best": [
                {
                    "name": "BEST 1E Series Interchangeable Core",
                    "description": "Small format interchangeable core cylinder for easy rekeying without removing hardware.",
                    "url": "https://www.seclock.com/catalog/price-books/best",
                    "model_numbers": ["1E74", "1E76", "1E7"],
                    "features": ["Tool-free removal", "6 or 7 pin options", "Master keying", "High security options"],
                    "price_range": "$40-$120",
                    "manufacturer": "BEST"
                }
            ]
        }
    }
    
    def get_recommendations(self, specs: Dict[str, Any]) -> List[ProductRecommendation]:
        """Generate product recommendations based on door specifications."""
        recommendations = []
        
        door_type = specs.get('doorType', 'interior')
        material = specs.get('material', 'wood')
        has_glass = specs.get('hasGlass', False)
        fire_rating = specs.get('fireRating', 'none')
        is_fire_rated = fire_rating != 'none'
        hardware_list = specs.get('hardware', [])
        width = float(specs.get('width', 36))
        height = float(specs.get('height', 80))
        
        # Determine door weight class
        is_heavy = width > 42 or height > 84 or material in ['steel', 'fiberglass']
        is_commercial = door_type in ['commercial', 'exterior-entry']
        
        # Door Closers - Always recommended for commercial
        if is_commercial or is_fire_rated:
            if is_heavy:
                # Heavy duty closers for large/heavy doors
                for closer in self.PRODUCTS['door_closers']['lcn'][:1]:
                    recommendations.append(self._create_recommendation(closer, "Door Closers"))
            else:
                # Standard duty for typical doors
                for closer in self.PRODUCTS['door_closers']['norton'][:1]:
                    recommendations.append(self._create_recommendation(closer, "Door Closers"))
        
        # Locks - Based on door type and security needs
        if 'lockset' in hardware_list or 'deadbolt' in hardware_list or is_commercial:
            if is_commercial:
                # Grade 1 commercial locks
                for lock in self.PRODUCTS['locks']['schlage'][:1]:
                    recommendations.append(self._create_recommendation(lock, "Commercial Locks"))
                for lock in self.PRODUCTS['locks']['corbin_russwin'][:1]:
                    recommendations.append(self._create_recommendation(lock, "Commercial Locks"))
            else:
                # Standard commercial grade
                for lock in self.PRODUCTS['locks']['schlage'][2:3]:  # ALX series
                    recommendations.append(self._create_recommendation(lock, "Cylindrical Locks"))
        
        # Deadbolts
        if 'deadbolt' in hardware_list:
            if specs.get('prepType') == 'high-security':
                for deadbolt in self.PRODUCTS['deadbolts']['medeco']:
                    recommendations.append(self._create_recommendation(deadbolt, "High-Security Deadbolts"))
            else:
                for deadbolt in self.PRODUCTS['deadbolts']['schlage']:
                    recommendations.append(self._create_recommendation(deadbolt, "Commercial Deadbolts"))
        
        # Exit Devices - For exterior and commercial
        if door_type in ['commercial', 'exterior-entry'] or 'panic' in hardware_list:
            for device in self.PRODUCTS['exit_devices']['von_duprin'][:1]:
                recommendations.append(self._create_recommendation(device, "Exit Devices"))
            for device in self.PRODUCTS['exit_devices']['falcon'][:1]:
                recommendations.append(self._create_recommendation(device, "Exit Devices"))
        
        # Hinges - Always needed
        hinge_count = int(specs.get('hingeCount', 3))
        if is_heavy or height > 84:
            for hinge in self.PRODUCTS['hinges']['mckinney'][:1]:
                recommendations.append(self._create_recommendation(hinge, "Hinges"))
        else:
            for hinge in self.PRODUCTS['hinges']['hager'][:1]:
                recommendations.append(self._create_recommendation(hinge, "Hinges"))
        
        # Electric hinges if electronic access
        if 'electric_strike' in hardware_list or 'maglock' in hardware_list:
            for hinge in self.PRODUCTS['hinges']['mckinney'][1:2]:
                recommendations.append(self._create_recommendation(hinge, "Electric Hinges"))
        
        # Electronic Access Control
        if 'electric_strike' in hardware_list:
            for strike in self.PRODUCTS['electronic_access']['hes'][:1]:
                recommendations.append(self._create_recommendation(strike, "Electric Strikes"))
        
        if 'maglock' in hardware_list:
            for maglock in self.PRODUCTS['electronic_access']['securitron']:
                recommendations.append(self._create_recommendation(maglock, "Electromagnetic Locks"))
        
        if 'keypad' in hardware_list:
            for keypad in self.PRODUCTS['electronic_access']['alarm_lock']:
                recommendations.append(self._create_recommendation(keypad, "Electronic Keypad Locks"))
            for keypad in self.PRODUCTS['electronic_access']['schlage_electronics']:
                recommendations.append(self._create_recommendation(keypad, "Electronic Access Control"))
        
        # Door Protection - For commercial and high-traffic
        if is_commercial:
            for plate in self.PRODUCTS['door_accessories']['don_jo'][:1]:
                recommendations.append(self._create_recommendation(plate, "Door Protection"))
            for push_plate in self.PRODUCTS['door_accessories']['rockwood'][:1]:
                recommendations.append(self._create_recommendation(push_plate, "Push/Pull Plates"))
        
        # Fire/Life Safety
        if is_fire_rated:
            for holder in self.PRODUCTS['fire_safety']['lcn']:
                recommendations.append(self._create_recommendation(holder, "Fire Door Hardware"))
            # Smoke seals
            for seal in self.PRODUCTS['weatherstripping']['ngp']:
                recommendations.append(self._create_recommendation(seal, "Fire Door Seals"))
        
        # Weatherstripping for exterior doors
        if door_type in ['exterior-entry', 'exterior-patio']:
            for seal in self.PRODUCTS['weatherstripping']['pemko']:
                recommendations.append(self._create_recommendation(seal, "Weatherstripping"))
        
        # Automatic Operators for accessibility
        if 'auto_operator' in hardware_list:
            for operator in self.PRODUCTS['auto_operators']['norton']:
                recommendations.append(self._create_recommendation(operator, "Automatic Door Operators"))
        
        # High Security Cylinders
        if specs.get('prepType') == 'high-security' or 'ic_core' in hardware_list:
            for cylinder in self.PRODUCTS['cylinders']['medeco']:
                recommendations.append(self._create_recommendation(cylinder, "High Security Cylinders"))
            for core in self.PRODUCTS['cylinders']['best']:
                recommendations.append(self._create_recommendation(core, "Interchangeable Cores"))
        
        return recommendations
    
    def _create_recommendation(self, product: Dict, category: str) -> ProductRecommendation:
        return ProductRecommendation(
            name=product['name'],
            category=category,
            description=product['description'],
            url=product['url'],
            model_numbers=product.get('model_numbers', []),
            features=product.get('features', []),
            price_range=product.get('price_range'),
            distributor=f"{self.name} ({product.get('manufacturer', '')})"
        )


class AssaAbloyDSSDistributor(BaseDistributor):
    """
    ASSA ABLOY Door Security Solutions - Doors and Frames
    https://www.assaabloydss.com/
    
    ASSA ABLOY Group brands offer steel doors, metal frames, specialty doors,
    and aesthetic design options from brands including Ceco Door, Curries,
    Baron, and RITE Door.
    """
    
    name = "ASSA ABLOY Door Security Solutions"
    website = "https://www.assaabloydss.com"
    logo_url = "https://www.assaabloydss.com/content/dam/assa-abloy/americas/dss/assa-abloy-dss/logos/assa-abloy-logo.svg"
    phone = "800-377-3948"
    
    # Doors and Frames product catalog
    PRODUCTS = {
        # Standard Hollow Metal Doors
        "hollow_metal_doors": {
            "ceco": [
                {
                    "name": "Ceco Standard Steel Door",
                    "description": "Strong and secure steel doors designed to meet a full range of safety, security, and aesthetic requirements. Available in various gauges and configurations.",
                    "url": "https://www.cecodoor.com/en/products/",
                    "model_numbers": ["Series 18", "Series 16", "Series 14"],
                    "features": ["18, 16, or 14 gauge steel", "Flush or embossed face", "Fire rated options", "Multiple core options"],
                    "price_range": "$350-$800",
                    "manufacturer": "Ceco Door"
                },
                {
                    "name": "Ceco Fire-Rated Steel Door",
                    "description": "UL labeled fire-rated hollow metal doors for commercial and industrial applications requiring fire protection up to 3 hours.",
                    "url": "https://www.cecodoor.com/en/products/",
                    "model_numbers": ["FR-20", "FR-45", "FR-60", "FR-90", "FR-180"],
                    "features": ["20-minute to 3-hour ratings", "Positive pressure tested", "Temperature rise options", "Smoke and draft control"],
                    "price_range": "$500-$1,500",
                    "manufacturer": "Ceco Door"
                }
            ],
            "curries": [
                {
                    "name": "Curries Commercial Steel Door",
                    "description": "Full line of custom and standard hollow metal doors for new and retrofit construction projects. Ideal for healthcare, commercial, and educational markets.",
                    "url": "https://www.curries.com/en/products/",
                    "model_numbers": ["707", "747", "757", "767"],
                    "features": ["Custom sizes available", "Multiple gauge options", "Insulated core options", "Sound dampening"],
                    "price_range": "$400-$900",
                    "manufacturer": "Curries"
                },
                {
                    "name": "Curries Stile & Rail Door",
                    "description": "Architectural stile and rail doors with glass lite options for aesthetically demanding applications.",
                    "url": "https://www.curries.com/en/products/",
                    "model_numbers": ["SR-1", "SR-2", "SR-3"],
                    "features": ["Glass lite options", "Architectural finishes", "Vision panel configurations", "ADA compliant"],
                    "price_range": "$600-$1,400",
                    "manufacturer": "Curries"
                }
            ],
            "baron": [
                {
                    "name": "Baron Embossed Steel Door",
                    "description": "Embossed or standard hollow metal doors in 14-, 16-, 18- and 20-gauge options for commercial applications.",
                    "url": "https://www.baronmetal.com/en/products/",
                    "model_numbers": ["BE-18", "BE-16", "BE-14", "BS-18"],
                    "features": ["Embossed or smooth face", "Multiple gauges", "Honeycomb or polystyrene core", "Primed finish"],
                    "price_range": "$300-$700",
                    "manufacturer": "Baron"
                }
            ],
            "rite_door": [
                {
                    "name": "RITE Door Designer Series",
                    "description": "Unique aesthetic door finishes and designer options with preassembled hardware devices for upscale commercial applications.",
                    "url": "https://www.ritedoor.com/en/",
                    "model_numbers": ["RD-100", "RD-200", "RD-300"],
                    "features": ["Wood grain finishes", "Stainless steel options", "Factory-installed hardware", "Custom colors"],
                    "price_range": "$800-$2,000",
                    "manufacturer": "RITE Door"
                }
            ]
        },
        # Hollow Metal Frames
        "hollow_metal_frames": {
            "ceco": [
                {
                    "name": "Ceco Welded Frame",
                    "description": "Heavy-duty welded hollow metal frames for masonry or drywall construction. Superior strength for commercial applications.",
                    "url": "https://www.cecodoor.com/en/products/",
                    "model_numbers": ["WF-16", "WF-14", "WF-12"],
                    "features": ["Welded corners", "16, 14, or 12 gauge", "Masonry or drywall anchors", "Multiple throat sizes"],
                    "price_range": "$200-$500",
                    "manufacturer": "Ceco Door"
                },
                {
                    "name": "Ceco Knock-Down Frame",
                    "description": "Field-assembled knocked down frames for easy shipping and installation in retrofit applications.",
                    "url": "https://www.cecodoor.com/en/products/",
                    "model_numbers": ["KD-16", "KD-14"],
                    "features": ["Easy field assembly", "No welding required", "Adjustable for out-of-square openings", "Standard or fire rated"],
                    "price_range": "$150-$350",
                    "manufacturer": "Ceco Door"
                }
            ],
            "curries": [
                {
                    "name": "Curries Drywall Frame",
                    "description": "Hollow metal frames designed specifically for drywall construction with concealed anchoring systems.",
                    "url": "https://www.curries.com/en/products/",
                    "model_numbers": ["DW-S", "DW-D", "DW-B"],
                    "features": ["Drywall anchor system", "Single or double rabbet", "Adjustable base anchors", "Fire rated options"],
                    "price_range": "$175-$400",
                    "manufacturer": "Curries"
                }
            ],
            "baron": [
                {
                    "name": "Baron Masonry Frame",
                    "description": "14-, 16- and 18-gauge masonry or drywall frames for standard commercial door openings.",
                    "url": "https://www.baronmetal.com/en/products/",
                    "model_numbers": ["MF-16", "MF-14", "MF-18"],
                    "features": ["Masonry anchors included", "Multiple gauges", "Standard throat sizes", "Primed finish"],
                    "price_range": "$150-$350",
                    "manufacturer": "Baron"
                }
            ]
        },
        # Specialty Doors
        "specialty_doors": {
            "acoustical": [
                {
                    "name": "Acoustical Door Opening - STC Rated",
                    "description": "STC-rated doors for offices, schools, hotels, and anywhere noise transference could be problematic. Available in various STC ratings.",
                    "url": "https://www.assaabloydss.com/en/products/doors-and-frames/specialty-doors/product-details.aehpdp-acoustical-openings-dss_assa_abloy_dss_99370",
                    "model_numbers": ["STC-35", "STC-40", "STC-45", "STC-50"],
                    "features": ["STC ratings 35-55", "Gasketed perimeter", "Automatic door bottom", "Vision panel options"],
                    "price_range": "$1,500-$4,000",
                    "manufacturer": "ASSA ABLOY DSS"
                }
            ],
            "bullet_resistant": [
                {
                    "name": "Bullet Resistant Door Opening",
                    "description": "Multiple levels of protection against ballistic threats, tested and certified to strict UL 752 standards.",
                    "url": "https://www.assaabloydss.com/en/products/doors-and-frames/specialty-doors/product-details.aehpdp-bullet-resistant-openings-dss_assa_abloy_dss_99369",
                    "model_numbers": ["BR-1", "BR-3", "BR-4", "BR-8"],
                    "features": ["UL 752 Levels 1-8", "Steel and composite construction", "Matching bullet-resistant frames", "Vision panel options"],
                    "price_range": "$3,000-$15,000",
                    "manufacturer": "ASSA ABLOY DSS"
                }
            ],
            "blast_resistant": [
                {
                    "name": "Blast Resistant Door Opening",
                    "description": "Protection against explosions and excessive force. Designed for critical infrastructure and government facilities.",
                    "url": "https://www.assaabloydss.com/en/products/doors-and-frames/specialty-doors/product-details.aehpdp-blast-resistant-openings-dss_assa_abloy_dss_227316",
                    "model_numbers": ["BR-GSA", "BR-DOD", "BR-ISC"],
                    "features": ["GSA/ISC compliant", "DoD certified", "Blast tested", "Hazard mitigation"],
                    "price_range": "$5,000-$25,000",
                    "manufacturer": "ASSA ABLOY DSS"
                }
            ],
            "hurricane_resistant": [
                {
                    "name": "Hurricane Resistant Door Opening",
                    "description": "Essential in storm zones, ensuring safety and property protection. Florida Building Code and Miami-Dade approved.",
                    "url": "https://www.assaabloydss.com/en/products/doors-and-frames/specialty-doors/product-details.aehpdp-hurricane-resistant-openings-dss_assa_abloy_dss_227321",
                    "model_numbers": ["HC-S", "HC-M", "HC-L"],
                    "features": ["Florida Building Code approved", "Miami-Dade NOA", "Large/small missile impact", "HVHZ rated"],
                    "price_range": "$2,000-$8,000",
                    "manufacturer": "ASSA ABLOY DSS"
                },
                {
                    "name": "StormPro Hurricane and Tornado Resistant Opening",
                    "description": "Designed to protect against missile penetration from wind-borne debris for hurricane and tornado shelters.",
                    "url": "https://www.assaabloydss.com/en/products/doors-and-frames/specialty-doors/product-details.aehpdp-stormpro-hurricane-and-tornado-resistant-openings-dss_assa_abloy_dss_824814",
                    "model_numbers": ["SP-FEMA", "SP-ICC"],
                    "features": ["FEMA P-361 compliant", "ICC 500 certified", "EF5 tornado rated", "Shelter door approved"],
                    "price_range": "$4,000-$12,000",
                    "manufacturer": "ASSA ABLOY DSS"
                }
            ],
            "attack_resistant": [
                {
                    "name": "Attack Resistant Door Opening",
                    "description": "Forced entry resistant openings that prioritize safety and security with cutting-edge materials.",
                    "url": "https://www.assaabloydss.com/en/products/doors-and-frames/specialty-doors/product-details.aehpdp-attack-resistant-openings-dss_assa_abloy_dss_227315",
                    "model_numbers": ["FE-5", "FE-10", "FE-15"],
                    "features": ["Forced entry rated", "5-15 minute attack ratings", "Reinforced construction", "High-security hardware"],
                    "price_range": "$2,500-$10,000",
                    "manufacturer": "ASSA ABLOY DSS"
                },
                {
                    "name": "Forced Entry Bullet Resistant Opening",
                    "description": "Combines ballistic and forced-entry resistance with cutting-edge materials for unparalleled protection.",
                    "url": "https://www.assaabloydss.com/en/products/doors-and-frames/specialty-doors/product-details.aehpdp-forced-entry-bullet-resistant-openings-dss_assa_abloy_dss_227320",
                    "model_numbers": ["FEBR-3", "FEBR-5", "FEBR-8"],
                    "features": ["Combined FE + BR rating", "UL 752 ballistic", "ASTM forced entry", "Embassy-grade protection"],
                    "price_range": "$8,000-$30,000",
                    "manufacturer": "ASSA ABLOY DSS"
                }
            ],
            "flood_resistant": [
                {
                    "name": "Flood Resistant Door Opening",
                    "description": "Specially designed doorways that keep out water up to a depth of 36 inches for flood-prone facilities.",
                    "url": "https://www.assaabloydss.com/en/products/doors-and-frames/specialty-doors/product-details.aehpdp-flood-resistant-openings-dss_assa_abloy_dss_227319",
                    "model_numbers": ["FL-24", "FL-36"],
                    "features": ["24\" or 36\" water depth", "FM Approved", "Watertight gaskets", "Manual or automatic"],
                    "price_range": "$3,000-$8,000",
                    "manufacturer": "ASSA ABLOY DSS"
                }
            ],
            "lead_lined": [
                {
                    "name": "Lead-Lined Door Opening",
                    "description": "High-quality lead-lined door openings for radiation protection in medical and industrial applications.",
                    "url": "https://www.assaabloydss.com/en/products/doors-and-frames/specialty-doors/product-details.aehpdp-lead-lined-openings-dss_assa_abloy_dss_227322",
                    "model_numbers": ["LL-1/16", "LL-1/8", "LL-1/4"],
                    "features": ["1/16\" to 1/2\" lead equivalent", "Radiation shielding", "Healthcare compliant", "X-ray room rated"],
                    "price_range": "$2,000-$6,000",
                    "manufacturer": "ASSA ABLOY DSS"
                }
            ],
            "stainless_steel": [
                {
                    "name": "Stainless Steel Door Opening",
                    "description": "Sleek stainless steel doors and frames offering corrosion resistance and enhanced aesthetic appeal.",
                    "url": "https://www.assaabloydss.com/en/products/doors-and-frames/specialty-doors/product-details.aehpdp-stainless-steel-openings-dss_assa_abloy_dss_223738",
                    "model_numbers": ["SS-304", "SS-316"],
                    "features": ["304 or 316 stainless", "Corrosion resistant", "Hygienic", "Multiple finishes"],
                    "price_range": "$1,500-$4,500",
                    "manufacturer": "ASSA ABLOY DSS"
                }
            ],
            "emi_rfi_shielding": [
                {
                    "name": "EMI-RFI/STC Shielding Door Assembly",
                    "description": "Protects sensitive communications and electronics from electromagnetic interference. For data centers, SCIF, and military applications.",
                    "url": "https://www.assaabloydss.com/en/products/doors-and-frames/specialty-doors/product-details.aehpdp-emi-rfistc-shielding-assembly-with-split-frame-and-adjustable-seals-dss_assa_abloy_dss_959145",
                    "model_numbers": ["EMI-40", "EMI-60", "EMI-100"],
                    "features": ["40-100 dB shielding", "TEMPEST compliant", "SCIF requirements", "Combined STC rating"],
                    "price_range": "$8,000-$25,000",
                    "manufacturer": "ASSA ABLOY DSS"
                }
            ],
            "water_resistant": [
                {
                    "name": "Water Resistant Door Opening",
                    "description": "Sanitary and watertight solution for clean rooms, laboratories, or chemical storage areas.",
                    "url": "https://www.assaabloydss.com/en/products/doors-and-frames/specialty-doors/product-details.aehpdp-water-resistant-openings-dss_assa_abloy_dss_227324",
                    "model_numbers": ["WR-S", "WR-L"],
                    "features": ["Watertight seal", "Cleanroom compatible", "Chemical resistant", "Stainless steel option"],
                    "price_range": "$2,500-$6,000",
                    "manufacturer": "ASSA ABLOY DSS"
                }
            ]
        }
    }
    
    def get_recommendations(self, specs: Dict[str, Any]) -> List[ProductRecommendation]:
        """Generate door and frame recommendations based on specifications."""
        recommendations = []
        
        door_type = specs.get('doorType', 'interior')
        material = specs.get('material', 'wood')
        fire_rating = specs.get('fireRating', 'none')
        is_fire_rated = fire_rating != 'none'
        width = float(specs.get('width', 36))
        height = float(specs.get('height', 80))
        
        # Determine if commercial/industrial steel doors are appropriate
        is_commercial = door_type in ['commercial', 'exterior-entry']
        needs_steel = material in ['steel', 'fiberglass'] or is_commercial or is_fire_rated
        
        # Standard Hollow Metal Doors - for commercial/steel applications
        if needs_steel:
            if is_fire_rated:
                # Fire-rated steel doors
                for door in self.PRODUCTS['hollow_metal_doors']['ceco'][1:2]:  # Fire-rated
                    recommendations.append(self._create_recommendation(door, "Fire-Rated Steel Doors"))
            else:
                # Standard steel doors
                for door in self.PRODUCTS['hollow_metal_doors']['ceco'][:1]:
                    recommendations.append(self._create_recommendation(door, "Commercial Steel Doors"))
                for door in self.PRODUCTS['hollow_metal_doors']['curries'][:1]:
                    recommendations.append(self._create_recommendation(door, "Commercial Steel Doors"))
            
            # Always recommend frames for steel doors
            for frame in self.PRODUCTS['hollow_metal_frames']['ceco'][:1]:
                recommendations.append(self._create_recommendation(frame, "Hollow Metal Frames"))
        
        # Specialty Doors - based on specific requirements
        # Check for specialty requirements (these could be added to specs in the future)
        specialty_type = specs.get('specialtyType', None)
        
        if specialty_type == 'acoustical' or specs.get('acoustical', False):
            for door in self.PRODUCTS['specialty_doors']['acoustical']:
                recommendations.append(self._create_recommendation(door, "Acoustical Doors"))
        
        if specialty_type == 'bullet_resistant' or specs.get('bulletResistant', False):
            for door in self.PRODUCTS['specialty_doors']['bullet_resistant']:
                recommendations.append(self._create_recommendation(door, "Bullet Resistant Doors"))
        
        if specialty_type == 'blast_resistant' or specs.get('blastResistant', False):
            for door in self.PRODUCTS['specialty_doors']['blast_resistant']:
                recommendations.append(self._create_recommendation(door, "Blast Resistant Doors"))
        
        if specialty_type == 'hurricane_resistant' or specs.get('hurricaneResistant', False):
            for door in self.PRODUCTS['specialty_doors']['hurricane_resistant']:
                recommendations.append(self._create_recommendation(door, "Hurricane Resistant Doors"))
        
        if specialty_type == 'attack_resistant' or specs.get('attackResistant', False):
            for door in self.PRODUCTS['specialty_doors']['attack_resistant']:
                recommendations.append(self._create_recommendation(door, "Attack Resistant Doors"))
        
        if specialty_type == 'flood_resistant' or specs.get('floodResistant', False):
            for door in self.PRODUCTS['specialty_doors']['flood_resistant']:
                recommendations.append(self._create_recommendation(door, "Flood Resistant Doors"))
        
        if specialty_type == 'lead_lined' or specs.get('leadLined', False):
            for door in self.PRODUCTS['specialty_doors']['lead_lined']:
                recommendations.append(self._create_recommendation(door, "Lead-Lined Doors"))
        
        if specialty_type == 'stainless_steel' or material == 'stainless':
            for door in self.PRODUCTS['specialty_doors']['stainless_steel']:
                recommendations.append(self._create_recommendation(door, "Stainless Steel Doors"))
        
        if specialty_type == 'emi_shielding' or specs.get('emiShielding', False):
            for door in self.PRODUCTS['specialty_doors']['emi_rfi_shielding']:
                recommendations.append(self._create_recommendation(door, "EMI/RFI Shielding Doors"))
        
        # Designer doors for upscale commercial
        if is_commercial and specs.get('aesthetic', False):
            for door in self.PRODUCTS['hollow_metal_doors']['rite_door']:
                recommendations.append(self._create_recommendation(door, "Designer Steel Doors"))
        
        return recommendations
    
    def _create_recommendation(self, product: Dict, category: str) -> ProductRecommendation:
        return ProductRecommendation(
            name=product['name'],
            category=category,
            description=product['description'],
            url=product['url'],
            model_numbers=product.get('model_numbers', []),
            features=product.get('features', []),
            price_range=product.get('price_range'),
            distributor=f"{self.name} ({product.get('manufacturer', '')})"
        )


# Registry of all available distributors
DISTRIBUTORS = {
    'dormakaba': DormakabaDistributor(),
    'seclock': SecLockDistributor(),
    'assaabloy_dss': AssaAbloyDSSDistributor(),
}


def get_all_recommendations(specs: Dict[str, Any], distributor_ids: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Get product recommendations from all or specified distributors.
    
    Args:
        specs: Door specifications dictionary
        distributor_ids: Optional list of distributor IDs to query. If None, queries all.
    
    Returns:
        Dictionary with distributor info and their recommendations
    """
    results = {
        "distributors": [],
        "total_recommendations": 0
    }
    
    distributors_to_query = DISTRIBUTORS
    if distributor_ids:
        distributors_to_query = {k: v for k, v in DISTRIBUTORS.items() if k in distributor_ids}
    
    for dist_id, distributor in distributors_to_query.items():
        recommendations = distributor.get_recommendations(specs)
        dist_result = {
            "id": dist_id,
            **distributor.to_dict(),
            "recommendations": [r.to_dict() for r in recommendations],
            "recommendation_count": len(recommendations)
        }
        results["distributors"].append(dist_result)
        results["total_recommendations"] += len(recommendations)
    
    return results


def get_available_distributors() -> List[Dict[str, Any]]:
    """Return list of all available distributors."""
    return [
        {"id": dist_id, **dist.to_dict()}
        for dist_id, dist in DISTRIBUTORS.items()
    ]
