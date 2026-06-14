import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Literal, Optional
from uuid import uuid4

from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, ConfigDict, Field
from starlette.middleware.cors import CORSMiddleware


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


def format_money(value: float) -> str:
    return f"${value:,.0f}"


PRODUCTS = [
    {
        "id": "solstice-diamond-ring",
        "name": "Solstice Diamond Ring",
        "slug": "solstice-diamond-ring",
        "category": "Rings",
        "price": 4200,
        "currency": "USD",
        "materials": ["18K Gold", "Platinum"],
        "is_customizable": True,
        "featured": True,
        "short_description": "A sculpted diamond ring with graceful pavé detail.",
        "description": "Our Solstice ring frames a brilliant center diamond with a refined, hand-set pavé halo and a softly tapered band designed for daily elegance.",
        "hero_image": "https://images.unsplash.com/photo-1611955167811-4711904bb9f8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA1MDV8MHwxfHNlYXJjaHwzfHxmaW5lJTIwamV3ZWxyeXxlbnwwfHx8fDE3ODE0Mzc3MzN8MA&ixlib=rb-4.1.0&q=85",
        "gallery": [
            "https://images.unsplash.com/photo-1611955167811-4711904bb9f8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA1MDV8MHwxfHNlYXJjaHwzfHxmaW5lJTIwamV3ZWxyeXxlbnwwfHx8fDE3ODE0Mzc3MzN8MA&ixlib=rb-4.1.0&q=85",
            "https://images.unsplash.com/photo-1605100804763-247f67b3557e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA1MDV8MHwxfHNlYXJjaHwxfHxmaW5lJTIwamV3ZWxyeXxlbnwwfHx8fDE3ODE0Mzc3MzN8MA&ixlib=rb-4.1.0&q=85"
        ],
        "rating": 4.9,
        "review_count": 32,
        "highlights": ["Hand-set pavé", "Conflict-conscious sourcing", "Made to order in 14 days"],
        "reviews": [
            {"author": "Amelia", "rating": 5, "title": "Absolutely radiant", "comment": "The finish is flawless and it feels timeless.", "date": "2026-02-11"},
            {"author": "Nora", "rating": 5, "title": "Elegant without being loud", "comment": "Exactly what I wanted for a forever piece.", "date": "2026-01-28"}
        ]
    },
    {
        "id": "luna-pearl-necklace",
        "name": "Luna Pearl Necklace",
        "slug": "luna-pearl-necklace",
        "category": "Necklaces",
        "price": 1950,
        "currency": "USD",
        "materials": ["Freshwater Pearl", "18K Gold"],
        "is_customizable": True,
        "featured": True,
        "short_description": "An airy strand of luminous pearls with a discreet gold clasp.",
        "description": "Luna is composed for understated ceremony—balanced proportions, softly reflective pearls, and an heirloom sensibility that sits beautifully against silk or skin.",
        "hero_image": "https://images.unsplash.com/photo-1654699991520-aaaf4dd2608b?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA1NDh8MHwxfHNlYXJjaHwyfHxlbGVnYW50JTIwcGVhcmwlMjBuZWNrbGFjZSUyMGpld2Vscnl8ZW58MHx8fHwxNzgxNDM3NzIzfDA&ixlib=rb-4.1.0&q=85",
        "gallery": [
            "https://images.unsplash.com/photo-1654699991520-aaaf4dd2608b?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA1NDh8MHwxfHNlYXJjaHwyfHxlbGVnYW50JTIwcGVhcmwlMjBuZWNrbGFjZSUyMGpld2Vscnl8ZW58MHx8fHwxNzgxNDM3NzIzfDA&ixlib=rb-4.1.0&q=85",
            "https://images.unsplash.com/photo-1611652022419-a9419f74343d?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA1NDh8MHwxfHNlYXJjaHwxfHxlbGVnYW50JTIwcGVhcmwlMjBuZWNrbGFjZSUyMGpld2Vscnl8ZW58MHx8fHwxNzgxNDM3NzIzfDA&ixlib=rb-4.1.0&q=85"
        ],
        "rating": 4.8,
        "review_count": 21,
        "highlights": ["Hand-knotted strand", "Soft luster matching", "Gift boxed"],
        "reviews": [
            {"author": "Ella", "rating": 5, "title": "Pure luxury", "comment": "It elevates every outfit instantly.", "date": "2026-03-01"},
            {"author": "Sofia", "rating": 4, "title": "Beautiful craftsmanship", "comment": "The pearls feel carefully selected and balanced.", "date": "2026-02-03"}
        ]
    },
    {
        "id": "aurum-chain-bracelet",
        "name": "Aurum Chain Bracelet",
        "slug": "aurum-chain-bracelet",
        "category": "Bracelets",
        "price": 1280,
        "currency": "USD",
        "materials": ["18K Gold"],
        "is_customizable": False,
        "featured": False,
        "short_description": "A refined gold chain with fluid movement and quiet shine.",
        "description": "Aurum is designed with custom-cast links and a near-weightless drape, offering a luxurious everyday bracelet that layers effortlessly.",
        "hero_image": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?auto=format&fit=crop&w=1200&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1617038260897-41a1f14a8ca0?auto=format&fit=crop&w=1200&q=80"
        ],
        "rating": 4.7,
        "review_count": 18,
        "highlights": ["Fluid hand feel", "Secure clasp", "Designed for stacking"],
        "reviews": [
            {"author": "Grace", "rating": 5, "title": "So easy to wear", "comment": "The clasp feels secure and premium.", "date": "2026-02-14"}
        ]
    },
    {
        "id": "stellare-drop-earrings",
        "name": "Stellare Drop Earrings",
        "slug": "stellare-drop-earrings",
        "category": "Earrings",
        "price": 1640,
        "currency": "USD",
        "materials": ["White Gold", "Diamond"],
        "is_customizable": False,
        "featured": True,
        "short_description": "Diamond drops designed to catch candlelight and conversation.",
        "description": "Light, elongated, and balanced, Stellare brings fine diamond movement to evening dressing without sacrificing comfort.",
        "hero_image": "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?auto=format&fit=crop&w=1200&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1617038220319-276d3cfab638?auto=format&fit=crop&w=1200&q=80"
        ],
        "rating": 4.9,
        "review_count": 26,
        "highlights": ["Lightweight balance", "High brilliance stones", "Secure post fastening"],
        "reviews": [
            {"author": "Layla", "rating": 5, "title": "Wedding-perfect", "comment": "They shimmer beautifully without feeling heavy.", "date": "2026-03-12"}
        ]
    },
    {
        "id": "atelier-signature-pendant",
        "name": "Atelier Signature Pendant",
        "slug": "atelier-signature-pendant",
        "category": "Custom",
        "price": 3100,
        "currency": "USD",
        "materials": ["18K Gold", "Diamond", "Engravable"],
        "is_customizable": True,
        "featured": False,
        "short_description": "A bespoke pendant designed around your story and stone selection.",
        "description": "Begin with our signature silhouette and tailor every detail—from engraving and chain length to gemstone and gold tone—for a deeply personal piece.",
        "hero_image": "https://images.unsplash.com/photo-1617038220319-276d3cfab638?auto=format&fit=crop&w=1200&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1617038220319-276d3cfab638?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1624585179018-25699030cb8f?auto=format&fit=crop&w=1200&q=80"
        ],
        "rating": 5.0,
        "review_count": 9,
        "highlights": ["Design consultation included", "Rendered before production", "Ideal for gifting or milestones"],
        "reviews": [
            {"author": "Harper", "rating": 5, "title": "Meaningful and beautifully made", "comment": "The team translated my idea perfectly.", "date": "2026-01-09"}
        ]
    },
    {
        "id": "velour-emerald-ring",
        "name": "Velour Emerald Ring",
        "slug": "velour-emerald-ring",
        "category": "Rings",
        "price": 3850,
        "currency": "USD",
        "materials": ["Yellow Gold", "Emerald", "Diamond"],
        "is_customizable": True,
        "featured": False,
        "short_description": "An emerald centerpiece framed with discreet diamond brilliance.",
        "description": "Velour pairs a richly saturated emerald with architectural gold lines for a ring that feels both classic and distinctly modern.",
        "hero_image": "https://images.pexels.com/photos/2849742/pexels-photo-2849742.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
        "gallery": [
            "https://images.pexels.com/photos/2849742/pexels-photo-2849742.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
            "https://images.unsplash.com/photo-1605100804763-247f67b3557e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA1MDV8MHwxfHNlYXJjaHwxfHxmaW5lJTIwamV3ZWxyeXxlbnwwfHx8fDE3ODE0Mzc3MzN8MA&ixlib=rb-4.1.0&q=85"
        ],
        "rating": 4.8,
        "review_count": 14,
        "highlights": ["Statement stone", "Available in bespoke sizing", "Hand-finished prongs"],
        "reviews": [
            {"author": "Mia", "rating": 5, "title": "Rich color and lovely setting", "comment": "The emerald has incredible depth.", "date": "2026-02-19"}
        ]
    }
]

COLLECTIONS = [
    {
        "id": "bridal-rings",
        "name": "Bridal & Forever",
        "category": "Rings",
        "description": "Ceremony-ready rings and heirloom silhouettes.",
        "image": "https://images.pexels.com/photos/32988751/pexels-photo-32988751.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940"
    },
    {
        "id": "soft-lustre",
        "name": "Pearls & Light",
        "category": "Necklaces",
        "description": "Luminous pieces with soft editorial grace.",
        "image": "https://images.unsplash.com/photo-1611652022419-a9419f74343d?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA1NDh8MHwxfHNlYXJjaHwxfHxlbGVnYW50JTIwcGVhcmwlMjBuZWNrbGFjZSUyMGpld2Vscnl8ZW58MHx8fHwxNzgxNDM3NzIzfDA&ixlib=rb-4.1.0&q=85"
    },
    {
        "id": "bespoke-atelier",
        "name": "Bespoke Atelier",
        "category": "Custom",
        "description": "Designed around milestones, stories, and one-of-one commissions.",
        "image": "https://images.unsplash.com/photo-1624585179018-25699030cb8f?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA1MDV8MHwxfHNlYXJjaHw0fHxmaW5lJTIwamV3ZWxyeXxlbnwwfHx8fDE3ODE0Mzc3MzN8MA&ixlib=rb-4.1.0&q=85"
    }
]


class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str = Field(default_factory=lambda: str(uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class StatusCheckCreate(BaseModel):
    client_name: str


class Review(BaseModel):
    author: str
    rating: int
    title: str
    comment: str
    date: str


class Product(BaseModel):
    id: str
    name: str
    slug: str
    category: str
    price: float
    currency: str
    materials: List[str]
    is_customizable: bool
    featured: bool
    short_description: str
    description: str
    hero_image: str
    gallery: List[str]
    rating: float
    review_count: int
    highlights: List[str]
    reviews: List[Review]


class ProductSummary(BaseModel):
    id: str
    name: str
    slug: str
    category: str
    price: float
    currency: str
    formatted_price: str
    hero_image: str
    rating: float
    review_count: int
    short_description: str
    featured: bool
    is_customizable: bool


class Collection(BaseModel):
    id: str
    name: str
    category: str
    description: str
    image: str


class CatalogResponse(BaseModel):
    items: List[ProductSummary]
    total: int
    categories: List[str]


class HomeResponse(BaseModel):
    hero_product: ProductSummary
    featured_products: List[ProductSummary]
    collections: List[Collection]
    atelier_story: dict
    testimonials: List[Review]


class BespokeInquiryCreate(BaseModel):
    name: str
    email: str
    jewelry_type: str
    budget: str
    material_preference: str
    inspiration: Optional[str] = ""
    timeline: str
    message: str


class BespokeInquiryResponse(BespokeInquiryCreate):
    id: str
    created_at: str
    status: Literal["received"]


class ShopifyReadiness(BaseModel):
    connection_ready: bool
    next_step: str
    supported_sync_targets: List[str]


def build_product_summary(product: dict) -> ProductSummary:
    return ProductSummary(
        id=product["id"],
        name=product["name"],
        slug=product["slug"],
        category=product["category"],
        price=product["price"],
        currency=product["currency"],
        formatted_price=format_money(product["price"]),
        hero_image=product["hero_image"],
        rating=product["rating"],
        review_count=product["review_count"],
        short_description=product["short_description"],
        featured=product["featured"],
        is_customizable=product["is_customizable"],
    )

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Maison Aurelle API is running."}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.model_dump()
    status_obj = StatusCheck(**status_dict)
    
    # Convert to dict and serialize datetime to ISO string for MongoDB
    doc = status_obj.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()
    
    _ = await db.status_checks.insert_one(doc)
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    # Exclude MongoDB's _id field from the query results
    status_checks = await db.status_checks.find({}, {"_id": 0}).to_list(1000)
    
    # Convert ISO string timestamps back to datetime objects
    for check in status_checks:
        if isinstance(check['timestamp'], str):
            check['timestamp'] = datetime.fromisoformat(check['timestamp'])
    
    return status_checks


@api_router.get("/catalog/home", response_model=HomeResponse)
async def get_home_catalog():
    featured_products = [build_product_summary(product) for product in PRODUCTS if product["featured"]]
    testimonials = [review for product in PRODUCTS for review in product["reviews"][:1]][:4]
    return HomeResponse(
        hero_product=featured_products[0],
        featured_products=featured_products,
        collections=[Collection(**collection) for collection in COLLECTIONS],
        atelier_story={
            "title": "The Atelier",
            "description": "Each piece begins with a sketch, a material study, and the discipline of hand-finishing. Maison Aurelle is designed for moments that deserve permanence.",
            "image": "https://images.unsplash.com/photo-1624585179018-25699030cb8f?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA1MDV8MHwxfHNlYXJjaHw0fHxmaW5lJTIwamV3ZWxyeXxlbnwwfHx8fDE3ODE0Mzc3MzN8MA&ixlib=rb-4.1.0&q=85",
        },
        testimonials=testimonials,
    )


@api_router.get("/catalog/products", response_model=CatalogResponse)
async def get_products(
    category: Optional[str] = Query(default=None),
    search: Optional[str] = Query(default=None),
    customizable_only: bool = Query(default=False),
):
    filtered = PRODUCTS
    if category and category.lower() != "all":
        filtered = [item for item in filtered if item["category"].lower() == category.lower()]
    if search:
        term = search.lower().strip()
        filtered = [
            item for item in filtered
            if term in item["name"].lower()
            or term in item["category"].lower()
            or term in item["description"].lower()
            or any(term in material.lower() for material in item["materials"])
        ]
    if customizable_only:
        filtered = [item for item in filtered if item["is_customizable"]]

    categories = sorted({product["category"] for product in PRODUCTS})
    return CatalogResponse(
        items=[build_product_summary(product) for product in filtered],
        total=len(filtered),
        categories=["All", *categories],
    )


@api_router.get("/catalog/products/{slug}", response_model=Product)
async def get_product_detail(slug: str):
    product = next((item for item in PRODUCTS if item["slug"] == slug), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return Product(**product)


@api_router.get("/catalog/collections", response_model=List[Collection])
async def get_collections():
    return [Collection(**collection) for collection in COLLECTIONS]


@api_router.post("/bespoke-inquiries", response_model=BespokeInquiryResponse, status_code=201)
async def create_bespoke_inquiry(payload: BespokeInquiryCreate):
    inquiry_id = str(uuid4())
    created_at = datetime.now(timezone.utc).isoformat()
    inquiry_doc = {
        "id": inquiry_id,
        "name": payload.name,
        "email": payload.email,
        "jewelry_type": payload.jewelry_type,
        "budget": payload.budget,
        "material_preference": payload.material_preference,
        "inspiration": payload.inspiration or "",
        "timeline": payload.timeline,
        "message": payload.message,
        "created_at": created_at,
        "status": "received",
    }
    await db.bespoke_inquiries.insert_one(inquiry_doc.copy())
    return BespokeInquiryResponse(**inquiry_doc)


@api_router.get("/shopify/readiness", response_model=ShopifyReadiness)
async def get_shopify_readiness():
    return ShopifyReadiness(
        connection_ready=False,
        next_step="Create your Shopify store, generate Storefront/Admin credentials, then map products and checkout redirects.",
        supported_sync_targets=[
            "products",
            "collections",
            "inventory",
            "checkout redirect",
            "custom jewelry intake tagging",
        ],
    )

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()