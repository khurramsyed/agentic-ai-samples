import traceback

class ChatInterface:
    def __init__(self, query_processor):
        self.query_processor = query_processor
    
    async def run_chat_loop(self):
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                query = input("\nQuery: ").strip()
                if query.lower() == 'quit':
                    break

                response = await self.query_processor.process_query(query)
                print("\n" + response)

            except Exception as e:
                print(f"\nError: {str(e)}")
                traceback.print_exc()