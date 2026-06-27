import logging
import os
import re
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from typing import List, Literal, Optional
from uuid import uuid4

from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, ConfigDict, Field
import requests
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


def strip_html(value: str) -> str:
    if not value:
        return ""
    text = re.sub(r"<[^>]+>", " ", value)
    text = unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def truncate_text(value: str, max_length: int = 120) -> str:
    if len(value) <= max_length:
        return value
    return value[: max_length - 1].rstrip() + "…"


def get_shopify_store_domain() -> Optional[str]:
    value = os.environ.get("SHOPIFY_STORE_DOMAIN")
    return value.strip() if value else None


def get_shopify_admin_token() -> Optional[str]:
    value = os.environ.get("SHOPIFY_ADMIN_TOKEN")
    return value.strip() if value else None


def shopify_is_configured() -> bool:
    return bool(get_shopify_store_domain() and get_shopify_admin_token())


def shopify_headers() -> dict:
    token = get_shopify_admin_token()
    if not token:
        raise HTTPException(status_code=503, detail="Shopify is not configured")
    return {
        "X-Shopify-Access-Token": token,
        "Content-Type": "application/json",
    }


def fetch_shopify_resource(path: str, params: Optional[dict] = None) -> dict:
    store_domain = get_shopify_store_domain()
    if not store_domain:
        raise HTTPException(status_code=503, detail="Shopify store domain missing")

    response = requests.get(
        f"https://{store_domain}/admin/api/2025-04/{path}",
        headers=shopify_headers(),
        params=params or {},
        timeout=30,
    )
    if response.status_code >= 400:
        raise HTTPException(status_code=502, detail=f"Shopify API error: {response.text[:200]}")
    return response.json()


def derive_product_category(product: dict) -> str:
    product_type = (product.get("product_type") or "").strip()
    if product_type in CATEGORY_LIST:
        return product_type

    tags = [tag.strip() for tag in (product.get("tags") or "").split(",") if tag.strip()]
    for category in CATEGORY_LIST:
        if category.lower() in {tag.lower() for tag in tags}:
            return category

    title = (product.get("title") or "").lower()
    if "grill" in title:
        return "Grills"
    if "ring" in title:
        return "Rings"
    if "earring" in title:
        return "Earrings"
    if "bangle" in title:
        return "Bangles"
    if "bracelet" in title:
        return "Bracelets"
    if "chain" in title:
        return "Chains"
    if "charm" in title:
        return "Charms"
    return "Rings"


def derive_materials(product: dict) -> List[str]:
    tags = [tag.strip() for tag in (product.get("tags") or "").split(",") if tag.strip()]
    known_materials = ["Moissanite", "Gold", "Silver", "Diamond", "Platinum", "White Gold", "Yellow Gold"]
    materials = [material for material in known_materials if any(material.lower() in tag.lower() for tag in tags)]

    if not materials:
        options = product.get("options") or []
        for option in options:
            if option.get("name", "").lower() in {"material", "metal"}:
                values = option.get("values") or []
                materials.extend([value for value in values if value])

    return materials or ["Signature Finish"]


def transform_shopify_product(product: dict) -> dict:
    description = strip_html(product.get("body_html") or "")
    variants = product.get("variants") or []
    first_variant = variants[0] if variants else {}
    images = product.get("images") or []
    gallery = [image.get("src") for image in images if image.get("src")]
    hero_image = gallery[0] if gallery else ASSET_RING_CAMPAIGN
    tags = [tag.strip() for tag in (product.get("tags") or "").split(",") if tag.strip()]
    featured = any(tag.lower() in {"featured", "best seller", "bestseller"} for tag in tags)
    customizable = any(tag.lower() in {"custom", "customizable", "bespoke"} for tag in tags)
    price_value = float(first_variant.get("price") or 0)
    category = derive_product_category(product)
    materials = derive_materials(product)

    return {
        "id": str(product.get("id")),
        "name": product.get("title") or "Untitled Product",
        "slug": product.get("handle") or str(product.get("id")),
        "category": category,
        "price": price_value,
        "currency": "USD",
        "materials": materials,
        "is_customizable": customizable,
        "featured": featured,
        "short_description": truncate_text(description or f"{category} by Royal Spark", 110),
        "description": description or f"{category} by Royal Spark.",
        "hero_image": hero_image,
        "gallery": gallery or [hero_image],
        "rating": 5.0,
        "review_count": 0,
        "highlights": materials[:3] if materials else ["Luxury Finish"],
        "reviews": [],
    }


def fetch_live_shopify_products() -> List[dict]:
    if not shopify_is_configured():
        return PRODUCTS
    payload = fetch_shopify_resource("products.json", {"limit": 250, "status": "active"})
    products = payload.get("products") or []
    return [transform_shopify_product(product) for product in products]


def fetch_live_shopify_collections() -> List[dict]:
    if not shopify_is_configured():
        return COLLECTIONS

    collections: List[dict] = []
    for path, key in (("custom_collections.json", "custom_collections"), ("smart_collections.json", "smart_collections")):
        payload = fetch_shopify_resource(path, {"limit": 50})
        for collection in payload.get(key) or []:
            title = collection.get("title") or "Collection"
            collections.append(
                {
                    "id": str(collection.get("id")),
                    "name": title,
                    "category": title,
                    "description": f"Explore the {title} collection.",
                    "image": ASSET_RING_CAMPAIGN,
                }
            )

    return collections or COLLECTIONS


ASSET_RING_CAMPAIGN = "https://customer-assets.emergentagent.com/job_shopify-gems-2/artifacts/8jfge9he_fashion-%26-beauty-design-2x%20%281%29%20%281%29.png"
ASSET_GRILL_CROWN = "https://customer-assets.emergentagent.com/job_shopify-gems-2/artifacts/y62y0h0m_fashion-%26-beauty-design-2x%20%282%29%20%281%29.png"
ASSET_GRILL_SMILES = "https://customer-assets.emergentagent.com/job_shopify-gems-2/artifacts/rqlc637n_fashion-%26-beauty-design-2x%20%284%29%20%281%29.png"
ASSET_GRILL_DETAIL = "https://customer-assets.emergentagent.com/job_shopify-gems-2/artifacts/q8yfzjph_fashion-%26-beauty-design-2x%20%283%29%20%281%29.png"
ASSET_GRILL_BEFORE_AFTER = "https://customer-assets.emergentagent.com/job_shopify-gems-2/artifacts/yruo7fl8_fashion-%26-beauty-design-2x%20%285%29%20%281%29.png"
ASSET_CHAIN_IMAGE = "https://supremejewelers.com/cdn/shop/files/NCK00702B._7_57529e40-a13e-4acc-a79f-9ae93784f021.jpg?v=1743765226"
ASSET_NECKLACE_IMAGE = "https://supremejewelers.com/cdn/shop/files/NCK00706FINAL_7.jpg?v=1743765844"
ASSET_BRACELET_IMAGE = "https://supremejewelers.com/cdn/shop/files/21LBR00824.jpg?v=1743759681"


PRODUCTS = []

CATEGORY_LIST = [
    "Bangles",
    "Bracelets",
    "Chains",
    "Charms",
    "Earrings",
    "Grills",
    "Rings",
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
    },
    {
        "id": "contact-collection",
        "name": "Contact Royal Spark",
        "category": "Contact",
        "description": "Visit, call, or request a private consultation in Houston, Texas.",
        "image": ASSET_GRILL_BEFORE_AFTER
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
    hero_product: Optional[ProductSummary] = None
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
    has_store_domain: Optional[bool] = None
    has_admin_token: Optional[bool] = None


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
    live_products = fetch_live_shopify_products()
    featured_products = [build_product_summary(product) for product in live_products if product["featured"]][:6]
    if not featured_products:
        featured_products = [build_product_summary(product) for product in live_products[:6]]
    testimonials = [review for product in live_products for review in product["reviews"][:1]][:4]
    return HomeResponse(
        hero_product=featured_products[0] if featured_products else None,
        featured_products=featured_products,
        collections=[Collection(**collection) for collection in fetch_live_shopify_collections()],
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
    material: Optional[str] = Query(default=None),
):
    filtered = fetch_live_shopify_products()
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
    if material:
        material_term = material.lower().strip()
        filtered = [
            item for item in filtered
            if any(material_term in product_material.lower() for product_material in item["materials"])
        ]

    categories = sorted({*CATEGORY_LIST, *{product["category"] for product in filtered}})
    return CatalogResponse(
        items=[build_product_summary(product) for product in filtered],
        total=len(filtered),
        categories=["All", *categories],
    )


@api_router.get("/catalog/products/{slug}", response_model=Product)
async def get_product_detail(slug: str):
    live_products = fetch_live_shopify_products()
    product = next((item for item in live_products if item["slug"] == slug), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return Product(**product)


@api_router.get("/catalog/collections", response_model=List[Collection])
async def get_collections():
    return [Collection(**collection) for collection in fetch_live_shopify_collections()]


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
    configured = shopify_is_configured()
    return ShopifyReadiness(
        connection_ready=configured,
        next_step=(
            "Shopify is connected. Add active products and collections in Shopify to populate the storefront."
            if configured
            else "Create your Shopify store, generate Storefront/Admin credentials, then map products and checkout redirects."
        ),
        supported_sync_targets=[
            "products",
            "collections",
            "inventory",
            "checkout redirect",
            "custom jewelry intake tagging",
        ],
        has_store_domain=bool(get_shopify_store_domain()),
        has_admin_token=bool(get_shopify_admin_token()),
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