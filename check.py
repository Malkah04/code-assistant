from generation.data import create_vb

vector_store = create_vb()

results = vector_store.get(
    include=["documents", "metadatas"]
)

print("Total documents:", len(results["ids"]))

for doc_id, document, metadata in zip(
    results["ids"],
    results["documents"],
    results["metadatas"],
):
    if metadata.get("source") == "user_feedback":
        print("\nFOUND USER FEEDBACK")
        print("ID:", doc_id)
        print("Metadata:", metadata)
        print("Document:", document)

print("\nSources in database:")
for metadata in results["metadatas"]:
    print(metadata.get("source"))