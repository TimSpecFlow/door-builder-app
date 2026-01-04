from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import EstimateSerializer
import base64
import json
import re
import os

# Try to import OpenAI - will be used for AI measurement parsing
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class EstimateView(APIView):
    """Return a comprehensive price estimate based on all door specifications."""

    # Material base costs per square foot
    MATERIAL_COSTS = {
        'wood': 60.0,
        'wood-hollow': 25.0,
        'steel': 45.0,
        'fiberglass': 55.0,
        'aluminum': 70.0,
        'composite': 50.0,
    }

    # Jamb material costs
    JAMB_COSTS = {
        'wood': 35.0,
        'mdf': 25.0,
        'steel': 65.0,
        'aluminum': 80.0,
        'composite': 45.0,
    }

    # Door type multipliers
    DOOR_TYPE_MULTIPLIERS = {
        'interior': 1.0,
        'exterior-entry': 1.5,
        'exterior-patio': 1.8,
        'closet': 0.8,
        'barn': 1.4,
        'pocket': 1.6,
        'bifold': 0.9,
        'commercial': 2.0,
    }

    # Panel style additions
    PANEL_STYLE_COSTS = {
        'flat': 0,
        '2-panel': 50,
        '4-panel': 75,
        '6-panel': 100,
        'shaker': 80,
        'craftsman': 120,
        'french': 200,
        'louvered': 150,
    }

    # Glass options
    GLASS_TYPE_COSTS = {
        'clear': 100,
        'frosted': 150,
        'textured': 175,
        'rain': 200,
        'low-e': 250,
        'tempered': 180,
        'impact': 400,
    }

    LITE_PATTERN_MULTIPLIERS = {
        'full': 1.0,
        'half': 0.6,
        '3/4': 0.8,
        '1/4': 0.4,
        '9-lite': 1.2,
        '15-lite': 1.5,
        'sidelight': 0.5,
        'fanlight': 0.4,
    }

    # Hardware costs - Based on SecLock distributor pricing
    # Prices are mid-range estimates from actual distributor catalogs
    HARDWARE_COSTS = {
        # Basic Hardware
        'hinges': 45,           # ~$15-25 each x3 for standard door
        'handle': 85,           # Mid-range commercial lever
        'lockset': 250,         # Schlage ND Series or equivalent Grade 1
        'deadbolt': 150,        # Commercial grade deadbolt
        'doorCloser': 300,      # LCN/Norton surface mounted closer
        'kickplate': 45,        # 8" x door width stainless
        
        # Weatherproofing
        'weatherstrip': 60,     # Pemko or similar full perimeter
        'threshold': 85,        # Commercial aluminum threshold
        
        # Electronic Access Control
        'electric_strike': 250,  # HES 1006 or equivalent
        'maglock': 350,          # Securitron M62 (1200lb)
        'keypad': 550,           # Alarm Lock Trilogy or Schlage CO-100
        
        # Exit & Safety Devices
        'panic': 650,            # Von Duprin 99 series rim device
        'auto_operator': 2200,   # Norton/LCN low-energy ADA operator
        
        # Key Control
        'ic_core': 150,          # BEST small format IC with core
    }

    # Fire rating additions
    FIRE_RATING_COSTS = {
        'none': 0,
        '20-min': 150,
        '45-min': 300,
        '60-min': 500,
        '90-min': 750,
    }

    # Finish costs
    FINISH_COSTS = {
        'unfinished': 0,
        'primed': 50,
        'painted': 150,
        'stained': 200,
        'pre-finished': 175,
    }

    # Thickness additions
    THICKNESS_COSTS = {
        '1-3/8': 0,
        '1-3/4': 25,
        '2': 75,
        '2-1/4': 125,
    }

    def post(self, request):
        data = request.data
        
        # Core dimensions
        width = float(data.get('width', 36))
        height = float(data.get('height', 80))
        thickness = data.get('thickness', '1-3/4')
        
        # Calculate door area in square feet
        area_sqft = (width * height) / 144.0
        
        # Base door cost
        material = data.get('material', 'wood').lower()
        material_cost = self.MATERIAL_COSTS.get(material, 60.0)
        door_base = area_sqft * material_cost
        
        # Door type multiplier
        door_type = data.get('doorType', 'interior')
        type_multiplier = self.DOOR_TYPE_MULTIPLIERS.get(door_type, 1.0)
        door_base *= type_multiplier
        
        # Thickness addition
        door_base += self.THICKNESS_COSTS.get(thickness, 0)
        
        # Panel style
        panel_style = data.get('panelStyle', 'flat')
        door_base += self.PANEL_STYLE_COSTS.get(panel_style, 0)
        
        # Jamb/Frame cost
        jamb_width = float(data.get('jambWidth', 4.5))
        jamb_material = data.get('jambMaterial', 'wood').lower()
        jamb_linear_feet = (height * 2 + width) / 12.0  # Two sides + top
        jamb_cost = jamb_linear_feet * self.JAMB_COSTS.get(jamb_material, 35.0)
        
        # Glass options
        glass_cost = 0
        if data.get('hasGlass', False):
            glass_type = data.get('glassType', 'clear')
            lite_pattern = data.get('litePattern', 'full')
            base_glass = self.GLASS_TYPE_COSTS.get(glass_type, 100)
            pattern_mult = self.LITE_PATTERN_MULTIPLIERS.get(lite_pattern, 1.0)
            glass_cost = base_glass * pattern_mult * (area_sqft / 10)  # Scale by door size
        
        # Hardware
        hardware_cost = 0
        hardware_list = data.get('hardware', [])
        for h in hardware_list:
            h_lower = h.lower().replace(' ', '').replace('_', '')
            hardware_cost += self.HARDWARE_COSTS.get(h_lower, 0)
        
        # Fire rating
        fire_rating = data.get('fireRating', 'none')
        fire_cost = self.FIRE_RATING_COSTS.get(fire_rating, 0)
        
        # Finish
        finish = data.get('finish', 'unfinished')
        finish_cost = self.FINISH_COSTS.get(finish, 0)
        
        # Total estimate
        total = door_base + jamb_cost + glass_cost + hardware_cost + fire_cost + finish_cost
        
        # Labor estimate (roughly 40% of materials for installation)
        labor = total * 0.40
        
        total_with_labor = total + labor

        return Response({
            'estimate': round(total_with_labor, 2),
            'breakdown': {
                'door_slab': round(door_base, 2),
                'frame_jamb': round(jamb_cost, 2),
                'glass': round(glass_cost, 2),
                'hardware': round(hardware_cost, 2),
                'fire_rating': round(fire_cost, 2),
                'finish': round(finish_cost, 2),
                'materials_subtotal': round(total, 2),
                'labor': round(labor, 2),
            }
        })


class ParseMeasurementsView(APIView):
    """
    AI-powered measurement parser that can read:
    - Handwritten measurements from photos
    - Digital documents (PDFs, images)
    - Scanned specification sheets
    """

    SYSTEM_PROMPT = """You are an expert at reading door specifications and measurements from images.
Your task is to extract complete door measurements and specifications from the provided image.

Look for ALL of the following specifications:

DIMENSIONS:
- Width (in inches - convert from feet if needed, e.g., 3'0" = 36")
- Height (in inches - convert from feet if needed, e.g., 6'8" = 80")
- Thickness (common values: 1-3/8", 1-3/4", 2", 2-1/4")
- Jamb width (typically 4.5" to 6.5" for residential)
- Rough opening dimensions

DOOR CONFIGURATION:
- Door type: interior, exterior-entry, exterior-patio, closet, barn, pocket, bifold, commercial
- Swing direction: left-inswing, right-inswing, left-outswing, right-outswing
- Material: wood, wood-hollow, steel, fiberglass, aluminum, composite
- Panel style: flat, 2-panel, 4-panel, 6-panel, shaker, craftsman, french, louvered

GLASS/LITE OPTIONS:
- Whether glass is included (true/false)
- Glass type: clear, frosted, textured, rain, low-e, tempered, impact
- Lite pattern: full, half, 3/4, 1/4, 9-lite, 15-lite, sidelight, fanlight

HARDWARE PREP:
- Hinge count: 2, 3, or 4
- Bore size: 2-1/8", 1-1/2", or none
- Backset: 2-3/8", 2-3/4", or 5"

HARDWARE:
- hinges, handle, lockset, deadbolt, doorCloser, kickplate, weatherstrip, threshold

OTHER:
- Fire rating: none, 20-min, 45-min, 60-min, 90-min
- Finish: unfinished, primed, painted, stained, pre-finished

Return your response as valid JSON with this structure:
{
    "success": true,
    "measurements": {
        "width": <number in inches or null>,
        "height": <number in inches or null>,
        "thickness": "<string like '1-3/4' or null>",
        "jambWidth": <number or null>,
        "roughOpeningWidth": <number or null>,
        "roughOpeningHeight": <number or null>,
        "doorType": "<type or null>",
        "swingDirection": "<direction or null>",
        "material": "<material or null>",
        "panelStyle": "<style or null>",
        "hasGlass": <true/false or null>,
        "glassType": "<type or null>",
        "litePattern": "<pattern or null>",
        "hingeCount": <2/3/4 or null>,
        "boreSize": "<size or null>",
        "backset": "<size or null>",
        "hardware": ["list", "of", "hardware"],
        "fireRating": "<rating or null>",
        "finish": "<finish or null>",
        "notes": "<any additional notes or specifications found>"
    },
    "confidence": "<high/medium/low>",
    "raw_text": "<any text you can read from the image>"
}

IMPORTANT: 
- Convert all measurements to inches
- Set fields to null if not found in the image
- The image may be handwritten notes, typed documents, blueprints, or photos with measuring tape"""

    def post(self, request):
        if not OPENAI_AVAILABLE:
            return Response(
                {'error': 'OpenAI package not installed. Run: pip install openai'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key:
            return Response(
                {'error': 'OPENAI_API_KEY environment variable not set'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        # Get the uploaded file or base64 image
        image_file = request.FILES.get('image')
        image_base64 = request.data.get('image_base64')
        image_url = request.data.get('image_url')

        if not image_file and not image_base64 and not image_url:
            return Response(
                {'error': 'No image provided. Send image file, base64 data, or URL.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            client = OpenAI(api_key=api_key)

            # Prepare the image for the API
            if image_file:
                # Read and encode the uploaded file
                image_data = base64.b64encode(image_file.read()).decode('utf-8')
                content_type = image_file.content_type or 'image/jpeg'
                image_content = {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{content_type};base64,{image_data}",
                        "detail": "high"
                    }
                }
            elif image_base64:
                # Use provided base64 data
                # Remove data URL prefix if present
                if ',' in image_base64:
                    image_base64 = image_base64.split(',')[1]
                image_content = {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_base64}",
                        "detail": "high"
                    }
                }
            else:
                # Use URL directly
                image_content = {
                    "type": "image_url",
                    "image_url": {
                        "url": image_url,
                        "detail": "high"
                    }
                }

            # Call OpenAI Vision API
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": self.SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Please analyze this image and extract any door measurements and specifications you can find. Return the results as JSON."
                            },
                            image_content
                        ]
                    }
                ],
                max_tokens=1000,
                temperature=0.1
            )

            # Parse the response
            result_text = response.choices[0].message.content

            # Try to extract JSON from the response
            try:
                # Look for JSON in the response
                json_match = re.search(r'\{[\s\S]*\}', result_text)
                if json_match:
                    result = json.loads(json_match.group())
                else:
                    result = {
                        "success": False,
                        "error": "Could not parse AI response",
                        "raw_response": result_text
                    }
            except json.JSONDecodeError:
                result = {
                    "success": False,
                    "error": "Invalid JSON in AI response",
                    "raw_response": result_text
                }

            return Response(result)

        except Exception as e:
            return Response(
                {'error': str(e), 'success': False},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProductRecommendationsView(APIView):
    """
    Get product recommendations from distributors based on door specifications.
    """

    def post(self, request):
        from .distributors import get_all_recommendations
        
        specs = request.data
        
        # Optional: filter by specific distributors
        distributor_ids = request.data.get('distributors', None)
        
        try:
            results = get_all_recommendations(specs, distributor_ids)
            return Response(results)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DistributorsView(APIView):
    """
    List all available distributors.
    """

    def get(self, request):
        from .distributors import get_available_distributors
        
        return Response({
            'distributors': get_available_distributors()
        })


class GenerateQuotePDFView(APIView):
    """
    Generate a professional PDF quote for door specifications.
    """

    def post(self, request):
        from django.http import HttpResponse
        from .pdf_generator import QuoteGenerator
        
        specs = request.data.get('specs', {})
        estimate = request.data.get('estimate', {})
        recommendations = request.data.get('recommendations', [])
        
        try:
            generator = QuoteGenerator()
            pdf_buffer = generator.generate_quote(specs, estimate, recommendations)
            
            # Create HTTP response with PDF
            response = HttpResponse(pdf_buffer.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="SpecFlow_Quote.pdf"'
            
            return response
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
