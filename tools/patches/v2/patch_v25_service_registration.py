from pathlib import Path

path = Path("aletheus/runtime/core.py")
text = path.read_text()

service_block = '''
        self.services.register(
            "Aletheus Cognitive Reasoning Engine",
            {
                "status": "online",
                "version": self.reasoning.version,
            },
        )
'''

# Add registration after Knowledge Graph registration
if '"Aletheus Cognitive Reasoning Engine"' not in text:
    anchor = '''
        self.services.register(
            "Aletheus Knowledge Graph Engine",
            {
                "status": "online",
                "version": self.knowledge_graph.version,
            },
        )
'''
    if anchor in text:
        text = text.replace(anchor, anchor + service_block)
    else:
        print("Knowledge Graph service registration not found.")
        raise SystemExit(1)

path.write_text(text)
print("✔ Reasoning service registration added.")
