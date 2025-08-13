from notion_client import Client

class NotionTool:
    def __init__(self, api_key, database_id):
        self.client = Client(auth=api_key)
        self.db_id = database_id

    def add_note(self, title, content):
        self.client.pages.create(
            parent={"database_id": self.db_id},
            properties={"Name": {"title": [{"text": {"content": title}}]}},
            children=[{"object": "block", "type": "paragraph", "paragraph": {"text": [{"type": "text", "text": {"content": content}}]}}]
        )
        return "Note added to Notion."

    def list_notes(self, limit=5):
        results = self.client.databases.query(database_id=self.db_id, page_size=limit)
        return [r["properties"]["Name"]["title"][0]["plain_text"] for r in results["results"]]
