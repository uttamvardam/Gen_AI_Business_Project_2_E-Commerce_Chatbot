from semantic_router import Route
from semantic_router.routers import IndexedRouter
from semantic_router.encoders import HuggingFaceEncoder

encoder = HuggingFaceEncoder(
    name="sentence-transformers/all-MiniLM-L6-v2"
)

faq = Route(
    name='faq',
    utterances=[
        "What is the return policy?",
        "Can I return or exchange my order?",
        "Do I get discount with the HDFC credit card?",
        "How can I track my order?",
        "Where is my package right now?",
        "What payment methods are accepted?",
        "Can I pay with UPI or cash on delivery?",
        "How long does it take to process a refund?",
        "When will I get my refund money?",
        "Are there any ongoing sales, deals, or store promotions?",
        "Can I cancel or modify my order after placing it?",
        "Do you offer international shipping outside India?",
        "What should I do if I receive a damaged or defective item?",
        "How do I use a promo code or coupon during checkout?",
    ]
)

sql = Route(
    name='sql',
    utterances=[
        "I want to buy nike shoes that have 50% discount.",
        "Are there any shoes under Rs. 3000?",
        "Do you have formal shoes in size 9?",
        "Are there any Puma shoes on sale?",
        "What is the price of puma running shoes?",
        "Show me sports shoes for women",
        "Which product has the highest rating?",
        "What is the best rated shoe?",
        "Top rated shoes in your store",
        "Which shoe has the best customer reviews?",
        "Show me products with 5 star rating",
        "Which brand has the most products?",
        "Which brand has the largest number of shoes?",
        "How many products do you have?",
        "List all available shoe brands",
        "What is the most expensive shoe?",
        "What is the cheapest shoe available?",
        "Which brand gives the maximum discount?",
        "Show me Campus running shoes under 1500",
        "Find black sneakers with discount",
        "Do you have Skechers walking shoes?",
        "Which shoe is cheapest?",
    ]
)

# Define routes list
routes = [faq, sql]

# Initialize SemanticRouter
router = IndexedRouter(encoder=encoder, routes=routes)


if __name__ == "__main__":
    print(router("What is your policy on defective product?").name)
    print(router("Pink Puma shoes in price range 5000 to 1000").name)