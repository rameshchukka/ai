try:
	from ibm_watsonx_ai import Credentials
	from ibm_watsonx_ai.foundation_models import ModelInference
except Exception:
	Credentials = None
	ModelInference = None
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


def llm_model(system_msg, prompt_txt, params=None):
	project_id = "skills-network"
	candidate_models = [
		"meta-llama/llama-3-1-8b",
		"meta-llama/llama-3-3-70b-instruct",
		"mistralai/mistral-small-3-1-24b-instruct-2503",
	]

	if Credentials is None or ModelInference is None:
		raise RuntimeError("ibm_watsonx_ai is not installed in this Python environment.")

	api_key = os.getenv("WATSONX_APIKEY") or os.getenv("API_KEY")
	if api_key:
		credentials = Credentials(url="https://us-south.ml.cloud.ibm.com", api_key=api_key)
	else:
		credentials = Credentials(url="https://us-south.ml.cloud.ibm.com")

	messages = [
		{"role": "system", "content": system_msg},
		{"role": "user", "content": prompt_txt},
	]

	last_error = None
	for model_id in candidate_models:
		try:
			model = ModelInference(
				model_id=model_id,
				credentials=credentials,
				project_id=project_id,
				params=params or {"max_new_tokens": 600, "temperature": 0.0},
			)
			response = model.chat(messages=messages)
			return _extract_response_text(response)
		except Exception as e:
			last_error = e
			continue

	raise RuntimeError(f"No supported model worked. Last error: {last_error}")


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


def show_restaurant_card(res, index):
	print("\n--- Restaurant Card ---")
	print(f"index: {index}")
	print(json.dumps(res[index], indent=2, ensure_ascii=False))


def manage_restaurants(file_path, backup_path):
	while True:
		data = load_data(file_path)
		print(f"\n🏨 RESTAURANT DATABASE | Records: {len(data)}")
		print("1. Browse All (Names)")
		print("2. View Detailed Record")
		print("3. Add New Restaurant")
		print("4. Edit Restaurant Info")
		print("5. Delete Restaurant")
		print("6. Exit")

		choice = str(input("\nAction: ")).strip()

		if choice == '1':
			print("\n--- Current Listings ---")
			for i, rec in enumerate(data):
				print(f"{i}: {rec.get('name', 'N/A')}")

		elif choice == '2':
			idx_raw = str(input("Enter record index: ")).strip()
			if idx_raw.isdigit():
				idx = int(idx_raw)
				if 0 <= idx < len(data):
					show_restaurant_card(data, idx)
				else:
					print("invalid index.")
			else:
				print("invalid index.")

		elif choice in ['3', '4', '5']:
			print("\n❗ SECURITY WARNING: You are entering write-mode.")
			print("Changes will be saved to the database immediately.")
			confirm = str(input("Are you sure? (type 'yes' to proceed): ")).lower()
			if confirm != 'yes':
				print("Operation cancelled.")
				continue

			if choice == '3':
				itemId = 1000000 + len(data) + 1
				new_paragraph = str(input("Enter new restaurant description: ")).strip()
				if not new_paragraph:
					print("Operation cancelled.")
					continue
				try:
					new_record = new_data_entry_process(new_paragraph, itemId)
				except Exception:
					new_record = {
						"id": itemId,
						"name": new_paragraph,
						"city": None,
						"cuisine": None,
						"ambience": None,
						"rating": None,
						"price_range": None,
						"signature_dishes": [],
						"description": new_paragraph,
					}
				data.append(new_record)
				save_data(data, file_path)
				backup_data(file_path, backup_path)
				print("✅ Restaurant added.")

			elif choice == '4':
				idx_raw = str(input("Enter record index to edit: ")).strip()
				if not idx_raw.isdigit():
					print("invalid index.")
					continue
				idx = int(idx_raw)
				if not (0 <= idx < len(data)):
					print("invalid index.")
					continue

				for key in list(data[idx].keys()):
					new_val = str(input(f"{key} [{data[idx].get(key)}]: "))
					if new_val.strip() == "":
						continue
					if key == "rating":
						try:
							data[idx][key] = float(new_val)
						except ValueError:
							print("Invalid rating. Keeping old value.")
					elif key == "signature_dishes":
						data[idx][key] = [x.strip() for x in new_val.split(",") if x.strip()]
					elif key == "id":
						try:
							data[idx][key] = int(new_val)
						except ValueError:
							print("Invalid id. Keeping old value.")
					else:
						data[idx][key] = new_val

				save_data(data, file_path)
				backup_data(file_path, backup_path)
				print("✅ Record updated.")

			elif choice == '5':
				idx_raw = str(input("Enter record index to delete: ")).strip()
				if not idx_raw.isdigit():
					print("invalid index.")
					continue
				idx = int(idx_raw)
				if not (0 <= idx < len(data)):
					print("invalid index.")
					continue

				data.pop(idx)
				save_data(data, file_path)
				backup_data(file_path, backup_path)
				print("✅ Record deleted.")

		elif choice == '6':
			break
		else:
			print("Invalid input.")


class TestRestaurantDatabase(unittest.TestCase):

	def setUp(self):
		self.test_file = 'structured_restaurant_data_unit_test.json'
		self.test_file_backup = 'structured_restaurant_data_unit_test.json.bak'
		self.initial_data = [{"name": "Test Cafe", "location": "Test City"}]
		with open(self.test_file, 'w', encoding='utf-8') as f:
			json.dump(self.initial_data, f)

	def tearDown(self):
		if os.path.exists(self.test_file):
			os.remove(self.test_file)
		if os.path.exists(self.test_file_backup):
			os.remove(self.test_file_backup)

	@patch('builtins.input')
	@patch('sys.stdout', new_callable=io.StringIO)
	def test_add_and_delete_restaurant_success(self, mock_stdout, mock_input):
		mock_restaurant = (
			'The Copper Sprout is a high-concept, Modern Appalachian farm-to-table destination '
			'that blends an industrial-chic aesthetic with rustic forest charm, featuring reclaimed '
			'wood and amber lighting to create a sophisticated yet cozy vibe. Priced in the $$ '
			'category, the menu celebrates seasonal foraging and local heritage, headlined by '
			'signature dishes like Cast-Iron Smoked Trout with pickled fiddlehead ferns and '
			'hand-foraged Wild Mushroom Risotto with aged goat cheese. The experience is designed '
			'to be intimate and earthy, making it a premier spot for those seeking high-quality, '
			'smokehouse-influenced cuisine in a refined, atmospheric setting.'
		)
		mock_input.side_effect = ['3', 'yes', mock_restaurant, '6']

		try:
			manage_restaurants(self.test_file, self.test_file_backup)
		except SystemExit:
			pass

		with open(self.test_file, 'r', encoding='utf-8') as f:
			data = json.load(f)

		self.assertEqual(len(data), 2)
		self.assertIn("✅ Restaurant added.", mock_stdout.getvalue())

		mock_input.side_effect = ['5', 'yes', '1', '6']

		try:
			manage_restaurants(self.test_file, self.test_file_backup)
		except SystemExit:
			pass

		with open(self.test_file, 'r', encoding='utf-8') as f:
			data = json.load(f)

		self.assertEqual(len(data), 1)

	@patch('builtins.input')
	@patch('sys.stdout', new_callable=io.StringIO)
	def test_delete_security_cancel(self, mock_stdout, mock_input):
		mock_input.side_effect = ['5', 'no', '6']

		manage_restaurants(self.test_file, self.test_file_backup)

		with open(self.test_file, 'r', encoding='utf-8') as f:
			data = json.load(f)

		self.assertEqual(len(data), 1)
		self.assertIn("Operation cancelled.", mock_stdout.getvalue())


if __name__ == "__main__":
	unittest.main()
	# manage_restaurants(FILEPATH, BACKUP_PATH)
