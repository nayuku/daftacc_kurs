from sqlalchemy.orm import Session

from . import models, schemas


def get_shippers(db: Session):
    return db.query(models.Shipper).all()


def get_shipper(db: Session, shipper_id: int):
    return (
        db.query(models.Shipper).filter(models.Shipper.ShipperID == shipper_id).first()
    )


def get_suppliers(db: Session):
    return db.query(models.Supplier).all()


def get_supplier(db: Session, supplier_id: int):
    return db.query(models.Supplier).filter(models.Supplier.SupplierID == supplier_id).first()


def get_suppliers_products(db: Session, supplier_id: int):
    return db.query(models.Product.ProductID,
                    models.Product.ProductName,
                    models.Category.CategoryID,
                    models.Category.CategoryName,
                    models.Product.Discontinued,
                    ).join(models.Supplier, models.Product.SupplierID == models.Supplier.SupplierID) \
        .join(models.Category, models.Product.CategoryID == models.Category.CategoryID) \
        .filter(models.Product.SupplierID == supplier_id) \
        .order_by(models.Product.ProductID.desc()).all()


def add_supplier(db, supplier: models.Supplier):
    db.add(supplier)
    db.commit()
    pass


def modify_suppliers(db: Session, supplier_id, supplier: schemas.SupplierAll):
    mod_supplier = {col: val for col, val in dict(supplier).items() if val is not None}
    if mod_supplier:
        db.query(models.Supplier).filter(models.Supplier.SupplierID == supplier_id)\
            .update(values=mod_supplier)
        db.commit()
        pass


def delete_suppliers(db: Session, id: int):
    db.query(models.Supplier).filter(models.Supplier == id).delete()
    db.commit()
    pass
