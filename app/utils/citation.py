def format_citations(matches):
    citations = []
    seen = set()

    for match in matches:
        metadata = match.get("metadata", {})

        citation = {
            "document": metadata.get(
                "document_name",
                "Unknown Document"
            ),
            "source": metadata.get(
                "source",
                "Unknown Source"
            ),
            "topic": metadata.get(
                "topic",
                "Unknown Topic"
            ),
            "year": metadata.get(
                "year",
                "Unknown Year"
            )
        }

        citation_key = (
            citation["document"],
            citation["source"]
        )

        if citation_key not in seen:
            citations.append(citation)
            seen.add(citation_key)

    return citations

