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


ASSET_RING_CAMPAIGN = "https://customer-assets.emergentagent.com/job_shopify-gems-2/artifacts/8jfge9he_fashion-%26-beauty-design-2x%20%281%29%20%281%29.png"
ASSET_GRILL_CROWN = "https://customer-assets.emergentagent.com/job_shopify-gems-2/artifacts/y62y0h0m_fashion-%26-beauty-design-2x%20%282%29%20%281%29.png"
ASSET_GRILL_SMILES = "https://customer-assets.emergentagent.com/job_shopify-gems-2/artifacts/rqlc637n_fashion-%26-beauty-design-2x%20%284%29%20%281%29.png"
ASSET_GRILL_DETAIL = "https://customer-assets.emergentagent.com/job_shopify-gems-2/artifacts/q8yfzjph_fashion-%26-beauty-design-2x%20%283%29%20%281%29.png"
ASSET_GRILL_BEFORE_AFTER = "https://customer-assets.emergentagent.com/job_shopify-gems-2/artifacts/yruo7fl8_fashion-%26-beauty-design-2x%20%285%29%20%281%29.png"
ASSET_CHAIN_IMAGE = "https://supremejewelers.com/cdn/shop/files/NCK00702B._7_57529e40-a13e-4acc-a79f-9ae93784f021.jpg?v=1743765226"
ASSET_NECKLACE_IMAGE = "https://supremejewelers.com/cdn/shop/files/NCK00706FINAL_7.jpg?v=1743765844"
ASSET_BRACELET_IMAGE = "https://supremejewelers.com/cdn/shop/files/21LBR00824.jpg?v=1743759681"


PRODUCTS = [
    {
        "id": "royal-solitaire-spark-ring",
        "name": "Royal Solitaire Spark Ring",
        "slug": "royal-solitaire-spark-ring",
        "category": "Rings",
        "price": 3890,
        "currency": "USD",
        "materials": ["14K White Gold", "Lab Diamond"],
        "is_customizable": True,
        "featured": True,
        "short_description": "A bright-cut solitaire ring inspired by high-shine showroom campaigns.",
        "description": "Designed for the Royal Spark signature look, this solitaire profile delivers clean brilliance, polished shoulders, and a modern showroom finish for everyday luxury.",
        "hero_image": ASSET_RING_CAMPAIGN,
        "gallery": [
            ASSET_RING_CAMPAIGN,
            "https://supremejewelers.com/cdn/shop/files/Male_ring.jpg?v=1746694447&width=768"
        ],
        "rating": 4.9,
        "review_count": 44,
        "highlights": ["Center-stone focus", "High-polish finish", "Custom sizing available"],
        "reviews": [
            {"author": "Amelia", "rating": 5, "title": "Bright and clean", "comment": "The shine is strong and the setting feels premium.", "date": "2026-02-11"},
            {"author": "Nora", "rating": 5, "title": "Looks expensive in person", "comment": "Exactly the type of ring I wanted for a standout piece.", "date": "2026-01-28"}
        ]
    },
    {
        "id": "emerald-halo-royal-ring",
        "name": "Emerald Halo Royal Ring",
        "slug": "emerald-halo-royal-ring",
        "category": "Rings",
        "price": 4625,
        "currency": "USD",
        "materials": ["14K White Gold", "Natural Diamond"],
        "is_customizable": True,
        "featured": True,
        "short_description": "Halo styling with a bold rectangular center silhouette and extra sparkle.",
        "description": "Inspired by statement showroom campaigns, this halo ring layers crisp lines, brilliant framing stones, and a tall-profile look for clients who want maximum presence.",
        "hero_image": ASSET_RING_CAMPAIGN,
        "gallery": [
            ASSET_RING_CAMPAIGN,
            "https://supremejewelers.com/cdn/shop/files/Female_band.jpg?v=1746694447&width=768"
        ],
        "rating": 4.8,
        "review_count": 29,
        "highlights": ["Halo brilliance", "Engagement-ready", "Luxury gift presentation"],
        "reviews": [
            {"author": "Ella", "rating": 5, "title": "Strong sparkle", "comment": "The halo catches light beautifully from every angle.", "date": "2026-03-01"},
            {"author": "Sofia", "rating": 4, "title": "Feels very premium", "comment": "Looks like a showcase piece right out of a luxury catalog.", "date": "2026-02-03"}
        ]
    },
    {
        "id": "diamond-smile-grill-set",
        "name": "Diamond Smile Grill Set",
        "slug": "diamond-smile-grill-set",
        "category": "Grills",
        "price": 2150,
        "currency": "USD",
        "materials": ["Silver Tone", "Iced Stones"],
        "is_customizable": False,
        "featured": True,
        "short_description": "Statement grill styling with a bright iced-out finish for instant impact.",
        "description": "Built for bold smiles and campaign-ready shine, this full-set grill design gives clients a strong entry point into Royal Spark’s custom grill offering.",
        "hero_image": ASSET_GRILL_SMILES,
        "gallery": [
            ASSET_GRILL_SMILES,
            ASSET_GRILL_DETAIL
        ],
        "rating": 4.9,
        "review_count": 37,
        "highlights": ["Custom-fit ready", "Photo-ready sparkle", "Popular starter grill style"],
        "reviews": [
            {"author": "Jay", "rating": 5, "title": "Exactly the shine I wanted", "comment": "The look pops on camera and feels like a premium custom set.", "date": "2026-02-14"}
        ]
    },
    {
        "id": "gold-classic-grill-set",
        "name": "Gold Classic Grill Set",
        "slug": "gold-classic-grill-set",
        "category": "Grills",
        "price": 1795,
        "currency": "USD",
        "materials": ["Yellow Gold Finish", "Mirror Polish"],
        "is_customizable": False,
        "featured": False,
        "short_description": "A polished gold grill look with a smoother, classic street-luxury finish.",
        "description": "For clients who want a cleaner metal-first statement, this gold grill concept emphasizes shape, polish, and boldness over heavy stone coverage.",
        "hero_image": ASSET_GRILL_DETAIL,
        "gallery": [
            ASSET_GRILL_DETAIL,
            ASSET_GRILL_SMILES
        ],
        "rating": 4.8,
        "review_count": 24,
        "highlights": ["Smooth gold finish", "Custom top/bottom options", "Street-luxury style"],
        "reviews": [
            {"author": "Marcus", "rating": 5, "title": "Clean gold look", "comment": "Simple, bold, and exactly right for a classic setup.", "date": "2026-03-12"}
        ]
    },
    {
        "id": "vvs-before-after-grill-set",
        "name": "VVS Before & After Grill Set",
        "slug": "vvs-before-after-grill-set",
        "category": "Grills",
        "price": 2890,
        "currency": "USD",
        "materials": ["Gold Tone", "VVS-style stones"],
        "is_customizable": True,
        "featured": False,
        "short_description": "A high-contrast grill concept built around dramatic before-and-after presentation.",
        "description": "This custom grill concept is perfect for ad campaigns, showroom consultations, and transformation-led selling that highlights the final smile upgrade.",
        "hero_image": ASSET_GRILL_BEFORE_AFTER,
        "gallery": [
            ASSET_GRILL_BEFORE_AFTER,
            ASSET_GRILL_CROWN
        ],
        "rating": 5.0,
        "review_count": 16,
        "highlights": ["Before/after presentation", "Premium custom consultation", "Ideal for social content"],
        "reviews": [
            {"author": "Dre", "rating": 5, "title": "This sells itself", "comment": "The before-and-after look makes it easy for clients to imagine the result.", "date": "2026-01-09"}
        ]
    },
    {
        "id": "radiant-bezel-chain-necklace",
        "name": "Radiant Bezel Chain Necklace",
        "slug": "radiant-bezel-chain-necklace",
        "category": "Chains",
        "price": 5345,
        "currency": "USD",
        "materials": ["14K Gold", "Diamond"],
        "is_customizable": True,
        "featured": False,
        "short_description": "A high-visibility chain necklace with bezel-set sparkle and retail-ready appeal.",
        "description": "Inspired by luxury showroom best sellers, this chain style adds a polished, high-ticket necklace option to the Royal Spark range for future expansion.",
        "hero_image": ASSET_CHAIN_IMAGE,
        "gallery": [
            ASSET_CHAIN_IMAGE,
            ASSET_NECKLACE_IMAGE
        ],
        "rating": 4.7,
        "review_count": 18,
        "highlights": ["Diamond bezel links", "Layering-friendly", "Future Shopify bestseller"],
        "reviews": [
            {"author": "Noah", "rating": 5, "title": "Looks strong in the showcase", "comment": "This is the type of chain clients ask about immediately.", "date": "2026-02-19"}
        ]
    },
    {
        "id": "mixed-cut-tennis-bracelet",
        "name": "Mixed Cut Tennis Bracelet",
        "slug": "mixed-cut-tennis-bracelet",
        "category": "Bracelets",
        "price": 6825,
        "currency": "USD",
        "materials": ["14K White Gold", "Mixed Cut Diamonds"],
        "is_customizable": True,
        "featured": False,
        "short_description": "A refined bracelet option for clients who want classic sparkle beyond rings.",
        "description": "This mixed-cut tennis bracelet adds a future-ready bracelet category with premium styling, high perceived value, and strong cross-sell potential.",
        "hero_image": ASSET_BRACELET_IMAGE,
        "gallery": [
            ASSET_BRACELET_IMAGE,
            "https://supremejewelers.com/cdn/shop/files/2LBR00824.jpg?v=1743759681&width=533"
        ],
        "rating": 4.8,
        "review_count": 15,
        "highlights": ["Mixed diamond cuts", "Luxury gifting option", "Classic tennis profile"],
        "reviews": [
            {"author": "Mia", "rating": 5, "title": "Balanced and elegant", "comment": "A strong bracelet option with serious shine.", "date": "2026-02-19"}
        ]
    }
]

COLLECTIONS = [
    {
        "id": "signature-rings",
        "name": "Signature Rings",
        "category": "Rings",
        "description": "Solitaire, halo, and statement ring styles inspired by luxury retail showcases.",
        "image": ASSET_RING_CAMPAIGN
    },
    {
        "id": "grill-collection",
        "name": "Royal Grillz",
        "category": "Grills",
        "description": "Custom-fit gold and iced grill looks for bold luxury styling.",
        "image": ASSET_GRILL_SMILES
    },
    {
        "id": "chains-bracelets",
        "name": "Chains & Bracelets",
        "category": "Chains",
        "description": "Retail-ready necklace and bracelet styles prepared for the next catalog expansion.",
        "image": ASSET_CHAIN_IMAGE
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
    return {"message": "Royal Spark API is running."}

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
            "title": "Blue Label Campaign",
            "description": "Royal Spark now blends deep midnight blue, gold highlights, diamond rings, and custom grill concepts into one client-ready luxury storefront.",
            "image": ASSET_GRILL_CROWN,
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