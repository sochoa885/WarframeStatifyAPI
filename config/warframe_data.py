from functools import reduce
import time
import httpx
from sqlalchemy.orm import Session
from crud.items import get_items, get_rank_0_forty_eight_hours_by_item_id, get_rank_0_ninety_days_by_item_id, get_rank_max_forty_eight_hours_by_item_id, get_rank_max_ninety_days_by_item_id, insert_many_forty_eight_hours, insert_many_items, get_item_by_name, insert_many_ninety_days, update_many_forty_eight_hours, update_many_ninety_days
from database import SessionLocal

interval_item_seconds = 2
WARFRAME_API_URL_V2 = "https://api.warframe.market/v2/items"
WARFRAME_API_URL_V1 = "https://api.warframe.market/v1/items"
tags = {
    "warframe": 1,
    "primary": 2,
    "secondary": 3,
    "melee": 4,
    "necramech": 5
}
types = {
    "component": 1,
    "arcane_enhancement": 2,
    "mod": 3
}

async def insert_statistics(db: Session):
    items = get_items(db);
    create_forty_eight_items = []
    create_ninety_items = []
    update_forty_eight_items = []
    update_ninety_items = []
    for item in items:
        async with httpx.AsyncClient() as client:
            time.sleep(interval_item_seconds)
            try:
                response = await client.get(f"{WARFRAME_API_URL_V1}/{item.url_name}/statistics")
                response.raise_for_status()
                statistics_closed = response.json().get("payload", {}).get("statistics_closed", {})
                forty_eight_hours = statistics_closed.get("48hours", {})
                forty_eight = list(filter(lambda x: x.get("mod_rank", 0) == 0, forty_eight_hours))
                forty_eight_max = list(filter(lambda x: x.get("mod_rank", 10) > 0, forty_eight_hours))
                ninety_days = statistics_closed.get("90days", {})
                ninety = list(filter(lambda x: x.get("mod_rank", 0) == 0, ninety_days))
                ninety_max = list(filter(lambda x: x.get("mod_rank", 10) > 0, ninety_days))
                avg_price48 = reduce(lambda x, y: x + y.get("avg_price", 0.0), forty_eight, 0) / (len(forty_eight) or 1)
                avg_price90 = reduce(lambda x, y: x + y.get("avg_price", 0.0), ninety, 0) / (len(ninety) or 1)
                total_volume48 = reduce(lambda x, y: x + y.get("volume", 0), forty_eight, 0)
                total_volume90 = reduce(lambda x, y: x + y.get("volume", 0), ninety, 0)
                avg_price48max = reduce(lambda x, y: x + y.get("avg_price", 0.0), forty_eight_max, 0) / (len(forty_eight_max) or 1)
                avg_price90max = reduce(lambda x, y: x + y.get("avg_price", 0.0), ninety_max, 0) / (len(ninety_max) or 1)
                total_volume48max = reduce(lambda x, y: x + y.get("volume", 0), forty_eight_max, 0)
                total_volume90max = reduce(lambda x, y: x + y.get("volume", 0), ninety_max, 0)
                if(len(forty_eight) > 0):
                    existing_item = get_rank_0_forty_eight_hours_by_item_id(db, item.id)
                    if existing_item:
                        item_data = {
                            "id": existing_item.id,
                            "volume": total_volume48,
                            "avg_price": round(avg_price48, 1),
                            "rank": 0,
                            "item_id": item.id
                        }
                        update_forty_eight_items.append(item_data)
                    else:
                        item_data = {
                            "volume": total_volume48,
                            "avg_price": round(avg_price48, 1),
                            "rank": 0,
                            "item_id": item.id
                        }
                        create_forty_eight_items.append(item_data)
                if(len(list(forty_eight_max)) > 0):
                    existing_item = get_rank_max_forty_eight_hours_by_item_id(db, item.id)
                    if existing_item:
                        item_data = {
                            "id": existing_item.id,
                            "volume": total_volume48max,
                            "avg_price": round(avg_price48max, 1),
                            "rank": 10,
                            "item_id": item.id
                        }
                        update_forty_eight_items.append(item_data)
                    else:
                        item_data = {
                            "volume": total_volume48max,
                            "avg_price": round(avg_price48max, 1),
                            "rank": 10,
                            "item_id": item.id
                        }
                        create_forty_eight_items.append(item_data)
                if(len(list(ninety)) > 0):
                    existing_item = get_rank_0_ninety_days_by_item_id(db, item.id)
                    if existing_item:
                        item_data = {
                            "id": existing_item.id,
                            "volume": total_volume90,
                            "avg_price": round(avg_price90, 1),
                            "rank": 0,
                            "item_id": item.id
                        }
                        update_ninety_items.append(item_data)
                    else:
                        item_data = {
                            "volume": total_volume90,
                            "avg_price": round(avg_price90, 1),
                            "rank": 0,
                            "item_id": item.id
                        }
                        create_ninety_items.append(item_data)
                if(len(list(ninety_max)) > 0):
                    existing_item = get_rank_max_ninety_days_by_item_id(db, item.id)
                    if existing_item:
                        item_data = {
                            "id": existing_item.id,
                            "volume": total_volume90max,
                            "avg_price": round(avg_price90max, 1),
                            "rank": 10,
                            "item_id": item.id
                        }
                        update_ninety_items.append(item_data)
                    else:
                        item_data = {
                            "volume": total_volume90max,
                            "avg_price": round(avg_price90max, 1),
                            "rank": 10,
                            "item_id": item.id
                        }
                        create_ninety_items.append(item_data)
            except:
                print(f"{item.name_en} not fetching")
                raise
        print(f"Stats for {item.name_en} loaded")
    insert_many_forty_eight_hours(db, create_forty_eight_items)
    insert_many_ninety_days(db, create_ninety_items)
    update_many_forty_eight_hours(db, update_forty_eight_items)
    update_many_ninety_days(db, update_ninety_items)
    print("Stats updated succesfully!")
    

async def fetch_and_update_items():
    db: Session = SessionLocal()
    headers = {'Language': 'es'}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(WARFRAME_API_URL_V2, headers=headers)
            response.raise_for_status()
        except httpx.RequestError as e:
            print(f"Error fetching data: {e}")
            return
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code} - {e.response.text}")
            return
    items = list(response.json().get("data", {}))
    items_data = []
    for index, item in enumerate(items):
        i18n = item.get("i18n", {})
        name_en = i18n.get("en", {}).get("name", "Unknown Item")
        name_es = i18n.get("es", {}).get("name", "Unknown Item")
        icon = i18n.get("en", {}).get("icon", "Unknown_Icon")
        url_name = item.get("urlName", "Unknown_Url")
        tag = next((tipo for clave, tipo in tags.items() if clave in item.get("tags", [])), 6)
        item_type = next((tipo for clave, tipo in types.items() if clave in item.get("tags", [])), 4)
        item_data = {
            "name_en": name_en,
            "name_es": name_es,
            "url_name": url_name,
            "icon": icon,
            "tag_id": tag,
            "type_id": item_type
        }
        existing_item = get_item_by_name(db, name_en)
        if not existing_item:
            items_data.append(item_data)
        print(f"Loaded item: {index+1}/{len(items)}")
    try: 
        insert_many_items(db, items_data)
    except ValueError as e:
        print("Error loading items ", e)
        raise
    print("Items updated successfully!")
    time.sleep(1)
    await insert_statistics(db)