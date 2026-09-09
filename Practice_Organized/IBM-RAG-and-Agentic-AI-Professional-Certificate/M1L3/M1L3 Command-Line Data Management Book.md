# M1L3 Book: Build a Command-Line Data Management UI for Restaurant Data

This markdown book contains the complete solution split into separate chunks.

## Chunk 1: Imports and Constants

```python
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional
import json
import os
import shutil
import io
import unittest
from unittest.mock import patch

FILEPATH = "structured_restaurant_data.json"
BACKUP_PATH = "structured_restaurant_data.json.bak"
EXAMPLE_RESTAURANT_PARAGRAPH = (
    "Down in Santa Monica, Mar de Cortez serves as a sun-drenched, casual taqueria "
    "specializing in Baja-style seafood. With a 4.2/5 rating, it captures the salt-air "
    "energy of the coast through its signature beer-battered snapper tacos and zesty "
    "octopus ceviche, making it a premier spot for open-air dining near the pier. "
    "Price range: $$."
)
```

## Chunk 2: Pydantic Schema

```python
class Restaurant(BaseModel):
    id: int
    name: str
    city: Optional[str] = None
    cuisine: Optional[str] = None
    ambience: Optional[str] = None
    rating: Optional[float] = None
    price_range: Optional[str] = None
    signature_dishes: List[str] = Field(default_factory=list)
    description: Optional[str] = None
```

## Chunk 3: File Data Helpers

```python
def load_data(filepath: str = FILEPATH) -> list:
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data: list, filepath: str = FILEPATH) -> None:
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def backup_data(src: str = FILEPATH, dst: str = BACKUP_PATH) -> bool:
    if not os.path.exists(src):
        return False
    shutil.copy2(src, dst)
    return True
```

## Chunk 4: LLM Response and JSON Cleanup Helpers

```python
def _extract_response_text(response) -> str:
    if isinstance(response, dict):
        if response.get("choices"):
            msg = response["choices"][0].get("message", {})
            if isinstance(msg, dict):
                return msg.get("content", "")
        if response.get("results"):
            first = response["results"][0]
            if isinstance(first, dict):
                return first.get("generated_text") or first.get("output_text") or ""
        if response.get("error"):
            raise RuntimeError(str(response["error"]))
    return str(response)


def _safe_json_text(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:]
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return text[start : end + 1]
    return text
```

## Chunk 5: Prompt Generator for Structuring Restaurant Paragraphs

```python
def restaurant_data_structure_prompt_generation(restaurant_paragraph):
    system_msg = (
        "You are a data extraction engine. Extract restaurant information and return ONLY valid JSON."
    )
    prompt_txt = (
        "Convert the following restaurant paragraph to JSON with this exact schema:\n"
        "{\n"
        '  "id": <int>,\n'
        '  "name": <string>,\n'
        '  "city": <string|null>,\n'
        '  "cuisine": <string|null>,\n'
        '  "ambience": <string|null>,\n'
        '  "rating": <number|null>,\n'
        '  "price_range": <string|null>,\n'
        '  "signature_dishes": <array of strings>,\n'
        '  "description": <string|null>\n'
        "}\n"
        "Rules:\n"
        "- Output JSON only (no markdown, no explanation).\n"
        "- rating must be numeric if present.\n"
        "- signature_dishes must always be an array.\n"
        "- Use null for unknown values.\n\n"
        f"Paragraph:\n{restaurant_paragraph}"
    )
    return system_msg, prompt_txt
```

## Chunk 6: Core LLM Call Function

```python
def llm_model(system_msg, prompt_txt, params=None):
    model_id = "ibm/granite-3-8b-instruct"
    project_id = "skills-network"

    api_key = os.getenv("WATSONX_APIKEY") or os.getenv("API_KEY")
    if api_key:
        credentials = Credentials(url="https://us-south.ml.cloud.ibm.com", api_key=api_key)
    else:
        credentials = Credentials(url="https://us-south.ml.cloud.ibm.com")

    model = ModelInference(
        model_id=model_id,
        credentials=credentials,
        project_id=project_id,
        params=params or {"max_new_tokens": 600, "temperature": 0.0},
    )

    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": prompt_txt},
    ]

    response = model.chat(messages=messages)
    return _extract_response_text(response)
```

## Chunk 7: JSON Auto-Repair Prompt Builder

```python
def JSON_auto_repair_prompts(response, error_message):
    system_msg = "You repair malformed JSON and output JSON only."
    prompt_txt = (
        "The following JSON is invalid for the restaurant schema.\n\n"
        f"Validation error:\n{error_message}\n\n"
        f"Broken JSON:\n{response}\n\n"
        "Return corrected JSON with keys:\n"
        "id, name, city, cuisine, ambience, rating, price_range, signature_dishes, description\n"
        "Rules:\n"
        "- Output JSON only.\n"
        "- rating must be number or null.\n"
        "- signature_dishes must be an array of strings.\n"
        "- Keep meaning, only fix schema/types."
    )
    return system_msg, prompt_txt
```

## Chunk 8: Required Function - new_data_entry_process

```python
def new_data_entry_process(paragraph, itemId):
    system_msg, prompt_txt = restaurant_data_structure_prompt_generation(paragraph)
    raw_text = llm_model(system_msg, prompt_txt)
    raw_text = _safe_json_text(raw_text)

    max_retries = 3
    last_error = None

    for _ in range(max_retries):
        try:
            record = Restaurant.model_validate_json(raw_text).model_dump()
            record["id"] = int(itemId)
            return record
        except ValidationError as ve:
            last_error = str(ve)
            rep_sys, rep_prompt = JSON_auto_repair_prompts(raw_text, last_error)
            raw_text = _safe_json_text(llm_model(rep_sys, rep_prompt))
        except Exception as e:
            last_error = str(e)
            break

    raise ValueError(f"Failed to structure new entry after retries. Last error: {last_error}")
```

## Chunk 9: CRUD Utility Functions

```python
def get_next_id(data: list) -> int:
    if not data:
        return 1
    return max(int(item.get("id", 0)) for item in data) + 1


def list_restaurants(data: list) -> None:
    if not data:
        print("No restaurant records found.")
        return
    for item in data:
        print(
            f"[{item.get('id')}] {item.get('name')} | "
            f"{item.get('city', 'N/A')} | rating={item.get('rating', 'N/A')}"
        )


def view_restaurant(data: list, item_id: int) -> None:
    record = next((x for x in data if int(x.get("id", -1)) == item_id), None)
    if not record:
        print("Record not found.")
        return
    print(json.dumps(record, indent=2, ensure_ascii=False))


def add_restaurant(data: list) -> list:
    paragraph = input("Paste new restaurant paragraph: ").strip()
    if not paragraph:
        print("No paragraph provided.")
        return data
    item_id = get_next_id(data)
    record = new_data_entry_process(paragraph, item_id)
    data.append(record)
    print(f"Added restaurant id={item_id}: {record.get('name')}")
    return data


def update_restaurant(data: list) -> list:
    item_id = int(input("Enter id to update: ").strip())
    idx = next((i for i, x in enumerate(data) if int(x.get("id", -1)) == item_id), None)
    if idx is None:
        print("Record not found.")
        return data
    paragraph = input("Paste updated restaurant paragraph: ").strip()
    if not paragraph:
        print("No paragraph provided.")
        return data
    record = new_data_entry_process(paragraph, item_id)
    data[idx] = record
    print(f"Updated restaurant id={item_id}: {record.get('name')}")
    return data


def delete_restaurant(data: list) -> list:
    item_id = int(input("Enter id to delete: ").strip())
    new_data = [x for x in data if int(x.get("id", -1)) != item_id]
    if len(new_data) == len(data):
        print("Record not found.")
        return data
    print(f"Deleted restaurant id={item_id}")
    return new_data
```

## Chunk 10: CLI Menu and Main Loop

```python
def print_menu() -> None:
    print("\nRestaurant Data Management")
    print("1) List all restaurants")
    print("2) View restaurant by id")
    print("3) Add new restaurant (from paragraph)")
    print("4) Update restaurant (from paragraph)")
    print("5) Delete restaurant")
    print("6) Backup data")
    print("7) Save")
    print("0) Exit")


def run_cli():
    data = load_data(FILEPATH)
    print(f"Loaded {len(data)} records from {FILEPATH}")

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            list_restaurants(data)
        elif choice == "2":
            item_id = int(input("Enter id: ").strip())
            view_restaurant(data, item_id)
        elif choice == "3":
            data = add_restaurant(data)
        elif choice == "4":
            data = update_restaurant(data)
        elif choice == "5":
            data = delete_restaurant(data)
        elif choice == "6":
            ok = backup_data(FILEPATH, BACKUP_PATH)
            print("Backup created." if ok else "No source file to back up.")
        elif choice == "7":
            save_data(data, FILEPATH)
            print(f"Saved to {FILEPATH}")
        elif choice == "0":
            save_data(data, FILEPATH)
            print("Saved and exiting.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    run_cli()
```

## Chunk 11: Optional Quick Local Test Snippet

```python
if __name__ == "__main__":
    sample_data = load_data(FILEPATH)
    print(f"Current records: {len(sample_data)}")
```
