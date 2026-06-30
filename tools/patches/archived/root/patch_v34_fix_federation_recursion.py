from pathlib import Path

path = Path("aletheus/federation_v3/federation_core.py")
text = path.read_text()

text = text.replace(
'''    def statistics(self):

        self.bootstrap()

        return {

            "version": self.VERSION,

            "federation": self.federation.name,

            "remote_nodes": len(

                self.federation.remote_nodes

            ),

            "health": "healthy",

        }
''',
'''    def statistics(self):

        if self.federation is None:
            return {
                "version": self.VERSION,
                "federation": None,
                "remote_nodes": 0,
                "health": "not_initialized",
            }

        return {
            "version": self.VERSION,
            "federation": self.federation.name,
            "remote_nodes": len(self.federation.remote_nodes),
            "health": "healthy",
        }
'''
)

path.write_text(text)

print("✔ Federation recursion fixed.")
