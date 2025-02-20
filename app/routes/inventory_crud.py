from fastapi import Depends,Request
from fastapi import APIRouter
from slowapi.util import get_remote_address
from app.models.basemodel import *
from app.utils.utils import *
from app.db.database import *
from app.main import limiter
item_id_counter = 0

router = APIRouter(tags=["Inventory CRUD"])

@router.post("/add-new-item", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def add_new_item(request: Request, item: Item, current_user: User = Depends(get_current_user),role: str = Depends(require_role_jwt("admin"))):
    global item_id_counter
    item_id_counter = item_id_counter + 1
    icon = get_inventory_db()
    cursor = icon.cursor()
    cursor.execute("INSERT INTO inventory (item_id, item_name, item_description, item_price) VALUES (?, ?, ?, ?)", (item_id_counter, item.item_name, item.item_description, item.item_price))
    icon.commit()
    icon.close()
    return  {"message": "Item Created Successfully with the item id %s"%(item_id_counter)}
   
@router.get("/get-all-items", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
async def get_all_items(request: Request, current_user: User = Depends(get_current_user),role: str = Depends(require_role_jwt("admin"))):
    global item_id_counter
    item_id_counter = item_id_counter + 1
    all_items = convert_sql_result_to_json("inventory")
    return  all_items

@limiter.limit("5/minute")
@router.get("/item/{item_id}",status_code=status.HTTP_200_OK)
async def get_item_detail(item_id: int, request: Request, current_user: User = Depends(get_current_user),role: str = Depends(require_role_jwt("admin"))):
    icon = get_inventory_db()
    cursor = icon.cursor()
    cursor.execute("select * from inventory where item_id=%s"%(item_id))
    item_detail =  cursor.fetchone()
    icon.close()
    if item_detail is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id":item_detail["item_id"],"item_name":item_detail["item_name"],"item_description":item_detail["item_description"],"item_price":item_detail["item_price"]}

@limiter.limit("5/minute")
@router.put("/update-item/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_item_detail(item_id: int, item: Item, request: Request, current_user: User = Depends(get_current_user),role: str = Depends(require_role_jwt("admin"))):
    icon = get_inventory_db()
    cursor = icon.cursor()
    query="update inventory set item_name = '%s', item_description = '%s', item_price='%s' where item_id =%s"%(item.item_name, item.item_description, item.item_price, item_id)
    cursor.execute(query)
    row_count = cursor.rowcount
    icon.commit()
    icon.close()
    if row_count == 0 :
        raise HTTPException (
            status_code= 400,
            detail= "item %s doesnt exist"%(item_id)
        )
    return  {"message": "Item Updated Successfully with the item id %s"%(item_id)}

@limiter.limit("5/minute")
@router.delete("/delete-item/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, request: Request, current_user: User = Depends(get_current_user),role: str = Depends(require_role_jwt("admin"))):
    icon = get_inventory_db()
    cursor = icon.cursor()
    query="delete from inventory where item_id = %s"%(item_id)
    cursor.execute(query)
    row_count = cursor.rowcount
    icon.commit()
    icon.close()
    if row_count == 0 :
        raise HTTPException (
            status_code= 400,
            detail= "item %s doesnt exist"%(item_id)
        )
    return  {"message": "Item Deleted Successfully with the item id- %s"%(item_id)}
