
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy import create_engine, String, Float, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, sessionmaker

# ---------------- DATABASE SETUP ----------------

DATABASE_URL = "sqlite:///./products.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- SQLALCHEMY MODEL ----------------

class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    price: Mapped[float] = mapped_column(Float)
    quantity: Mapped[int] = mapped_column(default=0)


# Create table if it does not exist
Base.metadata.create_all(bind=engine)


# ---------------- PYDANTIC SCHEMAS ----------------

class ProductCreate(BaseModel):
    name: str
    price: float
    quantity: int = 0


class ProductUpdate(BaseModel):
    name: str
    price: float
    quantity: int


class ProductPatch(BaseModel):
    name: str | None = None
    price: float | None = None
    quantity: int | None = None


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    price: float
    quantity: int


# ---------------- FASTAPI APP ----------------

app = FastAPI()

@app.get("/")
def home(db:Session = Depends(get_db)):
    return {"msg":"Running fine!!"}
# ---------------- CREATE ----------------

@app.post(
    "/products",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db)
):
    product = Product(**product_data.model_dump())

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


# ---------------- READ ALL ----------------

@app.get("/products", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    statement = select(Product)
    products = db.scalars(statement).all()

    return products


# ---------------- READ ONE ----------------

@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    statement = select(Product).where(Product.id == product_id)
    product = db.scalars(statement).one_or_none()

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return product


# ---------------- FULL UPDATE (PUT) ----------------

@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db)
):
    product = db.get(Product, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    product.name = product_data.name
    product.price = product_data.price
    product.quantity = product_data.quantity

    db.commit()
    db.refresh(product)

    return product


# ---------------- PARTIAL UPDATE (PATCH) ----------------

@app.patch("/products/{product_id}", response_model=ProductResponse)
def patch_product(
    product_id: int,
    product_data: ProductPatch,
    db: Session = Depends(get_db)
):
    product = db.get(Product, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    update_data = product_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)

    return product


# ---------------- DELETE ----------------

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    db.delete(product)
    db.commit()

    return {"message": "Product deleted successfully"}
