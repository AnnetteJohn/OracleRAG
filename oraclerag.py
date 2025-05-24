from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
import os

# =============================================
# Configuration 
# =============================================

# Azure AI Search configuration
AZURE_SEARCH_SERVICE = "aiminiproject"  
AZURE_SEARCH_INDEX = "hotels-sample-index" 
AZURE_SEARCH_ENDPOINT = "https://aiminiproject.search.windows.net"
AZURE_SEARCH_KEY = ""

# =============================================
# Set up client
# =============================================

# Set up Azure AI Search client
search_client = SearchClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    index_name=AZURE_SEARCH_INDEX,
    credential=AzureKeyCredential(AZURE_SEARCH_KEY)
)

# =============================================
# Information Retrieval implementation
# =============================================

def search_documents(query_text, top=5):
    """
    Search for relevant documents in Azure AI Search
    """
    # Use a simple keyword search
    search_results = search_client.search(
        search_text=query_text,
        select=["HotelName", "Description", "Category", "Tags", "Rating", "Address/City", "Address/StateProvince"],
        top=top
    )
    
    # Process results
    documents = []
    for result in search_results:
        doc = {
            "name": result["HotelName"],
            "description": result["Description"],
            "category": result["Category"]
        }
        
        # Add optional fields if they exist
        if "Rating" in result:
            doc["rating"] = result["Rating"]
        
        if "Tags" in result:
            doc["tags"] = result["Tags"]
        
        if "Address/City" in result:
            doc["city"] = result["Address/City"]
            
        if "Address/StateProvince" in result:
            doc["state"] = result["Address/StateProvince"]
            
        documents.append(doc)
    
    return documents

def format_results(query, documents):
    """
    Format the retrieved documents into a readable response
    """
    if not documents:
        return f"No results found for '{query}'."
    
    response = f"Results for '{query}':\n\n"
    
    for i, doc in enumerate(documents, 1):
        response += f"Result {i}: {doc['name']}\n"
        response += f"Category: {doc['category']}\n"
        
        if "rating" in doc:
            response += f"Rating: {doc['rating']} stars\n"
            
        if "city" in doc and "state" in doc:
            response += f"Location: {doc['city']}, {doc['state']}\n"
            
        if "tags" in doc and doc['tags']:
            response += f"Features: {', '.join(doc['tags'])}\n"
            
        response += f"Description: {doc['description']}\n\n"
    
    # Add a summary section
    response += "Summary:\n"
    response += f"Found {len(documents)} hotels matching your search for '{query}'.\n"
    
    # Add some simple analysis
    categories = {}
    locations = {}
    total_rating = 0
    rating_count = 0
    
    for doc in documents:
        # Count by category
        cat = doc['category']
        categories[cat] = categories.get(cat, 0) + 1
        
        # Count by location if available
        if "city" in doc:
            city = doc['city']
            locations[city] = locations.get(city, 0) + 1
        
        # Calculate average rating if available
        if "rating" in doc:
            total_rating += doc['rating']
            rating_count += 1
    
    # Add category breakdown
    response += "\nCategory breakdown:\n"
    for cat, count in categories.items():
        response += f"- {cat}: {count} hotels\n"
    
    # Add location breakdown if available
    if locations:
        response += "\nLocation breakdown:\n"
        for loc, count in locations.items():
            response += f"- {loc}: {count} hotels\n"
    
    # Add average rating if available
    if rating_count > 0:
        avg_rating = total_rating / rating_count
        response += f"\nAverage rating: {avg_rating:.1f} stars\n"
    
    return response

def information_retrieval_query(user_query):
    """
    Complete information retrieval workflow: retrieve documents and format results
    """
    print(f"Query: {user_query}")
    print("\nRetrieving relevant documents...")
    
    # Step 1: Retrieve relevant documents
    retrieved_docs = search_documents(user_query)
    
    print(f"Found {len(retrieved_docs)} relevant documents")
    
    # Step 2: Format results into a readable response
    print("\nFormatting results...")
    response = format_results(user_query, retrieved_docs)
    
    print("\nFormatted Response:")
    print(response)
    
    return {
        "query": user_query,
        "retrieved_documents": retrieved_docs,
        "response": response
    }

# =============================================
# Simple CLI to demonstrate the workflow
# =============================================

def main():
    print("=== Simple Information Retrieval Implementation with Azure AI Search ===")
    print("(Using the sample hotels index for demonstration)")
    print("\nType 'exit' to quit")
    
    while True:
        user_query = input("\nEnter your question about hotels: ")
        
        if user_query.lower() == 'exit':
            break
        
        result = information_retrieval_query(user_query)

if __name__ == "__main__":
    main()